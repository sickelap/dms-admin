from collections import deque

import pytest

from dms_admin_api.config import Settings
from dms_admin_api.dms.models import CommandResult
from dms_admin_api.dms.runner import CommandRunner
from dms_admin_api.dms.service import DmsService


class FakeRunner:
    def __init__(self, results: list[CommandResult]) -> None:
        self.results = deque(results)
        self.commands: list[list[str]] = []

    def run(self, args: list[str]) -> CommandResult:
        self.commands.append(args)
        return self.results.popleft()


def build_service(results: list[CommandResult]) -> tuple[DmsService, FakeRunner]:
    runner = FakeRunner(results)
    settings = Settings(session_secret="secret")
    return DmsService(settings=settings, runner=runner), runner


def test_create_account_uses_setup_command_and_verifies_from_accounts_file() -> None:
    service, runner = build_service(
        [
            CommandResult(stdout="", stderr="", exit_code=0),
            CommandResult(stdout="hello@example.com|hash\n", stderr="", exit_code=0),
        ]
    )

    result = service.create_account("hello@example.com", "password")

    assert result.model_dump() == {"status": "applied", "detail": "Account hello@example.com created"}
    assert runner.commands[0] == [
        "docker",
        "exec",
        "mailserver",
        "setup",
        "email",
        "add",
        "hello@example.com",
        "password",
    ]


def test_delete_account_uses_forced_delete_and_verifies_absence() -> None:
    service, runner = build_service(
        [
            CommandResult(stdout="", stderr="", exit_code=0),
            CommandResult(stdout="", stderr="", exit_code=0),
        ]
    )

    result = service.delete_account("hello@example.com")

    assert result.model_dump() == {"status": "applied", "detail": "Account hello@example.com removed"}
    assert runner.commands[0][-4:] == ["email", "del", "-y", "hello@example.com"]


def test_failed_command_returns_failed_status() -> None:
    service, _ = build_service([CommandResult(stdout="", stderr="bad request", exit_code=1)])

    result = service.create_alias("postmaster@example.com", "hello@example.com")

    assert result.model_dump() == {"status": "failed", "detail": "bad request"}


def test_set_quota_verifies_updated_quota_file() -> None:
    service, _ = build_service(
        [
            CommandResult(stdout="", stderr="", exit_code=0),
            CommandResult(stdout="hello@example.com:10 M\n", stderr="", exit_code=0),
        ]
    )

    result = service.set_quota("hello@example.com", "10 M")

    assert result.model_dump() == {"status": "applied", "detail": "Quota set for hello@example.com"}


def test_add_relay_domain_verifies_relay_map() -> None:
    service, _ = build_service(
        [
            CommandResult(stdout="", stderr="", exit_code=0),
            CommandResult(stdout="@example.com [smtp.example.com]:587\n", stderr="", exit_code=0),
            CommandResult(stdout="", stderr="", exit_code=0),
        ]
    )

    result = service.add_relay_domain("example.com", "smtp.example.com", 587)

    assert result.model_dump() == {"status": "applied", "detail": "Relay domain example.com added"}


def test_runner_returns_failed_result_when_executable_is_missing() -> None:
    result = CommandRunner().run(["/definitely/missing/binary"])

    assert result.exit_code == 127
    assert result.stdout == ""
    assert "No such file" in result.stderr


def test_runner_falls_back_to_docker_socket_for_docker_exec(monkeypatch: pytest.MonkeyPatch) -> None:
    runner = CommandRunner()

    def raise_os_error(args: list[str], **_: object) -> CommandResult:
        raise FileNotFoundError("docker missing")

    monkeypatch.setattr("subprocess.run", raise_os_error)
    monkeypatch.setattr(
        runner,
        "_docker_exec_via_socket",
        lambda args: CommandResult(stdout="ok", stderr="", exit_code=0),
    )

    result = runner.run(["docker", "exec", "mailserver", "setup", "help"])

    assert result.model_dump() == {"stdout": "ok", "stderr": "", "exit_code": 0}
