import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import db.schema_registry  # noqa: F401 - Ensures all SQLAlchemy models are registered
from services.client_api.routes.brand_generation import (
    router as brand_generation_router,
)
from services.client_api.routes.brands import router as brand_router
from services.client_api.routes.docs import router as docs_router
from vozai.config import get_settings
from vozai.http_logging import http_logging_middleware
from vozai.logging_config import configure_logging


settings = get_settings()

configure_logging(
    level=settings.log_level,
    service_name="client-api",
    environment=settings.environment,
)


app = FastAPI(
    title="Voisso API",
    description="Voisso marketing automation platform API",
    version="0.1.0",
    docs_url=None,
    redoc_url=None,
    redirect_slashes=False,
)

app.middleware("http")(http_logging_middleware)

allowed_origins = [
    "https://vozai.pages.dev",
]

if settings.environment == "development":
    allowed_origins.extend(
        [
            "http://localhost:3000",
            "http://localhost:5173",
            "http://127.0.0.1:3000",
            "http://127.0.0.1:5173",
        ]
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "HEAD"],
    allow_headers=["Authorization", "Content-Type", "Accept"],
)

app.include_router(docs_router)
app.include_router(brand_router)
app.include_router(brand_generation_router)


@app.get("/health")
async def health_check():
    return {"status": "ok", "environment": settings.environment}


@app.get("/")
async def root():
    return {
        "message": "Voisso API",
        "version": "0.1.0",
        "docs": "/docs",
    }


def main():
    uvicorn.run(
        "client_api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.environment == "development",
    )


if __name__ == "__main__":
    main()
