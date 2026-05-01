#!/usr/bin/env bash

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

fail() {
  printf 'error: %s\n' "$*" >&2
  exit 1
}

require_command() {
  command -v "$1" >/dev/null 2>&1 || fail "$1 is required but was not found in PATH."
}

restore_if_preexisting() {
  local var_name="$1"
  local marker_name="$2"
  local value_name="$3"

  if [[ "${!marker_name}" == "1" ]]; then
    export "$var_name=${!value_name}"
  fi
}

source_env_preserving_shell_overrides() {
  local registry_was_set=0
  local arch_was_set=0
  local tag_was_set=0
  local registry_value=""
  local arch_value=""
  local tag_value=""

  if [[ -v DMS_ADMIN_IMAGE_REGISTRY ]]; then
    registry_was_set=1
    registry_value="$DMS_ADMIN_IMAGE_REGISTRY"
  fi

  if [[ -v DMS_ADMIN_IMAGE_ARCH ]]; then
    arch_was_set=1
    arch_value="$DMS_ADMIN_IMAGE_ARCH"
  fi

  if [[ -v DMS_ADMIN_IMAGE_TAG ]]; then
    tag_was_set=1
    tag_value="$DMS_ADMIN_IMAGE_TAG"
  fi

  if [[ -f "$ROOT_DIR/.env" ]]; then
    set -a
    # shellcheck disable=SC1091
    . "$ROOT_DIR/.env"
    set +a
  fi

  restore_if_preexisting DMS_ADMIN_IMAGE_REGISTRY registry_was_set registry_value
  restore_if_preexisting DMS_ADMIN_IMAGE_ARCH arch_was_set arch_value
  restore_if_preexisting DMS_ADMIN_IMAGE_TAG tag_was_set tag_value
}

normalize_arch() {
  local arch="$1"
  arch="${arch#linux/}"

  case "$arch" in
    amd64 | arm64)
      printf '%s' "$arch"
      ;;
    *)
      fail "DMS_ADMIN_IMAGE_ARCH must be amd64 or arm64."
      ;;
  esac
}

image_ref() {
  local name="$1"
  printf '%s/%s:%s' "$DMS_ADMIN_IMAGE_REGISTRY" "$name" "$DMS_ADMIN_IMAGE_TAG"
}

require_image_configuration() {
  DMS_ADMIN_IMAGE_ARCH="$(normalize_arch "${DMS_ADMIN_IMAGE_ARCH:-amd64}")"
  DMS_ADMIN_IMAGE_TAG="${DMS_ADMIN_IMAGE_TAG:-latest}"

  [[ -n "${DMS_ADMIN_IMAGE_REGISTRY:-}" ]] || fail "DMS_ADMIN_IMAGE_REGISTRY is required, for example ghcr.io/example."
}

check_docker_access() {
  require_command docker
  docker info >/dev/null 2>&1 || fail "Docker is not running or is not accessible."
}

check_buildx_prerequisites() {
  check_docker_access
  docker buildx version >/dev/null 2>&1 || fail "Docker Buildx is required. Install or enable the Docker buildx plugin."
}

require_local_image() {
  local image="$1"

  docker image inspect "$image" >/dev/null 2>&1 || fail "Local image $image was not found. Run scripts/build-images.sh first."
}
