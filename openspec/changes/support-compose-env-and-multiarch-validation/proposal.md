## Why

Local deployment and integration validation currently rely on implicit environment handling and the modern `docker compose` command. Operators and contributors need a clearer, more portable setup that works with `.env` files, older `docker-compose` installations, and both common container architectures.

## What Changes

- Load admin application environment values from a root `.env` file while preserving safe local defaults for development.
- Update compose configuration so it remains usable with older `docker-compose` versions.
- Make the DMS integration test harness work with both `docker compose` and `docker-compose`.
- Add a script that automates backend and frontend image build and test validation for `linux/amd64` and `linux/arm64`.
- Document the environment file, compose compatibility, and multi-architecture validation workflow.

## Capabilities

### New Capabilities

- `deployment-validation`: Covers local compose configuration, environment file handling, compose command compatibility, and multi-architecture build/test validation.

### Modified Capabilities

None.

## Impact

- Root compose configuration and local environment examples.
- DMS integration test compose invocation.
- New repository script for multi-architecture validation.
- README setup and validation documentation.
