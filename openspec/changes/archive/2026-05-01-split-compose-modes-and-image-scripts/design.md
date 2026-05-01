## Context

The repository currently has a single root `docker-compose.yml` that defines backend and frontend services with both `image` and `build` keys, bind mounts, and development commands. That shape is convenient for local iteration, but it does not cleanly separate three distinct operator needs:

- run the stack from existing images and allow Docker Compose to pull them
- run a local development stack with bind mounts and reload commands
- bring up an optional local mailserver alongside the admin services

The repository also has a single `scripts/build-images.sh` script that builds and pushes images in one step. The user now wants build and push responsibilities split into separate scripts while keeping image names compatible with the Compose workflow.

## Goals / Non-Goals

**Goals:**

- Make the base Compose file runtime-oriented so `docker compose up` can use or pull published images.
- Add a development overlay that restores local `build`, bind-mount, and hot-reload behavior.
- Add a full-stack overlay that introduces a mailserver service without making it part of the default stack.
- Split image build and image push workflows into separate scripts with shared configuration conventions.
- Keep the command surface explicit and documented so operators can choose runtime, dev, or full-stack behavior intentionally.

**Non-Goals:**

- Introduce CI/CD release automation.
- Add multi-platform manifest publishing.
- Redesign the application containers beyond what is needed to support the new Compose modes.
- Replace the integration-test mailserver fixture with a production-grade deployment template.

## Decisions

1. Use a base Compose file plus two overlays.

   The base `docker-compose.yml` will define the runtime-oriented `api` and `frontend` services with image references and shared environment. `docker-compose.dev.yml` will add local-development concerns such as `build`, bind mounts, and dev commands. `docker-compose.full.yml` will add the optional `mailserver` service and any related configuration adjustments.

   Alternatives considered:
   - A single Compose file with profiles for both dev/runtime switching and mailserver inclusion. Rejected because whole-service behavior changes are clearer with file overlays than with profile-gated fragments.
   - Separate unrelated Compose files for each mode. Rejected because duplicated service definitions would drift more easily than layered overrides.

2. Keep the base Compose file pull-friendly.

   The base file should define only image-based runtime behavior so `docker compose up` can start from existing local tags or pull from the configured registry when images are missing locally. This preserves a simple operator path and avoids defaulting to bind-mounted development containers in non-dev use cases.

   Alternatives considered:
   - Keep `build` in the base file. Rejected because it makes the default mode ambiguous and undermines the requirement that plain `docker compose up` be able to pull and run published images.

3. Split image responsibilities into `build-images.sh` and `push-images.sh`.

   `build-images.sh` will build backend and frontend images using the configured naming convention without pushing them. `push-images.sh` will push the already-tagged local images. Shared configuration loading and validation should be factored so both scripts use the same environment variables and clear prerequisite checks.

   Alternatives considered:
   - Keep a single build-and-push script. Rejected because it does not satisfy the requested operational separation.
   - Make the push script rebuild with `--push`. Rejected because that blurs responsibilities again and can duplicate work.

4. Reuse the existing image naming convention and `.env` contract.

   The existing registry, architecture, and tag variables should remain the public contract so Compose and scripts stay aligned. The documentation should explain when those values are required for pulling or pushing versus when local defaults are sufficient for development.

## Risks / Trade-offs

- Runtime and dev behavior diverge across overlays -> Keep the base file small, put only dev-specific settings in the dev overlay, and document the exact command matrix.
- Pushing local tags can fail if images were not built first -> Make `push-images.sh` validate local image presence and fail with a clear remediation message.
- Adding a root mailserver service may blur the boundary with the integration test fixture -> Keep the full-stack mailserver intentionally lightweight and scoped to local stack orchestration, not test harness behavior.
- More Compose files increase documentation burden -> Update `README.md` and `.env.example` together so the supported modes remain obvious.

## Migration Plan

1. Introduce the layered Compose files and keep image naming compatible with the existing environment variables.
2. Replace the current combined image publishing script with separate build and push scripts, preserving configuration keys.
3. Update docs and examples to point contributors to the correct Compose invocations for runtime, dev, and full-stack modes.
4. Verify the base runtime mode, dev overlay mode, and full-stack overlay mode through targeted tests or manual validation steps before removing references to the old workflow.

## Open Questions

- Whether the full-stack overlay should reuse exactly the same mailserver image settings as the integration fixture or expose a separate operator-facing variable set.
- Whether a convenience wrapper script for common Compose invocations is worthwhile after the layered files are introduced.
