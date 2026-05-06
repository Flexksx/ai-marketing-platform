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

# 1. Copy config files
COPY pyproject.toml uv.lock README.md ./
COPY backend/ backend/
COPY prompts/ prompts/

# 2. Install project and dependencies
RUN uv sync --frozen --no-dev


RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

USER appuser

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD uv run python -c "import urllib.request; urllib.request.urlopen('http://localhost:8080/health')" || exit 1

FROM base as api

CMD ["/app/.venv/bin/uvicorn", "services.client_api.main:app", "--host", "0.0.0.0", "--port", "8080"]

FROM base as worker

USER root

ENV PLAYWRIGHT_BROWSERS_PATH=/ms-playwright

RUN apt-get update && apt-get install -y --no-install-recommends \
    libnss3 \
    libnspr4 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libasound2 \
    libpango-1.0-0 \
    libcairo2 \
    fonts-liberation \
    && rm -rf /var/lib/apt/lists/*

# Install Playwright browsers into the environment
# FIX: Added chown here because 'uv run' as root dirties the .venv permissions
RUN uv run playwright install chromium && \
    uv run playwright install-deps chromium && \
    chown -R appuser:appuser /app /ms-playwright

USER appuser

CMD ["/app/.venv/bin/uvicorn", "services.worker_api.main:app", "--host", "0.0.0.0", "--port", "8080", "--timeout-keep-alive", "3600"]
