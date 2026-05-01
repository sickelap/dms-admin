import subprocess
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[2]


def read_root_file(path: str) -> str:
    return (ROOT_DIR / path).read_text()


def test_base_compose_is_runtime_oriented() -> None:
    compose = read_root_file("docker-compose.yml")

    assert "image: ${DMS_ADMIN_IMAGE_REGISTRY:-dms-admin}/backend:${DMS_ADMIN_IMAGE_TAG:-latest}" in compose
    assert "image: ${DMS_ADMIN_IMAGE_REGISTRY:-dms-admin}/frontend:${DMS_ADMIN_IMAGE_TAG:-latest}" in compose
    assert "build:" not in compose
    assert "mailserver:" not in compose


def test_dev_compose_restores_local_build_and_reload_settings() -> None:
    compose = read_root_file("docker-compose.dev.yml")

    assert "context: ./backend" in compose
    assert "context: ./frontend" in compose
    assert "/var/run/docker.sock:/var/run/docker.sock" in compose
    assert "--reload" in compose
    assert '"npm", "run", "dev"' in compose


def test_full_compose_adds_optional_mailserver_stack() -> None:
    compose = read_root_file("docker-compose.full.yml")

    assert "mailserver:" in compose
    assert "container_name: ${DMS_ADMIN_DMS_CONTAINER_NAME:-mailserver}" in compose
    assert "DMS_ADMIN_MAILSERVER_IMAGE" in compose
    assert "dms-mail-config:/tmp/docker-mailserver" in compose


def test_image_scripts_have_valid_bash_syntax() -> None:
    for script_name in ("scripts/image-common.sh", "scripts/build-images.sh", "scripts/push-images.sh"):
        subprocess.run(["bash", "-n", str(ROOT_DIR / script_name)], check=True)


def test_build_and_push_scripts_have_separate_responsibilities() -> None:
    build_script = read_root_file("scripts/build-images.sh")
    push_script = read_root_file("scripts/push-images.sh")

    assert "--load" in build_script
    assert "--push" not in build_script
    assert "docker push" in push_script
    assert "Run scripts/build-images.sh first." in read_root_file("scripts/image-common.sh")
