## Context

DMS Admin has separate backend and frontend Dockerfiles and an existing `scripts/validate-multiarch.sh` script that proves both images can build and test on `linux/amd64` and `linux/arm64`. Operators still need a release-oriented path that builds runtime images and pushes them to a configured registry for a chosen architecture, plus a Compose configuration that can run those published images.

The new workflow should fit the existing repository style: small Bash scripts in `scripts/`, documented `.env` keys, Docker Buildx for architecture-aware image builds, and Compose interpolation for local deployment configuration.

## Goals / Non-Goals

**Goals:**

- Provide one command that builds and pushes backend and frontend images.
- Configure registry, architecture, and tag through environment variables, with `.env` sourcing supported for local convenience.
- Make Docker Compose use configurable backend and frontend image references derived from the same registry, architecture, and tag values.
- Default tags to `latest` while allowing an override for future release/version tagging.
- Fail early with clear messages when required Docker tooling or registry configuration is missing.

**Non-Goals:**

- Create a CI release workflow.
- Add semantic versioning, Git SHA tagging, or multi-tag publishing in this change.
- Change application runtime Dockerfiles unless required by the publish script.
- Publish Docker Compose bundles.

## Decisions

1. Use Docker Buildx directly from a Bash script.

   Buildx already supports `--platform` and `--push`, and it is already required by the repository's multi-architecture validation script. This avoids adding a new release tool or dependency.

2. Use `DMS_ADMIN_IMAGE_REGISTRY`, `DMS_ADMIN_IMAGE_ARCH`, and `DMS_ADMIN_IMAGE_TAG`.

   The `DMS_ADMIN_` prefix matches existing configuration naming. `ARCH` matches the operator-facing concept and Compose image naming need. The script should translate `DMS_ADMIN_IMAGE_ARCH=amd64` into `linux/amd64` for Buildx. `DMS_ADMIN_IMAGE_TAG` defaults to `latest`.

3. Source root `.env` when present, without overriding already exported shell variables.

   This lets local operators store registry and platform defaults while still allowing CI or one-off shell invocations to override values.

4. Publish two architecture-specific image names under the configured registry.

   The expected images are `<registry>/dms-admin-backend-<arch>:<tag>` and `<registry>/dms-admin-frontend-<arch>:<tag>`. Including architecture in the repository name keeps single-architecture `latest` tags unambiguous and lets Compose select the correct published image from `.env`.

5. Make Compose image references configurable while preserving local builds.

   Each service should declare an `image` value interpolated from `DMS_ADMIN_IMAGE_REGISTRY`, `DMS_ADMIN_IMAGE_ARCH`, and `DMS_ADMIN_IMAGE_TAG`, while keeping the existing `build` blocks. This lets `docker compose up --build` continue to support local development and gives pushed images predictable names when Compose builds or runs services.

## Risks / Trade-offs

- Registry authentication is external to the script -> Document that users must run `docker login` or otherwise configure credentials before publishing.
- `latest` can be ambiguous -> Keep `latest` as the default requested behavior, but make the tag configurable from day one.
- Architecture-specific image repositories trade manifest simplicity for explicit image names -> Keep the convention documented and leave multi-platform manifests as a future enhancement.
- Sourcing `.env` in Bash can be fragile if values are not shell-compatible -> Document simple `KEY=value` usage and keep examples shell-safe.
- Compose interpolation needs defaults for local development -> Provide sensible defaults in `docker-compose.yml` and `.env.example` so local builds work without registry configuration.
