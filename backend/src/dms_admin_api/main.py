from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from dms_admin_api.config import get_settings
from dms_admin_api.routers import accounts, aliases, auth, health, quotas, relay, system


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title=settings.app_name)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(health.router, prefix="/api")
    app.include_router(auth.router, prefix="/api")
    app.include_router(accounts.router, prefix="/api")
    app.include_router(aliases.router, prefix="/api")
    app.include_router(quotas.router, prefix="/api")
    app.include_router(relay.router, prefix="/api")
    app.include_router(system.router, prefix="/api")
    return app


app = create_app()
