#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PLATFORMS=("linux/amd64" "linux/arm64")

fail() {
  printf 'error: %s\n' "$*" >&2
  exit 1
}

require_command() {
  command -v "$1" >/dev/null 2>&1 || fail "$1 is required but was not found in PATH."
}

platform_tag() {
  printf '%s' "$1" | tr '/:' '--'
}

check_docker_prerequisites() {
  require_command docker
  docker info >/dev/null 2>&1 || fail "Docker is not running or is not accessible."
  docker buildx version >/dev/null 2>&1 || fail "Docker Buildx is required. Install or enable the Docker buildx plugin."
}

check_platform_can_run() {
  local platform="$1"

  docker run --rm --platform "$platform" alpine:3.20 uname -m >/dev/null 2>&1 \
    || fail "Docker cannot run containers for $platform. Enable platform emulation, for example with Docker Desktop or binfmt/QEMU support."
}

build_and_test_backend() {
  local platform="$1"
  local tag_suffix
  tag_suffix="$(platform_tag "$platform")"
  local runtime_image="dms-admin-backend:${tag_suffix}"
  local test_image="dms-admin-backend-test:${tag_suffix}"
  local frontend_test_image="dms-admin-frontend-test:${tag_suffix}"

  docker buildx build \
    --platform "$platform" \
    --target runtime \
    --load \
    -t "$runtime_image" \
    -f "$ROOT_DIR/backend/Dockerfile" \
    "$ROOT_DIR"

  docker buildx build \
    --platform "$platform" \
    --target test \
    --load \
    -t "$test_image" \
    -f "$ROOT_DIR/backend/Dockerfile" \
    "$ROOT_DIR"

  docker run --rm --platform "$platform" "$test_image"

  docker buildx build \
    --platform "$platform" \
    --target frontend-test \
    --load \
    -t "$frontend_test_image" \
    -f "$ROOT_DIR/backend/Dockerfile" \
    "$ROOT_DIR"

  docker run --rm --platform "$platform" "$frontend_test_image"
}

check_docker_prerequisites

for platform in "${PLATFORMS[@]}"; do
  printf '\n==> Validating %s\n' "$platform"
  check_platform_can_run "$platform"
  build_and_test_backend "$platform"
done

printf '\nMulti-architecture validation completed successfully.\n'
