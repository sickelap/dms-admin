from typing import TypeVar

from fastapi import Depends

from dms_admin_api.config import Settings, get_settings
from dms_admin_api.dms.models import Account, Alias, CommandResult, MutationResult, Quota, RelayState
from dms_admin_api.dms.parsers import parse_accounts, parse_aliases, parse_quotas, parse_relay_state
from dms_admin_api.dms.runner import CommandRunner

T = TypeVar("T")


class DmsService:
    def __init__(self, settings: Settings, runner: CommandRunner | None = None) -> None:
        self.settings = settings
        self.runner = runner or CommandRunner()

    def _docker_exec(self, *command: str) -> CommandResult:
        return self.runner.run(
            [
                self.settings.docker_binary,
                "exec",
                self.settings.dms_container_name,
                *command,
            ]
        )

    def _read_config(self, filename: str) -> str:
        result = self._docker_exec("cat", f"{self.settings.dms_config_dir}/{filename}")
        if result.exit_code != 0:
            return ""
        return result.stdout

    def _verify(self, condition: bool, success_detail: str, failed_detail: str) -> MutationResult:
        if condition:
            return MutationResult(status="applied", detail=success_detail)
        return MutationResult(status="verification_failed", detail=failed_detail)

    def _normalize_quota(self, quota: str) -> str:
        return quota.replace(" ", "").upper()

    def connectivity(self) -> bool:
        return self._docker_exec("setup", "help").exit_code == 0

    def list_accounts(self) -> list[Account]:
        return parse_accounts(self._read_config("postfix-accounts.cf"))

    def create_account(self, email: str, password: str) -> MutationResult:
        result = self._docker_exec("setup", "email", "add", email, password)
        if result.exit_code != 0:
            return MutationResult(status="failed", detail=result.stderr.strip() or result.stdout.strip())

        emails = {account.email for account in self.list_accounts()}
        return self._verify(email in emails, f"Account {email} created", f"Account {email} was not observed after creation")

    def update_account_password(self, email: str, password: str) -> MutationResult:
        result = self._docker_exec("setup", "email", "update", email, password)
        if result.exit_code != 0:
            return MutationResult(status="failed", detail=result.stderr.strip() or result.stdout.strip())

        emails = {account.email for account in self.list_accounts()}
        return self._verify(email in emails, f"Password updated for {email}", f"Account {email} was not observed after password update")

    def delete_account(self, email: str) -> MutationResult:
        result = self._docker_exec("setup", "email", "del", "-y", email)
        if result.exit_code != 0:
            return MutationResult(status="failed", detail=result.stderr.strip() or result.stdout.strip())

        emails = {account.email for account in self.list_accounts()}
        return self._verify(email not in emails, f"Account {email} removed", f"Account {email} was still observed after deletion")

    def list_aliases(self) -> list[Alias]:
        return parse_aliases(self._read_config("postfix-virtual.cf"))

    def create_alias(self, address: str, target: str) -> MutationResult:
        result = self._docker_exec("setup", "alias", "add", address, target)
        if result.exit_code != 0:
            return MutationResult(status="failed", detail=result.stderr.strip() or result.stdout.strip())

        aliases = {(alias.address, alias.target) for alias in self.list_aliases()}
        return self._verify((address, target) in aliases, f"Alias {address} created", f"Alias {address} was not observed after creation")

    def delete_alias(self, address: str, target: str) -> MutationResult:
        result = self._docker_exec("setup", "alias", "del", address, target)
        if result.exit_code != 0:
            return MutationResult(status="failed", detail=result.stderr.strip() or result.stdout.strip())

        aliases = {(alias.address, alias.target) for alias in self.list_aliases()}
        return self._verify((address, target) not in aliases, f"Alias {address} removed", f"Alias {address} was still observed after deletion")

    def list_quotas(self) -> list[Quota]:
        return parse_quotas(self._read_config("dovecot-quotas.cf"))

    def set_quota(self, email: str, quota: str) -> MutationResult:
        result = self._docker_exec("setup", "quota", "set", email, quota)
        if result.exit_code != 0:
            return MutationResult(status="failed", detail=result.stderr.strip() or result.stdout.strip())

        quotas = {entry.email: entry.quota for entry in self.list_quotas()}
        observed_quota = quotas.get(email)
        return self._verify(
            observed_quota is not None and self._normalize_quota(observed_quota) == self._normalize_quota(quota),
            f"Quota set for {email}",
            f"Quota for {email} was not observed after update",
        )

    def delete_quota(self, email: str) -> MutationResult:
        result = self._docker_exec("setup", "quota", "del", email)
        if result.exit_code != 0:
            return MutationResult(status="failed", detail=result.stderr.strip() or result.stdout.strip())

        quotas = {entry.email for entry in self.list_quotas()}
        return self._verify(email not in quotas, f"Quota removed for {email}", f"Quota for {email} was still observed after deletion")

    def relay_state(self) -> RelayState:
        return parse_relay_state(
            self._read_config("postfix-relaymap.cf"),
            self._read_config("postfix-sasl-password.cf"),
        )

    def add_relay_domain(self, domain: str, host: str, port: int | None) -> MutationResult:
        command = ["setup", "relay", "add-domain", domain, host]
        if port is not None:
            command.append(str(port))

        result = self._docker_exec(*command)
        if result.exit_code != 0:
            return MutationResult(status="failed", detail=result.stderr.strip() or result.stdout.strip())

        domains = {(entry.domain, entry.host, entry.port) for entry in self.relay_state().domains}
        return self._verify((domain, host, port) in domains, f"Relay domain {domain} added", f"Relay domain {domain} was not observed after update")

    def exclude_relay_domain(self, domain: str) -> MutationResult:
        result = self._docker_exec("setup", "relay", "exclude-domain", domain)
        if result.exit_code != 0:
            return MutationResult(status="failed", detail=result.stderr.strip() or result.stdout.strip())

        domains = {entry.domain: entry for entry in self.relay_state().domains}
        entry = domains.get(domain)
        return self._verify(entry is not None and entry.excluded, f"Relay domain {domain} excluded", f"Relay exclusion for {domain} was not observed after update")

    def add_relay_auth(self, domain: str, username: str, password: str) -> MutationResult:
        result = self._docker_exec("setup", "relay", "add-auth", domain, username, password)
        if result.exit_code != 0:
            return MutationResult(status="failed", detail=result.stderr.strip() or result.stdout.strip())

        auth = {(entry.domain, entry.username) for entry in self.relay_state().auth}
        return self._verify((domain, username) in auth, f"Relay auth for {domain} added", f"Relay auth for {domain} was not observed after update")


def get_dms_service(settings: Settings = Depends(get_settings)) -> DmsService:
    return DmsService(settings=settings)
