from dms_admin_api.dms.models import Account, Alias, Quota, RelayAuth, RelayDomain, RelayState


def _non_comment_lines(content: str) -> list[str]:
    lines: list[str] = []
    for raw_line in content.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        lines.append(line)
    return lines


def parse_accounts(content: str) -> list[Account]:
    accounts: list[Account] = []
    for line in _non_comment_lines(content):
        email, *_ = line.split("|", maxsplit=1)
        accounts.append(Account(email=email.strip()))
    return accounts


def parse_aliases(content: str) -> list[Alias]:
    aliases: list[Alias] = []
    for line in _non_comment_lines(content):
        parts = line.split()
        if len(parts) < 2:
            continue
        aliases.append(Alias(address=parts[0], target=" ".join(parts[1:])))
    return aliases


def parse_quotas(content: str) -> list[Quota]:
    quotas: list[Quota] = []
    for line in _non_comment_lines(content):
        email, quota = line.split(":", maxsplit=1)
        quotas.append(Quota(email=email.strip(), quota=quota.strip()))
    return quotas


def parse_relay_domains(content: str) -> list[RelayDomain]:
    mappings: list[RelayDomain] = []
    for line in _non_comment_lines(content):
        parts = line.split()
        domain = parts[0].removeprefix("@")
        if len(parts) == 1:
            mappings.append(RelayDomain(domain=domain, excluded=True))
            continue

        destination = parts[1]
        if destination.startswith("[") and "]:" in destination:
            host_port = destination[1:]
            host, port = host_port.split("]:", maxsplit=1)
            mappings.append(RelayDomain(domain=domain, host=host, port=int(port)))
            continue

        mappings.append(RelayDomain(domain=domain, host=destination))
    return mappings


def parse_relay_auth(content: str) -> list[RelayAuth]:
    auth_entries: list[RelayAuth] = []
    for line in _non_comment_lines(content):
        parts = line.split()
        if len(parts) < 2:
            continue
        username, *_ = parts[1].split(":", maxsplit=1)
        auth_entries.append(RelayAuth(domain=parts[0].removeprefix("@"), username=username))
    return auth_entries


def parse_relay_state(domain_content: str, auth_content: str) -> RelayState:
    return RelayState(domains=parse_relay_domains(domain_content), auth=parse_relay_auth(auth_content))
