from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import routers from the routes directory
from routes import routing, parking, events, translation, webhooks


def create_app() -> FastAPI:
    """
    Application factory for the MARGSATHI Mobility Intelligence API.

    Having an app factory makes it easy to plug this backend into
    different environments (local, tests, cloud functions, etc.).
    """
    app = FastAPI(
        title="MARGSATHI Mobility Intelligence API",
        version="0.1.0",
        description=(
            "Hackathon-ready, modular FastAPI backend for the "
            "MARGSATHI mobility intelligence platform."
        ),
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )

    # Enable permissive CORS for hackathon-speed development.
    # In production, lock this down to known front-end origins.
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Health / meta endpoints
    @app.get("/", tags=["meta"])
    async def root():
        return {
            "name": "MARGSATHI Mobility Intelligence API",
            "version": app.version,
            "status": "ok",
            "docs_url": app.docs_url,
            "openapi_url": app.openapi_url,
        }

    @app.get("/health", tags=["meta"])
    async def health():
        return {"status": "healthy"}

    # Register feature routers
    app.include_router(
        routing.router,
        prefix="/api/routing",
        tags=["routing"],
    )
    app.include_router(
        parking.router,
        prefix="/api/parking",
        tags=["parking"],
    )
    app.include_router(
        events.router,
        prefix="/api/events",
        tags=["events"],
    )
    app.include_router(
        translation.router,
        prefix="/api/translation",
        tags=["translation"],
    )
    app.include_router(
        webhooks.router,
        prefix="/api/webhook",
        tags=["webhooks"],
    )

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )


