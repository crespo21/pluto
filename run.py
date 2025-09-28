"""FastAPI application launcher."""

import sys
from pathlib import Path

# Add the project root directory to Python path
project_root = Path(__file__).parent.resolve()
sys.path.insert(0, str(project_root))

# Import the FastAPI app and settings
from src.properties.settings import settings
from src.main import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "run:app", 
        host=settings.HOST, 
        port=settings.PORT, 
        reload=settings.RELOAD,
        log_level=settings.LOG_LEVEL.lower()
    )