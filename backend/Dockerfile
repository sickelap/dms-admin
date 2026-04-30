FROM python:3.12-slim

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends docker.io \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml uv.lock* ./
COPY src ./src
RUN pip install --no-cache-dir uv && uv sync --frozen --no-dev || uv sync --no-dev

CMD ["uv", "run", "uvicorn", "dms_admin_api.main:app", "--host", "0.0.0.0", "--port", "8000"]
