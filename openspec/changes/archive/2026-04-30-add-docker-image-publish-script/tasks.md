## 1. Publish Script

- [x] 1.1 Add `scripts/build-images.sh` with Docker and Buildx prerequisite checks.
- [x] 1.2 Source root `.env` when present while preserving already exported environment variables.
- [x] 1.3 Require `DMS_ADMIN_IMAGE_REGISTRY`, default `DMS_ADMIN_IMAGE_ARCH` and `DMS_ADMIN_IMAGE_TAG`, and print clear configuration errors.
- [x] 1.4 Build and push backend and frontend runtime images with architecture-specific names using `docker buildx build --platform linux/<arch> --push`.

## 2. Compose Configuration

- [x] 2.1 Update `docker-compose.yml` so backend and frontend services use image names derived from `DMS_ADMIN_IMAGE_REGISTRY`, `DMS_ADMIN_IMAGE_ARCH`, and `DMS_ADMIN_IMAGE_TAG`.
- [x] 2.2 Keep existing build blocks available so Compose remains usable for local development builds.

## 3. Documentation

- [x] 3.1 Add image publishing and Compose image variables to `.env.example`.
- [x] 3.2 Document script usage, required Docker registry authentication, Compose image configuration, defaults, and example commands in `README.md`.

## 4. Verification

- [x] 4.1 Run shell syntax validation for the new script.
- [x] 4.2 Run Docker Compose config validation to confirm image interpolation works.
- [x] 4.3 Run OpenSpec validation/status for `add-docker-image-publish-script`.
