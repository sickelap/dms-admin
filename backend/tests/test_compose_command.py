import subprocess

import pytest

from tests.integration.compose_command import resolve_compose_command


def test_resolve_compose_command_prefers_docker_compose_plugin() -> None:
    def which(command: str) -> str | None:
        return f"/usr/bin/{command}"

    def run(*_args: object, **_kwargs: object) -> subprocess.CompletedProcess:
        return subprocess.CompletedProcess(args=[], returncode=0)

    assert resolve_compose_command(run=run, which=which) == ["docker", "compose"]


def test_resolve_compose_command_falls_back_to_legacy_binary() -> None:
    def which(command: str) -> str | None:
        return "/usr/bin/docker-compose" if command == "docker-compose" else None

    assert resolve_compose_command(which=which) == ["docker-compose"]


def test_resolve_compose_command_uses_legacy_binary_when_plugin_fails() -> None:
    def which(command: str) -> str | None:
        return f"/usr/bin/{command}"

    def run(*_args: object, **_kwargs: object) -> subprocess.CompletedProcess:
        return subprocess.CompletedProcess(args=[], returncode=1)

    assert resolve_compose_command(run=run, which=which) == ["docker-compose"]


def test_resolve_compose_command_raises_when_no_compose_is_available() -> None:
    def which(_command: str) -> str | None:
        return None

    with pytest.raises(RuntimeError, match="Docker Compose is required"):
        resolve_compose_command(which=which)
