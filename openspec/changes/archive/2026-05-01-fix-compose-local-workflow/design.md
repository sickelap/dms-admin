## Context

The repository exposes three layered Compose files, but the practical local workflows are inconsistent. The base stack currently points at a published backend image that may not exist for contributors, while the development overlay builds locally but does not publish the frontend port even though the documentation says the Vite app is reachable from the host.

This change crosses Compose configuration and contributor-facing documentation. The goal is to make the documented commands trustworthy again without expanding scope into larger container strategy changes.

## Goals / Non-Goals

**Goals:**
- Ensure the supported local Compose workflows start in a way that matches repository documentation.
- Ensure the development frontend is reachable from the host on the documented port.
- Ensure the optional full-stack workflow still works after the local compose fixes.
- Clarify which workflow depends on published images versus local builds.
- Remove avoidable Compose warnings that distract from real startup problems.

**Non-Goals:**
- Redesign the overall image publishing strategy.
- Change the optional mailserver workflow beyond keeping it compatible with the corrected local stack.
- Introduce new deployment environments or additional compose overlays.

## Decisions

### Treat the local development overlay as the primary contributor workflow
The repository already contains local build and bind-mount behavior in `docker-compose.dev.yml`, so the smallest safe change is to make the documentation and Compose expectations center on that path for contributors.

Alternative considered:
- Make the base `docker compose up` path self-sufficient for local development. Rejected because it blurs the runtime-vs-development split and likely requires broader image and service changes than needed for this fix.

### Publish the frontend dev port from the dev overlay
The frontend container starts Vite correctly, but without a `ports` mapping the documented host URL is false. Adding a published port is the minimal change that makes the current design usable.

Alternative considered:
- Remove the documented localhost frontend URL and treat the dev UI as container-only. Rejected because it makes the local workflow materially worse and conflicts with the existing `.env` surface.

### Keep image-backed base Compose behavior explicit
The base stack should be documented as a published-image workflow only if that remains intentional. If it cannot be relied on in local setups, the docs should stop presenting it as the default contributor entrypoint.

Alternative considered:
- Leave the base command documented as-is and rely on contributors to build the image first. Rejected because it produces a broken first-run experience and hides the prerequisite.

### Remove the obsolete Compose `version` field
Current Compose ignores the field and warns on every run. Removing it is a low-risk cleanup that improves signal during startup investigation.

Alternative considered:
- Leave the warning in place. Rejected because it creates noise without value.

## Risks / Trade-offs

- [The base image-backed workflow may still be needed by some operators] → Keep the fix scoped to clarifying when that workflow is valid rather than removing it outright without review.
- [Publishing the frontend port could conflict with an already-used host port] → Continue using the existing environment-configurable frontend port so operators can override it.
- [Documentation-only fixes could mask unresolved compose behavior gaps] → Pair README changes with Compose config changes and verification steps so the documented workflow is exercised end to end.
