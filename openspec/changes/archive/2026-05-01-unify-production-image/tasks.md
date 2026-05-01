## 1. Backend Runtime Delivery

- [x] 1.1 Add backend runtime support for serving bundled frontend static assets and returning `index.html` for non-API client routes.
- [x] 1.2 Make production-safe API/static route boundaries explicit so `/api` requests are not shadowed by SPA fallback behavior.
- [x] 1.3 Add backend tests that cover root document serving, static asset serving, SPA route fallback, and `/api` route preservation.

## 2. Production Image Build

- [x] 2.1 Replace the current production Docker build path with a multi-stage build that compiles the frontend and copies the build output into the backend runtime image.
- [x] 2.2 Update frontend production API base URL behavior to default to the same-origin `/api` path while preserving workable local development overrides.
- [x] 2.3 Validate that the single production image still includes the backend runtime prerequisites needed for DMS command execution.

## 3. Compose And Image Workflow

- [x] 3.1 Update the base runtime Compose configuration to reference a single production application image.
- [x] 3.2 Preserve the split local development workflow in the development overlay so API reload and Vite dev server behavior remain available.
- [x] 3.3 Update image build, push, and validation scripts plus their tests to use the single production image contract.

## 4. Documentation And Rollout

- [x] 4.1 Update README and environment variable documentation to describe the single production image workflow and the split local development workflow.
- [x] 4.2 Add or update validation steps that demonstrate the new production runtime path and the unchanged local development path.
