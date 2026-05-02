FROM python:3.14-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_SYSTEM_PYTHON=1 \
    PORT=8081 \
    PLAYWRIGHT_BROWSERS_PATH=/ms-playwright \
    PYTHONPATH="/app"

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
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

RUN curl -LsSf https://astral.sh/uv/install.sh | sh && \
    mv /root/.local/bin/uv /usr/local/bin/uv && \
    chmod +x /usr/local/bin/uv
ENV PATH="/usr/local/bin:$PATH"

WORKDIR /app

# Build context must be set to backend/ directory
# docker build -t scraper-api -f scraper-api/Dockerfile .
COPY scraper-api/pyproject.toml scraper-api/uv.lock ./
COPY scraper-api-contract/ /app/scraper-api-contract/
COPY webapp-api-contract/ /app/webapp-api-contract/
COPY scraper-api/src/ src/

RUN uv sync --frozen --no-dev

RUN uv run playwright install chromium

RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app /ms-playwright

USER appuser

EXPOSE 8081

HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8081/health')" || exit 1

CMD ["/app/.venv/bin/uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8081"]
