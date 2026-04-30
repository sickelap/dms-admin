FROM python:3.12-slim AS base

WORKDIR /app

COPY pyproject.toml uv.lock* ./
RUN pip install --no-cache-dir uv

FROM base AS test

COPY src ./src
COPY tests ./tests
RUN uv sync --frozen || uv sync

CMD ["uv", "run", "pytest"]

FROM base AS runtime

RUN apt-get update \
    && apt-get install -y --no-install-recommends docker.io \
    && rm -rf /var/lib/apt/lists/*

COPY src ./src
RUN uv sync --frozen --no-dev || uv sync --no-dev

CMD ["uv", "run", "uvicorn", "dms_admin_api.main:app", "--host", "0.0.0.0", "--port", "8000"]
