## Why

The current runtime packaging publishes separate backend and frontend images, but the frontend image is effectively a Vite container shape rather than a simple production static asset delivery model. Moving production to a single image reduces deployment surface area, removes the cross-origin browser path in the default runtime, and aligns the frontend with the backend service that already owns operator authentication and API access.

## What Changes

- Replace the split production runtime image model with a single production image that builds the frontend and serves the resulting static assets from the FastAPI application.
- Keep the local development workflow split so contributors can continue using the Vite dev server and FastAPI reload behavior without forcing production packaging concerns into day-to-day iteration.
- Update the runtime Compose and image build/push workflows so production deployments reference a single application image instead of separate backend and frontend images.
- Add documented runtime behavior for serving the admin SPA, including static asset delivery and client-side route fallback from the FastAPI service.
- Reduce production cross-origin configuration by making the browser-facing runtime default to a same-origin `/api` path.

## Capabilities

### New Capabilities
- `admin-ui-delivery`: Runtime delivery of the built admin frontend from the FastAPI service, including static assets and SPA route fallback behavior.

### Modified Capabilities
- `deployment-validation`: Production image build, publish, and Compose runtime behavior changes from separate backend/frontend images to a single application image while preserving a split local development workflow.

## Impact

- `backend/` FastAPI application startup and runtime static-file handling
- `frontend/` production build configuration and API base URL assumptions
- Root Docker Compose files and image environment conventions
- `scripts/build-images.sh`, `scripts/push-images.sh`, and multi-architecture validation workflow
- Documentation and deployment-focused tests covering image naming and Compose behavior
