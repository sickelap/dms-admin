#!/usr/bin/env bash
set -euo pipefail

# shellcheck disable=SC1091
. "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/image-common.sh"

build_image() {
  local image

  image="$(image_ref "dms-admin")"

  printf '\n==> Building %s\n' "$image"

  docker buildx build \
    --platform "linux/$DMS_ADMIN_IMAGE_ARCH" \
    --load \
    -t "$image" \
    -f "$ROOT_DIR/backend/Dockerfile" \
    "$ROOT_DIR"
}

source_env_preserving_shell_overrides
require_image_configuration
check_buildx_prerequisites

build_image

printf '\nImages built successfully.\n'
