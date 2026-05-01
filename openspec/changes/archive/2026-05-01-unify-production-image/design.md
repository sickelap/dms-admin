## Context

The repository currently treats the backend and frontend as separate runtime services. The backend image runs FastAPI and includes Docker tooling for DMS interactions, while the frontend image is a Node/Vite container shape that is suitable for development but not ideal as a production runtime artifact. The root Compose files, image scripts, validation script, and README all assume two production images.

The target state is different in one important way: production should become a single deployable container that owns both the operator-facing web UI and the `/api` surface. At the same time, local development should remain split so the existing Vite and FastAPI reload loops stay fast and familiar.

This change cuts across multiple modules:

- frontend build and API base URL assumptions
- backend application startup and route/static handling
- Docker build pipeline and image naming conventions
- runtime Compose shape, scripts, tests, and documentation

## Goals / Non-Goals

**Goals:**

- Produce one production image that builds the frontend, embeds the built assets, and serves them from the FastAPI process.
- Preserve the existing split local development workflow with separate API and Vite services.
- Make the default browser runtime same-origin so the production path does not depend on cross-origin frontend-to-API requests.
- Keep the deployment contract explicit in Compose, image scripts, and documentation.

**Non-Goals:**

- Rework the admin UI itself beyond what is necessary for runtime delivery.
- Remove the existing development overlay or force Vite out of local workflows.
- Introduce a CDN, reverse proxy, or separate static asset service.
- Redesign the DMS integration model inside the backend container.

## Decisions

1. Use a multi-stage backend-owned production image.

   The production Docker build will compile the frontend assets in a Node build stage and copy the resulting build output into the backend runtime image. The backend image remains the only production image and continues to own the Docker tooling needed for DMS operations.

   Alternatives considered:
   - Keep separate production images and place a proxy in front. Rejected because it preserves extra deployment surface area and cross-origin complexity.
   - Introduce a dedicated static web server image such as Nginx. Rejected because the goal is a single deployable application image, not a different two-container split.

2. Keep development split from production packaging.

   The existing development overlay will remain responsible for local `uvicorn --reload` and `vite` workflows. Production image concerns will stay in the runtime image path and should not make the day-to-day loop depend on rebuilt frontend assets.

   Alternatives considered:
   - Collapse development into the single production image flow. Rejected because it would slow iteration and remove the value of the Vite dev server.

3. Serve the SPA from FastAPI with explicit route boundaries.

   FastAPI will continue to own `/api/*`. The built asset directory will be mounted under a static path such as `/assets/*`, and the app will return `index.html` for client-side routes that are not API endpoints or static asset paths.

   Alternatives considered:
   - Serve all files directly from `/` without a dedicated asset mount. Rejected because hashed static assets benefit from an explicit path boundary and clearer cache policy handling.
   - Replace `BrowserRouter` with hash-based routing. Rejected because route fallback at the server layer is straightforward and preserves cleaner URLs.

4. Make production frontend API calls same-origin by default.

   The frontend should resolve API requests to `/api` in the production-serving path. Development can still override the base URL or rely on the existing dev setup where the browser talks to the API at a different origin.

   Alternatives considered:
   - Keep absolute host-based defaults in the built frontend. Rejected because it creates avoidable environment-specific frontend configuration for the primary deployment path.

5. Replace the two-image runtime contract with one application image contract.

   The base runtime Compose file, build script, push script, and validation workflow will move from backend/frontend image references to a single application image reference. The dev overlay can continue to define separate build contexts for local workflows if that remains the simplest developer experience.

   Alternatives considered:
   - Maintain both the old and new production image contracts in parallel. Rejected because it increases operator ambiguity and doubles the validation/documentation burden.

## Risks / Trade-offs

- SPA fallback can unintentionally mask missing API or asset routes → Restrict fallback handling so it only applies to non-API HTML route requests.
- Production and development runtime paths diverge more clearly → Keep the split intentional, documented, and covered by tests around image scripts and route behavior.
- The backend image becomes a broader build artifact with frontend compilation involved → Use multi-stage builds so Node tooling is only present in the build stage, not the runtime layer.
- Changing image naming conventions may break existing local operator habits → Document the migration clearly and keep environment variables explicit and stable wherever possible.

## Migration Plan

1. Introduce the backend runtime support for serving built frontend assets and SPA fallback.
2. Replace the production Docker build path with a multi-stage single-image build that embeds the frontend build output.
3. Update the frontend API base URL defaults for the same-origin production path while preserving workable dev overrides.
4. Update the base Compose runtime path, image scripts, validation, and tests to use the single production image contract.
5. Update README and environment guidance to distinguish production runtime from split local development.
6. Roll back, if needed, by redeploying the previous separate backend/frontend image pair and restoring the previous Compose/image contract.

## Open Questions

- Whether the single image should keep the existing `backend` repository name for continuity or switch to a neutral application image name.
- Whether the frontend build output should live under a dedicated backend-owned directory in the repo or only exist as a copied Docker build artifact.
- Whether production should disable CORS entirely by default or keep it configurable for non-browser integrations and unusual deployments.
