#!/usr/bin/env bash
set -euo pipefail

# shellcheck disable=SC1091
. "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/image-common.sh"

build_image() {
  local name="$1"
  local context_dir="$2"
  local image

  image="$(image_ref "$name")"

  printf '\n==> Building %s\n' "$image"

  docker buildx build \
    --platform "linux/$DMS_ADMIN_IMAGE_ARCH" \
    --load \
    -t "$image" \
    "$context_dir"
}

source_env_preserving_shell_overrides
require_image_configuration
check_buildx_prerequisites

build_image "backend" "$ROOT_DIR/backend"
build_image "frontend" "$ROOT_DIR/frontend"

printf '\nImages built successfully.\n'
