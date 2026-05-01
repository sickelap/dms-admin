#!/usr/bin/env bash
set -euo pipefail

# shellcheck disable=SC1091
. "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/image-common.sh"

push_image() {
  local image="$1"

  printf '\n==> Pushing %s\n' "$image"
  docker push "$image"
}

source_env_preserving_shell_overrides
require_image_configuration
check_docker_access

backend_image="$(image_ref "dms-admin")"

require_local_image "$backend_image"

push_image "$backend_image"

printf '\nImages pushed successfully.\n'
