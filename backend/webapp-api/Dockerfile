FROM python:3.14-slim as base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_SYSTEM_PYTHON=1 \
    PORT=8080 \
    PYTHONPATH="/app"

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/install.sh | sh && \
    mv /root/.local/bin/uv /usr/local/bin/uv && \
    chmod +x /usr/local/bin/uv
ENV PATH="/usr/local/bin:$PATH"

WORKDIR /app

# Build context must be set to backend/ directory
# docker build -t webapp-api -f webapp-api/Dockerfile .
COPY webapp-api/pyproject.toml webapp-api/uv.lock ./
COPY webapp-api-contract/ /webapp-api-contract/
COPY scraper-api-contract/ /scraper-api-contract/
COPY webapp-api/src/ src/
COPY webapp-api/lib/ lib/

RUN uv sync --frozen --no-dev


RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

USER appuser

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD uv run python -c "import urllib.request; urllib.request.urlopen('http://localhost:8080/health')" || exit 1

CMD ["/app/.venv/bin/uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]
