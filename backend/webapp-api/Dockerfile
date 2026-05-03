FROM python:3.14-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8080 \
    PYTHONPATH="/backend/webapp-api"

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/install.sh | sh && \
    mv /root/.local/bin/uv /usr/local/bin/uv && \
    chmod +x /usr/local/bin/uv
ENV PATH="/usr/local/bin:$PATH"

# Build context must be set to backend/ directory
# docker build -t webapp-api -f webapp-api/Dockerfile .
#
# Mirror the uv workspace structure under /backend/ so { workspace = true }
# sources resolve correctly and contracts are installed as editable packages.

# Workspace root
COPY pyproject.toml uv.lock /backend/

# All workspace member pyproject.toml files (uv needs these for workspace discovery)
COPY webapp-api/pyproject.toml /backend/webapp-api/pyproject.toml
COPY scraper-api-contract/pyproject.toml /backend/scraper-api-contract/pyproject.toml
COPY webapp-api-contract/pyproject.toml /backend/webapp-api-contract/pyproject.toml
COPY scraper-api/pyproject.toml /backend/scraper-api/pyproject.toml

# Contract source (editable installs — live changes visible without reinstalling)
COPY scraper-api-contract/scraper_api_contract/ /backend/scraper-api-contract/scraper_api_contract/
COPY webapp-api-contract/webapp_api_contract/ /backend/webapp-api-contract/webapp_api_contract/

# Service source
COPY webapp-api/src/ /backend/webapp-api/src/
COPY webapp-api/lib/ /backend/webapp-api/lib/

WORKDIR /backend/webapp-api

RUN uv sync --frozen --no-dev --package webapp-api

RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /backend

USER appuser

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8080/health')" || exit 1

CMD ["/backend/.venv/bin/uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]
