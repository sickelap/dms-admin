## Context

The repository has a root compose file for running the admin API and frontend, plus an integration-test compose file for starting a local Docker Mail Server container. The root compose file currently relies on inline environment interpolation and the documentation assumes the modern `docker compose` plugin. The integration test helper also hardcodes `docker compose`, which excludes environments that still provide only the legacy `docker-compose` binary.

The project ships backend and frontend Dockerfiles, but there is no single workflow that proves those images build and their test suites pass for both `linux/amd64` and `linux/arm64`.

## Goals / Non-Goals

**Goals:**

- Make local compose configuration pick up documented values from `.env`.
- Keep compose files compatible with older `docker-compose` installations.
- Let integration tests run with either `docker compose` or `docker-compose`.
- Provide one script that validates backend and frontend build/test behavior for `linux/amd64` and `linux/arm64`.
- Document the expected environment and validation workflows.

**Non-Goals:**

- Publishing multi-architecture images to a registry.
- Changing application runtime behavior or API contracts.
- Replacing the existing unit and integration test frameworks.
- Requiring Docker Mail Server integration tests to run as part of every multi-architecture validation by default.

## Decisions

### Use Compose `.env` interpolation for local values

The root compose file will rely on Compose's built-in root `.env` interpolation for supported API and frontend settings and keep existing `${VAR:-default}` defaults. This gives contributors a single documented file for local overrides while preserving the current zero-configuration path, including older Compose installations that fail when an explicitly referenced `env_file` is missing.

Alternative considered: require all values in shell environment. That keeps compose simpler, but makes local setup less explicit and harder to reproduce.

### Preserve compatibility with legacy compose syntax

Compose files will include an explicit compose file version that older `docker-compose` versions understand. The service definitions should avoid newer compose features when a simpler equivalent is enough.

Alternative considered: support only the modern Docker Compose plugin. That is simpler, but does not meet the compatibility requirement.

### Detect compose command at runtime in tests

The integration helper will resolve a compose command once, preferring `docker compose` when available and falling back to `docker-compose`. This keeps the test code portable without forcing users to install both.

Alternative considered: make users set a `COMPOSE_COMMAND` environment variable. That is flexible, but adds friction for the common case.

### Validate one platform at a time with Buildx

The multi-architecture script will loop over `linux/amd64` and `linux/arm64`, build platform-specific backend and frontend images with Docker Buildx, then run the relevant tests inside those images. Running one platform at a time avoids the limitations of loading multi-platform image indexes into the local Docker engine.

Alternative considered: use a single multi-platform build command. That is useful for publishing, but less practical for local test execution because the resulting image cannot always be loaded and run locally in one step.

## Risks / Trade-offs

- Cross-architecture test execution depends on local Docker/QEMU support -> The script should fail early with a clear prerequisite message when the target platform cannot be run.
- Multi-architecture validation will be slower than normal unit tests -> Keep it as an explicit script rather than folding it into the default local test commands.
- Legacy compose compatibility can constrain future compose features -> Prefer simple service definitions unless a newer feature has a clear benefit.
- `.env` values can accidentally contain secrets -> Provide `.env.example` and document that real `.env` files are local-only.
