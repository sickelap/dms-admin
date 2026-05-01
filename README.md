# DMS Admin

Single-server admin interface for Docker Mail Server.

## Layout

- `backend/`: FastAPI API
- `frontend/`: React UI
- `openspec/`: proposal, design, specs, and task tracking

## Local development

1. Copy `.env.example` to `.env`.
2. Choose a workflow:
   - Local development with an existing DMS container:
     `docker compose -f docker-compose.yml -f docker-compose.dev.yml up --build`
   - Local development with the optional local mailserver:
     `docker compose -f docker-compose.yml -f docker-compose.dev.yml -f docker-compose.full.yml up --build`
3. If you are using an external DMS container, set `DMS_ADMIN_DMS_CONTAINER_NAME` in `.env` to match it.

The root Compose workflow reads supported local overrides from `.env`. If `.env` is absent, Compose uses the documented defaults from the compose files.

## Tests

- Backend unit tests: `cd backend && UV_CACHE_DIR=.uv-cache uv run pytest`
- Frontend tests: `cd frontend && npm test`
- Frontend build check: `cd frontend && npm run build`
- Local DMS integration tests:
  `cd backend && RUN_DMS_INTEGRATION=1 UV_CACHE_DIR=.uv-cache uv run pytest tests/integration/test_dms_container.py`

The integration suite starts a local Docker Mail Server container from `backend/tests/integration/compose.yaml` and exercises setup-managed account, alias, and quota flows against it.

## Docker compose

The repository now uses a layered Compose workflow:

- `docker-compose.yml`: base runtime stack for the single production `api` image
- `docker-compose.dev.yml`: local build, bind mount, and reload overrides, plus the Vite frontend service
- `docker-compose.full.yml`: optional local mailserver stack

Common commands:

```bash
docker compose -f docker-compose.yml -f docker-compose.dev.yml up --build
```

- Starts the recommended contributor workflow for local development.
- Builds the backend and frontend images locally.
- Publishes the backend on `http://localhost:8000`.
- Publishes the Vite frontend on `http://localhost:5173`.

```bash
docker compose up
```

- Starts the base runtime stack using the single production application image.
- This workflow is intended for a published-image runtime or for a previously built local image tagged as `${DMS_ADMIN_IMAGE_REGISTRY}/backend:${DMS_ADMIN_IMAGE_TAG}`.
- If that image is not present locally, Compose attempts to pull it from the configured registry.

```bash
docker compose -f docker-compose.yml -f docker-compose.full.yml up
```

- Starts the base runtime stack plus the optional local mailserver.
- Uses the same image-backed prerequisite path as `docker compose up`.

```bash
docker compose -f docker-compose.yml -f docker-compose.dev.yml -f docker-compose.full.yml up --build
```

- Starts the full local development stack, including the optional local mailserver.

On hosts with the legacy Compose binary, replace `docker compose` with `docker-compose`.

Useful overrides:

- `DMS_ADMIN_DMS_CONTAINER_NAME`: target running DMS container name
- `DMS_ADMIN_ADMIN_USERNAME` / `DMS_ADMIN_ADMIN_PASSWORD`: admin login
- `DMS_ADMIN_SESSION_SECRET`: session signing secret
- `DMS_ADMIN_API_PORT`: published API port, default `8000`
- `DMS_ADMIN_FRONTEND_PORT`: published frontend port for the dev overlay, default `5173`
- `VITE_API_BASE_URL`: frontend API base URL for the dev overlay, default `http://localhost:8000/api`
- `DMS_ADMIN_FRONTEND_DIST_DIR`: backend path used to serve the built frontend in the production image, default `/app/frontend-dist`
- `DMS_ADMIN_IMAGE_REGISTRY`: image registry or namespace used by compose image references
- `DMS_ADMIN_IMAGE_TAG`: image tag, default `latest`
- `DMS_ADMIN_MAILSERVER_IMAGE`: optional mailserver image for the full-stack overlay
- `DMS_ADMIN_MAILSERVER_HOSTNAME`: optional mailserver hostname for the full-stack overlay
- `DMS_ADMIN_MAILSERVER_DOMAINNAME`: optional mailserver domain name for the full-stack overlay

With the image variables above, the base Compose stack resolves the production runtime to:

```text
${DMS_ADMIN_IMAGE_REGISTRY}/backend:${DMS_ADMIN_IMAGE_TAG}
```

## Building and pushing images

Use `scripts/build-images.sh` to build the single production runtime image locally for one architecture. Use `scripts/push-images.sh` to push the existing local tag to a registry. Both scripts read the same image variables from the shell or from the root `.env` file. Shell variables take precedence over `.env` values.

Required configuration:

- `DMS_ADMIN_IMAGE_REGISTRY`: target registry or namespace, for example `ghcr.io/example`
- `DMS_ADMIN_IMAGE_ARCH`: target architecture, either `amd64` or `arm64`; defaults to `amd64`
- `DMS_ADMIN_IMAGE_TAG`: image tag; defaults to `latest`

Authenticate with the target registry before publishing:

```bash
docker login ghcr.io
```

Example using `.env` values:

```bash
scripts/build-images.sh
```

Push the built tags:

```bash
scripts/push-images.sh
```

Example one-off build:

```bash
DMS_ADMIN_IMAGE_REGISTRY=ghcr.io/example DMS_ADMIN_IMAGE_ARCH=arm64 DMS_ADMIN_IMAGE_TAG=latest scripts/build-images.sh
```

Example one-off push:

```bash
DMS_ADMIN_IMAGE_REGISTRY=ghcr.io/example DMS_ADMIN_IMAGE_ARCH=arm64 DMS_ADMIN_IMAGE_TAG=latest scripts/push-images.sh
```

The scripts operate on the production runtime image:

```text
<registry>/backend:<tag>
```

## Multi-architecture validation

Run the container validation script to build the single production image and run the backend/frontend automated checks for `linux/amd64` and `linux/arm64`:

```bash
scripts/validate-multiarch.sh
```

The script requires Docker, Docker Buildx, and the ability to run both target platforms locally. On Apple Silicon and other single-architecture hosts, enable Docker Desktop platform emulation or binfmt/QEMU support before running it.

Validation covers:

- the backend test target from the production Dockerfile
- the frontend test target from the production Dockerfile
- the final production runtime image build
