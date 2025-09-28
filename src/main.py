"""FastAPI application setup and dependency wiring."""

from fastapi import FastAPI

from src.properties.settings import settings
from src.infrastructure.database.config import init_db
from src.presentation.api.endpoints.user.user_endpoints import router as user_router

# Create and configure FastAPI application
app = FastAPI(
    title=settings.API_TITLE,
    description=settings.API_DESCRIPTION,
    version=settings.API_VERSION,
    debug=settings.DEBUG,
)

# Include routers with API prefix
app.include_router(user_router, prefix="/api")


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup."""
    # This is convenient for development but use Alembic for production migrations
    init_db()


@app.get("/", tags=["Health"])
async def health():
    """Health check endpoint."""
    return {"status": "OK", "message": "Pluto API is running"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)