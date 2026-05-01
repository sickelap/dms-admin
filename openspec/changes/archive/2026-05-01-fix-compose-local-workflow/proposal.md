## Why

The documented local Docker Compose workflows do not currently work as described. A fresh `docker compose up` fails because the default image reference does not resolve, and the documented dev frontend URL is not reachable because the dev overlay does not publish the frontend port.

## What Changes

- Align the base Compose workflow with an actually usable local startup path instead of a broken default image pull.
- Publish the frontend development port in the dev Compose overlay so the documented local Vite URL is reachable from the host.
- Preserve the optional full-stack Compose workflow so the local mailserver path still works after the compose changes.
- Update Compose-related documentation so the supported commands, defaults, and expectations match the real stack behavior.
- Remove avoidable Compose configuration noise that obscures real startup issues.

## Capabilities

### New Capabilities

### Modified Capabilities
- `deployment-validation`: local Compose startup and development access requirements will be updated so the documented base and dev workflows reflect the actual supported behavior.

## Impact

- `docker-compose.yml`
- `docker-compose.dev.yml`
- `README.md`
- Local Docker Compose startup behavior for contributors
