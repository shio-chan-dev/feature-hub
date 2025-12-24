import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from router import audits, decisions, experiment, feature, variant
from utils.logger import logger

def create_app() -> FastAPI:
    app = FastAPI(title="Feature Hub API", version="0.1.0")

    # CORS:
    # - 可通过环境变量 CORS_ALLOW_ORIGINS 指定允许的 Origin（逗号分隔）
    # - 未配置时默认放行所有 Origin（含本地），避免 nginx/内网部署时浏览器跨域拦截
    cors_origins_env = os.getenv("CORS_ALLOW_ORIGINS")
    if cors_origins_env:
        allow_origins = [o.strip() for o in cors_origins_env.split(",") if o.strip()]
    else:
        allow_origins = [
                "http://localhost:5173",
                "http://127.0.0.1:5173",
                "*",
                ]

    app.add_middleware(
            CORSMiddleware,
            allow_origins=allow_origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
            )

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
