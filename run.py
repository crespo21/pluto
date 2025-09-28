"""FastAPI application launcher."""

import os
import sys
from pathlib import Path

# Add the project root directory to Python path
project_root = Path(__file__).parent.resolve()
sys.path.insert(0, str(project_root))

# Import the FastAPI app from the src module
from src.main import app

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("run:app", host="0.0.0.0", port=port, reload=True)