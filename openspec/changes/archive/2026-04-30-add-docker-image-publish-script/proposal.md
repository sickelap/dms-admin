## Why

Operators need a repeatable way to publish and run DMS Admin backend and frontend container images for a chosen registry, architecture, and tag. The repository already validates multi-architecture Docker builds locally, but it does not provide a documented build-and-push workflow for distributable images or a Compose workflow that consumes those published images.

## What Changes

- Add a repository script that builds and pushes backend and frontend images with Docker Buildx.
- Allow the target registry, architecture, and tag to be configured with environment variables that may be supplied by the shell or a sourced `.env` file.
- Default image tags to `latest` while keeping the script contract open for future release, commit SHA, or version tags.
- Update Docker Compose so backend and frontend service image references are configurable from the same registry, architecture, and tag values.
- Document the image publishing and Compose image configuration usage.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `deployment-validation`: Adds a documented image publishing workflow and configurable Compose image references for architecture-specific backend and frontend container images.

## Impact

- Affected files are expected to include `scripts/`, `docker-compose.yml`, `.env.example`, and `README.md`.
- Requires Docker Buildx and an authenticated Docker registry session before pushing images.
- No application API, runtime behavior, database schema, or frontend user experience changes are expected.
