from pathlib import Path

from fastapi import FastAPI, HTTPException, status
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from dms_admin_api.config import get_settings
from dms_admin_api.routers import accounts, aliases, auth, health, quotas, relay, system


def _configure_frontend_routes(app: FastAPI, frontend_dist_path: Path) -> None:
    index_path = frontend_dist_path / "index.html"
    assets_path = frontend_dist_path / "assets"

    if assets_path.is_dir():
        app.mount("/assets", StaticFiles(directory=assets_path), name="frontend-assets")

    if not index_path.is_file():
        return

    @app.get("/", include_in_schema=False)
    def frontend_root() -> FileResponse:
        return FileResponse(index_path)

    @app.get("/{full_path:path}", include_in_schema=False)
    def frontend_client_route(full_path: str) -> FileResponse:
        if full_path.startswith("api/") or full_path.startswith("assets/"):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        return FileResponse(index_path)


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
    _configure_frontend_routes(app, settings.frontend_dist_path)
    return app


app = create_app()
