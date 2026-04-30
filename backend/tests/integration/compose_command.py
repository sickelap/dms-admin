import shutil
import subprocess
from collections.abc import Callable, Sequence

ComposeCommand = Sequence[str]
RunCommand = Callable[..., subprocess.CompletedProcess]
WhichCommand = Callable[[str], str | None]


def resolve_compose_command(
    *,
    run: RunCommand = subprocess.run,
    which: WhichCommand = shutil.which,
) -> ComposeCommand:
    if which("docker"):
        docker_compose = ["docker", "compose"]
        result = run(
            [*docker_compose, "version"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )
        if result.returncode == 0:
            return docker_compose

    if which("docker-compose"):
        return ["docker-compose"]

    raise RuntimeError("Docker Compose is required: install `docker compose` or `docker-compose`.")
