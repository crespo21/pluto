"""FastAPI application setup and dependency wiring."""

from contextlib import asynccontextmanager
from fastapi import FastAPI

from src.properties.settings import settings
from src.infrastructure.database.config import init_db
from src.presentation.api.endpoints.user.user_endpoints import router as user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize database before the application starts."""
    init_db()
    yield


# Create and configure FastAPI application
app = FastAPI(
    title=settings.API_TITLE,
    description=settings.API_DESCRIPTION,
    version=settings.API_VERSION,
    debug=settings.DEBUG,
    lifespan=lifespan,
)

# Include routers with API prefix
app.include_router(user_router, prefix="/api")

@app.get("/", tags=["Health"])
async def health():
    """Health check endpoint."""
    return {"status": "OK", "message": "Pluto API is running"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)