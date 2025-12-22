from fastapi import FastAPI

from router import audits, decisions, experiment, feature, variant

def create_app() -> FastAPI:
    app = FastAPI(title="Feature Hub API", version="0.1.0")

    app.include_router(feature.router)
    app.include_router(experiment.router)
    app.include_router(variant.router)
    app.include_router(decisions.router)
    app.include_router(audits.router)

    @app.get("/health", tags=["health"])
    async def health_check():
        return {"status": "ok"}

    return app


app = create_app()
