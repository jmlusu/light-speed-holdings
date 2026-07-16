"""FastAPI application for the CEO dashboard."""

from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from ai_company.dashboard.api import router

STATIC_DIR = Path(__file__).resolve().parents[3] / "static"


def create_app() -> FastAPI:
    app = FastAPI(title="Light Speed Holdings — CEO Dashboard", version="0.1.0")
    app.include_router(router)
    app.mount("/", StaticFiles(directory=str(STATIC_DIR), html=True), name="static")
    return app


app = create_app()
