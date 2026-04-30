from fastapi.testclient import TestClient

from dms_admin_api.dms.models import Account, Alias, MutationResult, Quota, RelayAuth, RelayDomain, RelayState
from dms_admin_api.dms.service import get_dms_service
from dms_admin_api.main import create_app


class StubDmsService:
    def connectivity(self) -> bool:
        return True

    def list_accounts(self) -> list[Account]:
        return [Account(email="hello@example.com")]

    def create_account(self, email: str, password: str) -> MutationResult:
        return MutationResult(status="applied", detail=f"Account {email} created")

    def update_account_password(self, email: str, password: str) -> MutationResult:
        return MutationResult(status="applied", detail=f"Password updated for {email}")

    def delete_account(self, email: str) -> MutationResult:
        return MutationResult(status="applied", detail=f"Account {email} removed")

    def list_aliases(self) -> list[Alias]:
        return [Alias(address="postmaster@example.com", target="hello@example.com")]

    def create_alias(self, address: str, target: str) -> MutationResult:
        return MutationResult(status="applied", detail=f"Alias {address} created")

    def delete_alias(self, address: str, target: str) -> MutationResult:
        return MutationResult(status="applied", detail=f"Alias {address} removed")

    def list_quotas(self) -> list[Quota]:
        return [Quota(email="hello@example.com", quota="5 G")]

    def set_quota(self, email: str, quota: str) -> MutationResult:
        return MutationResult(status="applied", detail=f"Quota set for {email}")

    def delete_quota(self, email: str) -> MutationResult:
        return MutationResult(status="applied", detail=f"Quota removed for {email}")

    def relay_state(self) -> RelayState:
        return RelayState(
            domains=[RelayDomain(domain="example.com", host="smtp.example.com", port=587)],
            auth=[RelayAuth(domain="example.com", username="relay-user")],
        )

    def add_relay_domain(self, domain: str, host: str, port: int | None) -> MutationResult:
        return MutationResult(status="applied", detail=f"Relay domain {domain} added")

    def exclude_relay_domain(self, domain: str) -> MutationResult:
        return MutationResult(status="applied", detail=f"Relay domain {domain} excluded")

    def add_relay_auth(self, domain: str, username: str, password: str) -> MutationResult:
        return MutationResult(status="applied", detail=f"Relay auth for {domain} added")


class UnreachableDmsService(StubDmsService):
    def connectivity(self) -> bool:
        return False


def build_client() -> TestClient:
    app = create_app()
    app.dependency_overrides[get_dms_service] = lambda: StubDmsService()
    client = TestClient(app)
    client.post("/api/auth/login", json={"username": "admin", "password": "admin"})
    return client


def test_accounts_endpoint_returns_accounts() -> None:
    client = build_client()

    response = client.get("/api/accounts")

    assert response.status_code == 200
    assert response.json() == [{"email": "hello@example.com"}]


def test_aliases_endpoint_returns_aliases() -> None:
    client = build_client()

    response = client.get("/api/aliases")

    assert response.status_code == 200
    assert response.json() == [{"address": "postmaster@example.com", "target": "hello@example.com"}]


def test_system_endpoint_returns_fresh_state() -> None:
    client = build_client()

    response = client.get("/api/system/status")

    assert response.status_code == 200
    assert response.json() == {"dms_container_name": "mailserver", "dms_reachable": True}


def test_system_endpoint_reports_unreachable_dms() -> None:
    app = create_app()
    app.dependency_overrides[get_dms_service] = lambda: UnreachableDmsService()
    client = TestClient(app)
    client.post("/api/auth/login", json={"username": "admin", "password": "admin"})

    response = client.get("/api/system/status")

    assert response.status_code == 200
    assert response.json() == {"dms_container_name": "mailserver", "dms_reachable": False}
