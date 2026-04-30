# DMS Admin

Single-server admin interface for Docker Mail Server.

## Layout

- `backend/`: FastAPI API
- `frontend/`: React UI
- `openspec/`: proposal, design, specs, and task tracking

## Local development

1. Start Docker Mail Server separately and note its container name.
2. Update environment values if your container is not named `mailserver`.
3. Run the backend with `uv run uvicorn dms_admin_api.main:app --reload` from `backend/`.
4. Run the frontend with `npm run dev` from `frontend/`.

## Tests

- Backend unit tests: `cd backend && UV_CACHE_DIR=.uv-cache uv run pytest`
- Frontend tests: `cd frontend && npm test`
- Frontend build check: `cd frontend && npm run build`
- Local DMS integration tests:
  `cd backend && RUN_DMS_INTEGRATION=1 UV_CACHE_DIR=.uv-cache uv run pytest tests/integration/test_dms_container.py`

The integration suite starts a local Docker Mail Server container from `backend/tests/integration/compose.yaml` and exercises setup-managed account, alias, and quota flows against it.

## Docker compose

Use `docker compose up --build` to run the admin services alongside a running DMS instance.

Useful overrides:

- `DMS_ADMIN_DMS_CONTAINER_NAME`: target running DMS container name
- `DMS_ADMIN_ADMIN_USERNAME` / `DMS_ADMIN_ADMIN_PASSWORD`: admin login
- `DMS_ADMIN_API_PORT`: published API port, default `8000`
- `DMS_ADMIN_FRONTEND_PORT`: published frontend port, default `5173`

Example against the local integration DMS container:

```bash
DMS_ADMIN_DMS_CONTAINER_NAME=dms-admin-test-mailserver docker compose up --build
```
