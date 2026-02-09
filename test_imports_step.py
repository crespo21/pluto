import sys
sys.path.insert(0, '.')

print("Importing settings...")
from src.properties.settings import settings
print("✓ Settings imported")

print("Importing database config...")
from src.infrastructure.database.config import init_db
print("✓ Database config imported")

print("Importing FastAPI...")
from fastapi import FastAPI
print("✓ FastAPI imported")

print("Importing middleware...")
from src.core.middleware import LoggingMiddleware
print("✓ Middleware imported")

print("Importing user router...")
from src.presentation.api.endpoints.user.user_endpoints import router as user_router
print("✓ User router imported")

print("Importing product router...")
from src.presentation.api.endpoints.product.product_endpoints import router as product_router
print("✓ Product router imported")

print("All imports successful!")
