FROM node:24-alpine AS frontend-deps

WORKDIR /frontend

COPY frontend/package.json frontend/package-lock.json* ./
RUN npm ci

FROM frontend-deps AS frontend-test

COPY frontend/ ./

CMD ["npm", "test"]

FROM frontend-deps AS frontend-build

COPY frontend/ ./
RUN npm run build

FROM python:3.12-slim AS base

WORKDIR /app

COPY backend/pyproject.toml backend/uv.lock* ./
RUN pip install --no-cache-dir uv

FROM base AS test

COPY backend/src ./src
COPY backend/tests ./tests
RUN uv sync --frozen || uv sync

CMD ["uv", "run", "pytest"]

FROM base AS runtime

RUN apt-get update \
    && apt-get install -y --no-install-recommends docker.io \
    && rm -rf /var/lib/apt/lists/*

COPY backend/src ./src
RUN uv sync --frozen --no-dev || uv sync --no-dev
COPY --from=frontend-build /frontend/dist ./frontend-dist

CMD ["uv", "run", "uvicorn", "dms_admin_api.main:app", "--host", "0.0.0.0", "--port", "8000"]
