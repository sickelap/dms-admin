import os
import shutil
import subprocess
import time
from pathlib import Path

import pytest

from dms_admin_api.config import Settings
from dms_admin_api.dms.service import DmsService

from .compose_command import resolve_compose_command

COMPOSE_FILE = Path(__file__).with_name("compose.yaml")
COMPOSE_DIR = COMPOSE_FILE.parent
DOCKER_DATA_DIR = COMPOSE_DIR / "docker-data" / "dms"

pytestmark = pytest.mark.skipif(
    os.getenv("RUN_DMS_INTEGRATION") != "1",
    reason="Set RUN_DMS_INTEGRATION=1 to run local DMS container integration tests",
)


def _compose(*args: str) -> None:
    subprocess.run(
        [*resolve_compose_command(), "-f", str(COMPOSE_FILE), *args],
        cwd=COMPOSE_DIR,
        check=True,
    )


def _wait_until_ready(service: DmsService) -> None:
    deadline = time.time() + 180
    while time.time() < deadline:
        if service.connectivity():
            return
        time.sleep(5)
    raise TimeoutError("DMS container did not become ready within 180 seconds")


def _reset_docker_data() -> None:
    if DOCKER_DATA_DIR.exists():
        shutil.rmtree(DOCKER_DATA_DIR)

    for relative_path in ("config", "mail-data", "mail-state", "logs"):
        (DOCKER_DATA_DIR / relative_path).mkdir(parents=True, exist_ok=True)


@pytest.fixture(scope="module")
def dms_service() -> DmsService:
    _reset_docker_data()
    _compose("up", "-d")
    service = DmsService(
        settings=Settings(
            dms_container_name="dms-admin-test-mailserver",
            session_secret="integration-secret",
        )
    )
    _wait_until_ready(service)
    try:
        yield service
    finally:
        _compose("down", "-v")


def test_account_alias_and_quota_flows_against_local_dms(dms_service: DmsService) -> None:
    email = "hello@example.test"
    alias = "postmaster@example.test"

    create_result = dms_service.create_account(email=email, password="example-password")
    assert create_result.status == "applied", create_result.detail

    accounts = dms_service.list_accounts()
    assert any(account.email == email for account in accounts)

    alias_result = dms_service.create_alias(address=alias, target=email)
    assert alias_result.status == "applied", alias_result.detail

    aliases = dms_service.list_aliases()
    assert any(entry.address == alias and entry.target == email for entry in aliases)

    quota_result = dms_service.set_quota(email=email, quota="10M")
    assert quota_result.status == "applied", quota_result.detail

    quotas = dms_service.list_quotas()
    assert any(entry.email == email and entry.quota.replace(" ", "") == "10M" for entry in quotas)
