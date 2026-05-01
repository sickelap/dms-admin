## Why

The current root Compose workflow blends local development behavior, image build configuration, and runtime image selection into one service definition. That makes it harder to run the stack predictably in different modes and prevents the repository from cleanly supporting a full stack with an optional local mailserver.

## What Changes

- Split the root Docker Compose configuration into a base runtime file plus overlays for development behavior and the optional full stack.
- Add a root Compose mailserver service that is only included when the full-stack overlay is used.
- Separate image build and image push responsibilities into distinct repository scripts.
- Keep image references configurable from environment values so `docker compose up` can pull published images when they are not already present locally.
- Update local documentation and environment examples to describe the new Compose command matrix and image workflow.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `deployment-validation`: Compose and image publication workflows must support separate runtime, development, and optional full-stack modes, plus distinct build and push scripts.

## Impact

- Root Compose files and related local deployment workflow
- `scripts/` image build and publish helpers
- Root `.env.example` and `README.md`
- Tests that validate Compose command resolution and image publishing behavior
