from dms_admin_api.dms.parsers import (
    parse_accounts,
    parse_aliases,
    parse_quotas,
    parse_relay_auth,
    parse_relay_domains,
)


def test_parse_accounts_returns_email_only() -> None:
    accounts = parse_accounts("hello@example.com|hash\nworld@example.com|hash2\n")

    assert [account.email for account in accounts] == ["hello@example.com", "world@example.com"]


def test_parse_aliases_returns_address_and_target() -> None:
    aliases = parse_aliases(
        "postmaster@example.com hello@example.com\nsales@example.com external@example.net\n"
    )

    assert [(alias.address, alias.target) for alias in aliases] == [
        ("postmaster@example.com", "hello@example.com"),
        ("sales@example.com", "external@example.net"),
    ]


def test_parse_quotas_returns_email_and_quota() -> None:
    quotas = parse_quotas("hello@example.com:5 G\n")

    assert [(quota.email, quota.quota) for quota in quotas] == [("hello@example.com", "5 G")]


def test_parse_relay_domains_supports_mapped_and_excluded_entries() -> None:
    entries = parse_relay_domains("@example.com [smtp.example.com]:587\n@internal.example.com\n")

    assert entries[0].model_dump() == {
        "domain": "example.com",
        "host": "smtp.example.com",
        "port": 587,
        "excluded": False,
    }
    assert entries[1].model_dump() == {
        "domain": "internal.example.com",
        "host": None,
        "port": None,
        "excluded": True,
    }


def test_parse_relay_auth_returns_domain_and_username_only() -> None:
    entries = parse_relay_auth("@example.com relay-user:super-secret\n")

    assert [entry.model_dump() for entry in entries] == [
        {"domain": "example.com", "username": "relay-user"}
    ]
