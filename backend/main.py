"""Entry point for the FastAPI application."""

from __future__ import annotations

from fastapi import FastAPI, HTTPException

from config import get_settings
from database import get_client, get_database, lifespan_context

settings = get_settings()

app = FastAPI(title=settings.app_name, lifespan=lifespan_context)


@app.get("/health", summary="Service health check")
async def health() -> dict[str, str]:
    """Return application health and MongoDB connectivity status."""

    try:
        get_client().admin.command("ping")
    except Exception as exc:  # pylint: disable=broad-except
        raise HTTPException(status_code=503, detail="MongoDB unavailable") from exc

    return {"status": "ok", "database": settings.mongodb_database}


@app.get("/documents", summary="List collection names")
async def list_collections() -> dict[str, list[str]]:
    """Example endpoint that lists all collection names in the configured database."""

    db = get_database()
    return {"collections": db.list_collection_names()}

