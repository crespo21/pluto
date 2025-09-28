# Pluto API Blueprint

A complete teaching scaffold demonstrating production-ready API development with Python. This project showcases clean architecture, proper separation of concerns, environment-based configuration, and database migrations. Perfect for learning modern API development patterns.

---

## 🚀 Quick Start Guide

**Follow these steps exactly** - this will get you up and running in 5 minutes:

### Step 1: Set Up Your Environment

```bash
# 1. Clone the repository (if you haven't already)
git clone <your-repository-url>
cd pluto

# 2. Create a Python virtual environment
python -m venv .venv

# 3. Activate the virtual environment
# On macOS/Linux:
source .venv/bin/activate
# On Windows:
# .venv\Scripts\activate

# 4. Install all required packages
pip install -r requirements.txt
```

> 💡 **Important**: Always activate the virtual environment before working on the project. You'll see `(.venv)` in your terminal prompt when it's active.

### Step 2: Configure the Application

The application uses environment variables for configuration. You can use the existing `.env` file or create your own:

```bash
# Check if .env file exists (it should)
ls -la .env

# If it doesn't exist, copy from example:
cp .env.example .env
```

Your `.env` file should contain:

```env
# Database Configuration
DATABASE_URL=sqlite:///./pluto.db
SQLALCHEMY_ECHO=0

# API Configuration
API_TITLE=Pluto API
DEBUG=1

# Server Configuration
HOST=127.0.0.1
PORT=8000
RELOAD=1
```

### Step 3: Set Up the Database

```bash
# Create database tables using migrations
alembic upgrade head
```

### Step 4: Start the Application

```bash
# Start the development server
python run.py
```

You should see output like:

```
INFO:     Will watch for changes in these directories: ['/path/to/pluto']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345] using StatReload
INFO:     Started server process [12346]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### Step 5: Test That Everything Works

**Option 1: Using your web browser**

1. Open http://127.0.0.1:8000 - you should see: `{"status":"OK","message":"Pluto API is running"}`
2. Open http://127.0.0.1:8000/docs - you should see the interactive API documentation

**Option 2: Using curl (if you have it)**

```bash
# Test health endpoint
curl http://127.0.0.1:8000/

# Create a test user
curl -X POST http://127.0.0.1:8000/api/users \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@example.com","status":"active"}'

# Get the user back
curl http://127.0.0.1:8000/api/users/1
```

**🎉 Congratulations!** Your API is now running. Visit http://127.0.0.1:8000/docs to explore all available endpoints.

### Common Issues & Solutions

**Issue**: `python: command not found`
**Solution**: Use `python3` instead of `python`

**Issue**: `ERROR: Address already in use`
**Solution**: Another instance is running. Stop it with `Ctrl+C` or change the port in `.env`

**Issue**: `ModuleNotFoundError`
**Solution**: Make sure your virtual environment is activated (`source .venv/bin/activate`)

**Issue**: Database errors
**Solution**: Run `alembic upgrade head` to create/update database tables## 🧪 Testing Strategy

### Test Structure

```
tests/
├── unit/                    # Fast tests, no external dependencies
│   ├── domain/             # Test entities, value objects
│   └── application/        # Test services with mocked repositories
├── integration/            # Test with real database
│   └── infrastructure/     # Test repositories, database operations
└── e2e/                   # End-to-end API tests
    └── api/               # Test complete request/response cycles
```

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run all tests
pytest

# Run specific test categories  
pytest tests/unit/          # Unit tests only
pytest tests/integration/   # Integration tests only
pytest tests/e2e/          # End-to-end tests only

# Run with coverage
pytest --cov=src --cov-report=html
```

### Test Examples

```python
# Unit test (tests/unit/application/test_user_service.py)
def test_create_user_success():
    # Arrange
    mock_repo = Mock(spec=UserRepository)
    service = UserService(mock_repo)
  
    # Act & Assert
    result = service.create_user(user_dto)
    mock_repo.create.assert_called_once()

# Integration test (tests/integration/test_user_repository.py)  
def test_repository_creates_user(db_session):
    repo = SqlAlchemyUserRepository(db_session)
    user = User(None, "test", "test@example.com", UserStatus.ACTIVE)
  
    created = repo.create(user)
    assert created.user_id is not None

# E2E test (tests/e2e/test_user_api.py)
async def test_create_user_endpoint(client):
    response = await client.post("/api/users", json={
        "username": "testuser",
        "email": "test@example.com"
    })
    assert response.status_code == 201
```t for learning modern API development patterns.

---

## 🚀 Quick Start

### 1. Environment Setup

```bash
# Clone and navigate to the project
git clone <repository-url>
cd pluto

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

Copy and customize the environment file:

cp .env.example .env

Edit `.env` to match your needs:

```env
# Database Configuration
DATABASE_URL=sqlite:///./pluto.db
SQLALCHEMY_ECHO=0

# API Configuration  
API_TITLE=Pluto API
DEBUG=1

# Server Configuration
HOST=127.0.0.1
PORT=8000
```

### 3. Database Setup

```bash
# Run initial migration to create tables
alembic upgrade head
```

### 4. Start the Application

```bash
# Development server with auto-reload
python run.py

# The API will be available at:
# - Main API: http://127.0.0.1:8000
# - Documentation: http://127.0.0.1:8000/docs
# - Health check: http://127.0.0.1:8000/
```

## 📋 Database Migrations

### Creating New Migrations

When you modify models in `src/infrastructure/database/models/`:

```bash
# Generate migration automatically
alembic revision --autogenerate -m "describe your changes"

# Review the generated migration file in:
# src/infrastructure/migrations/alembic/versions/

# Apply migrations
alembic upgrade head
```

### Migration Commands

```bash
# Show current migration status
alembic current

# Show migration history
alembic history

# Downgrade to previous migration
alembic downgrade -1

# Reset database (careful!)
alembic downgrade base
alembic upgrade head
```

## 🏗️ Architecture Overview

### Project Structure

```
├── .env                          # Environment variables (DO NOT commit to git)
├── .env.example                  # Example environment file (safe to commit)
├── alembic.ini                   # Alembic migration configuration
├── requirements.txt              # Python dependencies
├── run.py                        # Application launcher script
└── src/
    ├── main.py                   # FastAPI app factory & router registration
    ├── properties/               # Application configuration
    │   ├── __init__.py
    │   └── settings.py          # Environment-based settings (replaces config.py)
    ├── domain/                   # 🏛️ Pure business logic (no dependencies)
    │   ├── __init__.py
    │   ├── entities/             # Business entities (User, Product, etc.)
    │   │   ├── __init__.py
    │   │   └── user.py
    │   ├── enums/                # Domain enumerations (UserStatus, etc.)
    │   │   ├── __init__.py
    │   │   └── user_enums.py
    │   ├── exceptions/           # Domain-specific exceptions
    │   │   ├── __init__.py
    │   │   └── user_exceptions.py
    │   └── repositories/         # Repository interfaces (contracts)
    │       ├── __init__.py
    │       └── user_repository.py
    ├── application/              # 🎯 Use cases and orchestration
    │   ├── __init__.py
    │   ├── dto/                  # Data Transfer Objects
    │   │   ├── __init__.py
    │   │   └── user_dto.py
    │   └── services/             # Application services (business workflows)
    │       ├── __init__.py
    │       └── user_services.py
    ├── infrastructure/           # 🔧 External systems (database, APIs, etc.)
    │   ├── __init__.py
    │   └── database/
    │       ├── __init__.py
    │       ├── config.py         # DB engine, session management
    │       ├── models/           # SQLAlchemy ORM models
    │       │   ├── __init__.py
    │       │   └── user_model.py
    │       ├── repositories/     # Repository implementations
    │       │   ├── __init__.py
    │       │   └── sqlalchemy_user_repository.py
    │       └── migrations/       # Database migrations (Alembic)
    │           └── alembic/
    │               ├── env.py
    │               ├── script.py.mako
    │               └── versions/
    └── presentation/             # 🌐 HTTP API layer
        ├── __init__.py
        └── api/
            ├── __init__.py
            ├── dependencies.py   # 🔌 FastAPI dependency injection
            ├── models.py         # 📋 Pydantic request/response schemas
            └── endpoints/        # 🛣️ API endpoints by feature
                ├── __init__.py
                └── user/
                    ├── __init__.py
                    └── user_endpoints.py
```

**Key Files Every Beginner Must Understand:**

🔧 **Configuration & Setup**

- `src/properties/settings.py` - All app configuration (database, API settings)
- `src/main.py` - FastAPI app creation, router registration
- `src/presentation/api/dependencies.py` - Dependency injection wiring

🎯 **Business Logic Flow**

- `src/domain/entities/` - Your business objects
- `src/application/services/` - Your use cases/workflows
- `src/infrastructure/database/repositories/` - Database operations
- `src/presentation/api/endpoints/` - HTTP API endpoints

### Clean Architecture Principles

1. **Domain Layer**: Pure business logic, no external dependencies
2. **Application Layer**: Orchestrates use cases, depends only on domain
3. **Infrastructure Layer**: Implements domain contracts using external tools
4. **Presentation Layer**: HTTP interface, depends on application services

**Dependency Rule**: Inner layers never depend on outer layers. This enables:

- Easy testing (mock external dependencies)
- Technology swapping (change database, web framework)
- Multiple interfaces (HTTP, CLI, jobs) using same business logic

### Key Configuration Files

#### `src/properties/settings.py`

**Purpose**: Centralized configuration management using environment variables

This file:

- Loads variables from `.env` file using `python-dotenv`
- Provides type-safe access to configuration
- Sets sensible defaults for all settings
- Is imported throughout the application as `from src.properties.settings import settings`

```python
# Example usage in any file:
from src.properties.settings import settings

# Access configuration
database_url = settings.DATABASE_URL
api_title = settings.API_TITLE
debug_mode = settings.DEBUG
```

#### `src/main.py`

**Purpose**: FastAPI application factory and router registration

This is where you:

- Create the FastAPI app instance
- Configure app metadata (title, description, version)
- Register all API routers with their prefixes
- Set up startup/shutdown events

**Important**: Every new feature's router MUST be registered here!

#### `src/presentation/api/dependencies.py`

**Purpose**: FastAPI dependency injection container

This file contains:

- Database session providers
- Repository factory functions
- Service factory functions
- Any shared dependencies

**Pattern**: For each new service, add two functions:

```python
def get_[feature]_repository(session: Session = Depends(get_session)) -> [Feature]Repository:
    return SqlAlchemy[Feature]Repository(session=session)

def get_[feature]_service(repo: [Feature]Repository = Depends(get_[feature]_repository)) -> [Feature]Service:
    return [Feature]Service([feature]_repository=repo)
```

## 🔄 Complete Guide: Adding New Features

This step-by-step guide shows exactly how to add a new feature (e.g., "Product") to the system. **Follow every step in order** - this is the complete workflow used by professional developers.

### 📋 Overview: What We'll Build

We'll add a Product feature with these operations:

- Create product
- Get product by ID
- Update product
- Delete product

### Step 1: Define Domain Layer (Business Logic)

**What**: Define the core business rules and entities

#### 1.1 Create the Domain Entity

Create `src/domain/entities/product.py`:

```python
from typing import Optional
from decimal import Decimal

class Product:
    """Core Product business entity."""
  
    def __init__(self, product_id: Optional[int], name: str, price: Decimal, description: str):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.description = description
  
    def __repr__(self):
        return f"Product(id={self.product_id}, name='{self.name}', price={self.price})"
  
    def update_price(self, new_price: Decimal):
        """Business rule: Price must be positive."""
        if new_price <= 0:
            raise ValueError("Price must be positive")
        self.price = new_price
  
    def to_dict(self):
        return {
            "product_id": self.product_id,
            "name": self.name,
            "price": float(self.price),
            "description": self.description
        }
```

#### 1.2 Create Domain Enums (if needed)

Create `src/domain/enums/product_enums.py`:

```python
from enum import Enum

class ProductStatus(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    OUT_OF_STOCK = "out_of_stock"
```

#### 1.3 Create Domain Exceptions

Create `src/domain/exceptions/product_exceptions.py`:

```python
class ProductNotFoundError(Exception):
    """Raised when a product is not found."""
    pass

class ProductAlreadyExistsError(Exception):
    """Raised when trying to create a product that already exists."""
    pass
```

#### 1.4 Define Repository Interface (Contract)

Create `src/domain/repositories/product_repository.py`:

```python
from abc import ABC, abstractmethod
from typing import Optional, List
from ..entities.product import Product

class ProductRepository(ABC):
    """Abstract repository defining contract for Product persistence."""
  
    @abstractmethod
    def create(self, product: Product) -> Product:
        """Create a new product."""
        pass
  
    @abstractmethod
    def find_by_id(self, product_id: int) -> Optional[Product]:
        """Find product by ID."""
        pass
  
    @abstractmethod
    def find_all(self) -> List[Product]:
        """Get all products."""
        pass
  
    @abstractmethod
    def update(self, product: Product) -> Product:
        """Update existing product."""
        pass
  
    @abstractmethod
    def delete_by_id(self, product_id: int) -> bool:
        """Delete product by ID."""
        pass
```

### Step 2: Create Database Model (Infrastructure Layer)

**What**: Define how data is stored in the database

#### 2.1 Create SQLAlchemy Model

Create `src/infrastructure/database/models/product_model.py`:

```python
from decimal import Decimal
from typing import Any
from sqlalchemy import String, Numeric
from sqlalchemy.orm import Mapped, mapped_column
from .user_model import Base  # Import existing Base
from src.domain.entities.product import Product

class ProductModel(Base):
    """SQLAlchemy model for Product table."""
  
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=True)

    def __repr__(self) -> str:
        return f"ProductModel(id={self.id}, name='{self.name}', price={self.price})"

    def to_domain(self) -> Product:
        """Convert database model to domain entity."""
        return Product(
            product_id=self.id,
            name=self.name,
            price=self.price,
            description=self.description or ""
        )

    @classmethod
    def from_domain(cls, product: Product) -> "ProductModel":
        """Convert domain entity to database model."""
        kwargs: dict[str, Any] = {
            "name": product.name,
            "price": product.price,
            "description": product.description,
        }
      
        if product.product_id is not None:
            kwargs["id"] = product.product_id
          
        return cls(**kwargs)
```

#### 2.2 Generate Database Migration

```bash
# Generate migration automatically
alembic revision --autogenerate -m "add products table"

# Review the generated file in: src/infrastructure/migrations/alembic/versions/
# Then apply the migration:
alembic upgrade head
```

### Step 3: Implement Repository (Infrastructure Layer)

**What**: Implement the repository interface using SQLAlchemy

Create `src/infrastructure/database/repositories/sqlalchemy_product_repository.py`:

```python
import logging
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import select

from src.domain.repositories.product_repository import ProductRepository
from src.domain.entities.product import Product
from src.domain.exceptions.product_exceptions import ProductNotFoundError
from ..models.product_model import ProductModel

class SqlAlchemyProductRepository(ProductRepository):
    """SQLAlchemy implementation of ProductRepository."""
  
    def __init__(self, session: Session):
        self.session = session
        self.logger = logging.getLogger(__name__)

    def create(self, product: Product) -> Product:
        """Create a new product in database."""
        product_model = ProductModel.from_domain(product)
      
        try:
            self.session.add(product_model)
            self.session.commit()
            self.session.refresh(product_model)
        except Exception:
            self.session.rollback()
            raise
          
        return product_model.to_domain()

    def find_by_id(self, product_id: int) -> Optional[Product]:
        """Find product by ID."""
        product_model = self.session.get(ProductModel, product_id)
        return product_model.to_domain() if product_model else None

    def find_all(self) -> List[Product]:
        """Get all products."""
        results = self.session.execute(select(ProductModel)).scalars().all()
        return [model.to_domain() for model in results]

    def update(self, product: Product) -> Product:
        """Update existing product."""
        if product.product_id is None:
            raise ValueError("Product ID is required for update")
          
        product_model = self.session.get(ProductModel, product.product_id)
        if not product_model:
            raise ProductNotFoundError(f"Product with ID {product.product_id} not found")
          
        product_model.name = product.name
        product_model.price = product.price
        product_model.description = product.description
      
        self.session.commit()
        self.session.refresh(product_model)
      
        return product_model.to_domain()

    def delete_by_id(self, product_id: int) -> bool:
        """Delete product by ID."""
        product_model = self.session.get(ProductModel, product_id)
        if not product_model:
            return False
          
        self.session.delete(product_model)
        self.session.commit()
        return True
```

### Step 4: Create Application Service (Application Layer)

**What**: Implement business use cases and coordinate between layers

#### 4.1 Create DTO (Data Transfer Object)

Create `src/application/dto/product_dto.py`:

```python
from dataclasses import dataclass
from typing import Optional
from decimal import Decimal

from src.domain.entities.product import Product

@dataclass(frozen=True)
class ProductDTO:
    """Application-layer representation of a product."""
  
    id: Optional[int]
    name: str
    price: Decimal
    description: str

    def to_domain(self) -> Product:
        """Convert DTO to domain entity."""
        return Product(
            product_id=self.id,
            name=self.name,
            price=self.price,
            description=self.description,
        )

    def to_dict(self) -> dict:
        """Serialize DTO to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "price": float(self.price),
            "description": self.description,
        }

    @classmethod
    def from_domain(cls, product: Product) -> "ProductDTO":
        """Create DTO from domain entity."""
        return cls(
            id=product.product_id,
            name=product.name,
            price=product.price,
            description=product.description,
        )
```

#### 4.2 Create Application Service

Create `src/application/services/product_service.py`:

```python
from typing import Optional, List
from decimal import Decimal

from src.application.dto.product_dto import ProductDTO
from src.domain.repositories.product_repository import ProductRepository
from src.domain.exceptions.product_exceptions import ProductNotFoundError

class ProductService:
    """Application service for Product use cases."""
  
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository

    def create_product(self, product_dto: ProductDTO) -> ProductDTO:
        """Create a new product."""
        product_entity = product_dto.to_domain()
        created_product = self.product_repository.create(product_entity)
        return ProductDTO.from_domain(created_product)

    def get_product_by_id(self, product_id: int) -> Optional[ProductDTO]:
        """Get product by ID."""
        product = self.product_repository.find_by_id(product_id)
        return ProductDTO.from_domain(product) if product else None

    def get_all_products(self) -> List[ProductDTO]:
        """Get all products."""
        products = self.product_repository.find_all()
        return [ProductDTO.from_domain(product) for product in products]

    def update_product(self, product_dto: ProductDTO) -> ProductDTO:
        """Update existing product."""
        product_entity = product_dto.to_domain()
        updated_product = self.product_repository.update(product_entity)
        return ProductDTO.from_domain(updated_product)

    def delete_product(self, product_id: int) -> bool:
        """Delete product by ID."""
        return self.product_repository.delete_by_id(product_id)
```

### Step 5: Add Dependency Injection

**What**: Wire up the new service in the dependency injection system

#### 5.1 Update `src/presentation/api/dependencies.py`

Add these functions to the existing file:

```python
# Add these imports at the top
from src.application.services.product_service import ProductService
from src.domain.repositories.product_repository import ProductRepository
from src.infrastructure.database.repositories.sqlalchemy_product_repository import SqlAlchemyProductRepository

# Add these functions at the bottom
def get_product_repository(session: Session = Depends(get_session)) -> ProductRepository:
    """Provide a ProductRepository instance with injected session."""
    return SqlAlchemyProductRepository(session=session)

def get_product_service(repo: ProductRepository = Depends(get_product_repository)) -> ProductService:
    """Provide a ProductService instance with injected repository."""
    return ProductService(product_repository=repo)
```

### Step 6: Create API Models (Presentation Layer)

**What**: Define the HTTP request/response schemas

#### 6.1 Update `src/presentation/api/models.py`

Add these classes to the existing file:

```python
from decimal import Decimal

# Add these new classes
class ProductCreate(BaseModel):
    """Schema for product creation requests."""
  
    name: str = Field(..., min_length=1, max_length=100, description="Product name")
    price: Decimal = Field(..., gt=0, description="Product price (must be positive)")
    description: str = Field(default="", max_length=500, description="Product description")
  
    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Laptop",
                "price": 999.99,
                "description": "High-performance laptop"
            }
        }
    }

class ProductResponse(BaseModel):
    """Schema for product responses."""
  
    id: Optional[int] = None
    name: str
    price: Decimal
    description: str
  
    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 1,
                "name": "Laptop",
                "price": 999.99,
                "description": "High-performance laptop"
            }
        }
    }

class ProductUpdate(BaseModel):
    """Schema for product updates."""
  
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    price: Optional[Decimal] = Field(None, gt=0)
    description: Optional[str] = Field(None, max_length=500)
```

### Step 7: Create API Endpoints

**What**: Create HTTP endpoints for the new feature

#### 7.1 Create Directory Structure

```bash
mkdir -p src/presentation/api/endpoints/product
touch src/presentation/api/endpoints/product/__init__.py
```

#### 7.2 Create `src/presentation/api/endpoints/product/product_endpoints.py`

```python
"""Product API endpoints."""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status

from src.application.dto.product_dto import ProductDTO
from src.application.services.product_service import ProductService
from src.domain.exceptions.product_exceptions import ProductNotFoundError
from src.presentation.api.dependencies import get_product_service
from src.presentation.api.models import ProductCreate, ProductResponse, ProductUpdate

# Convert between DTOs and API models
def _dto_to_response(product_dto: ProductDTO) -> ProductResponse:
    """Convert ProductDTO to ProductResponse."""
    data = product_dto.to_dict()
    return ProductResponse(
        id=data["id"],
        name=data["name"],
        price=data["price"],
        description=data["description"],
    )

def _request_to_dto(product_data: ProductCreate, product_id: Optional[int] = None) -> ProductDTO:
    """Convert ProductCreate to ProductDTO."""
    return ProductDTO(
        id=product_id,
        name=product_data.name,
        price=product_data.price,
        description=product_data.description,
    )

# Define router
router = APIRouter(
    prefix="/products",
    tags=["products"],
    responses={404: {"description": "Product not found"}},
)

@router.post(
    "",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new product",
)
async def create_product(
    product_data: ProductCreate,
    product_service: ProductService = Depends(get_product_service),
):
    """Create a new product."""
    try:
        product_dto = _request_to_dto(product_data)
        created_product = product_service.create_product(product_dto)
        return _dto_to_response(created_product)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )

@router.get(
    "/{product_id}",
    response_model=ProductResponse,
    summary="Get product by ID",
)
async def get_product(
    product_id: int,
    product_service: ProductService = Depends(get_product_service),
):
    """Get a product by ID."""
    product = product_service.get_product_by_id(product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {product_id} not found",
        )
    return _dto_to_response(product)

@router.get(
    "",
    response_model=List[ProductResponse],
    summary="Get all products",
)
async def get_all_products(
    product_service: ProductService = Depends(get_product_service),
):
    """Get all products."""
    products = product_service.get_all_products()
    return [_dto_to_response(product) for product in products]

# Add more endpoints as needed...
```

### Step 8: Register Router in Main Application

**What**: Tell FastAPI about your new endpoints

#### 8.1 Update `src/main.py`

Add these lines:

```python
# Add this import at the top
from src.presentation.api.endpoints.product.product_endpoints import router as product_router

# Add this line after the existing router registration
app.include_router(product_router, prefix="/api")
```

The file should now look like:

```python
"""FastAPI application setup and dependency wiring."""

from fastapi import FastAPI

from src.properties.settings import settings
from src.infrastructure.database.config import init_db
from src.presentation.api.endpoints.user.user_endpoints import router as user_router
from src.presentation.api.endpoints.product.product_endpoints import router as product_router

# Create and configure FastAPI application
app = FastAPI(
    title=settings.API_TITLE,
    description=settings.API_DESCRIPTION,
    version=settings.API_VERSION,
    debug=settings.DEBUG,
)

# Include routers with API prefix
app.include_router(user_router, prefix="/api")
app.include_router(product_router, prefix="/api")

# ... rest of the file
```

### Step 9: Test Your New Feature

**What**: Verify everything works correctly

#### 9.1 Start the Application

```bash
# Make sure you're in virtual environment
source .venv/bin/activate

# Start the server
python run.py
```

#### 9.2 Test the API

Visit `http://127.0.0.1:8000/docs` and you should see your new Product endpoints.

Test with curl:

```bash
# Create a product
curl -X POST http://127.0.0.1:8000/api/products \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Laptop",
    "price": 999.99,
    "description": "High-performance laptop"
  }'

# Get the product
curl http://127.0.0.1:8000/api/products/1
```

### 🎯 Key Files Modified Summary

When adding any new feature, you will touch these files:

1. **Domain Layer**: `src/domain/entities/`, `src/domain/repositories/`, `src/domain/exceptions/`
2. **Infrastructure Layer**: `src/infrastructure/database/models/`, `src/infrastructure/database/repositories/`
3. **Application Layer**: `src/application/dto/`, `src/application/services/`
4. **Presentation Layer**: `src/presentation/api/models.py`, `src/presentation/api/endpoints/`, `src/presentation/api/dependencies.py`
5. **Configuration**: `src/main.py` (register new routers)
6. **Database**: Generate and run migrations

### 🚨 Important Notes for Beginners

- **Always follow the layers**: Domain → Application → Infrastructure → Presentation
- **Never skip dependency injection**: Every service needs to be wired in `dependencies.py`
- **Always register routers**: New endpoints won't work until added to `main.py`
- **Run migrations**: Database changes require `alembic` commands
- **Test each step**: Don't build everything at once - test as you go

### 🔧 Common Beginner Mistakes & Solutions

#### "My new endpoint returns 404"

**Problem**: Router not registered in `main.py`
**Solution**: Add `app.include_router(your_router, prefix="/api")` to `src/main.py`

#### "Dependency injection error"

**Problem**: Service not defined in `dependencies.py`
**Solution**: Add both repository and service functions to `src/presentation/api/dependencies.py`

#### "Import errors when starting app"

**Problem**: Missing `__init__.py` files or wrong import paths**Solution**:

- Add empty `__init__.py` files in all directories
- Use absolute imports: `from src.domain.entities.product import Product`

#### "Database table doesn't exist"

**Problem**: Forgot to run migrations
**Solution**:

```bash
alembic revision --autogenerate -m "add your changes"
alembic upgrade head
```

#### "Settings not loading"

**Problem**: Environment variables not in `.env` or wrong import**Solution**:

- Check `.env` file exists and has correct values
- Import settings: `from src.properties.settings import settings`
- Use `settings.VARIABLE_NAME` not `os.getenv()`

#### "Tests fail with import errors"

**Problem**: Python path not set correctly
**Solution**: Run tests with: `PYTHONPATH=. pytest` or use `python -m pytest`

### 📁 File Checklist for New Features

When adding a new feature called "Product", verify you have:

✅ **Domain Layer**:

- `src/domain/entities/product.py` - Business entity
- `src/domain/repositories/product_repository.py` - Repository interface
- `src/domain/exceptions/product_exceptions.py` - Domain exceptions

✅ **Infrastructure Layer**:

- `src/infrastructure/database/models/product_model.py` - SQLAlchemy model
- `src/infrastructure/database/repositories/sqlalchemy_product_repository.py` - Implementation
- Migration generated and applied

✅ **Application Layer**:

- `src/application/dto/product_dto.py` - Data transfer object
- `src/application/services/product_service.py` - Application service

✅ **Presentation Layer**:

- Added models to `src/presentation/api/models.py`
- `src/presentation/api/endpoints/product/product_endpoints.py` - API endpoints
- Updated `src/presentation/api/dependencies.py` - Dependency injection
- Updated `src/main.py` - Router registration

✅ **Testing**:

- API endpoints work in `/docs`
- Database operations succeed
- All imports resolve correctly

---

## Implementing an API endpoint

1. **Define/extend DTOs** – update `UserDTO` or add new dataclasses for request/response payloads.
2. **Add service logic** – place orchestration code in `UserService` (create new services for other aggregates). Services should only call repository interfaces.
3. **Wire the repository** – `SqlAlchemyUserRepository` implements the domain contract using SQLAlchemy. Ensure helper functions (`_persist`, `_ensure_status`, etc.) remain at the class scope, not nested inside `__init__`.
4. **Expose via presentation layer** – choose a framework (FastAPI recommended for async support). In `presentation/api/user_controller.py`, create routers that depend on the service. Example skeleton:

   ```python
   from fastapi import APIRouter, Depends, HTTPException
   from src.application.dto.user_dto import UserDTO
   from src.application.services.user_services import UserService

   router = APIRouter(prefix="/users", tags=["users"])

   @router.post("", response_model=UserDTO)
   def create_user(payload: UserDTO, service: UserService = Depends(get_user_service)):
       try:
    	   return service.create_user(payload)
       except UserAlreadyExistsError as exc:
    	   raise HTTPException(status_code=409, detail=str(exc))
   ```
5. **Document** – describe request/response shapes using Pydantic models or JSON schemas so API consumers know what to expect.
6. **Test** – unit test the service (pure Python) and integration test the router using the framework’s test client with a transactional, throwaway database.

---

## Testing strategy

- **Unit tests**: target `domain` and `application` layers. Use fakes for `UserRepository` when testing services.
- **Integration tests**: spin up a temporary database, run migrations, and hit the `SqlAlchemyUserRepository` directly.
- **End-to-end tests**: exercise HTTP endpoints using the chosen framework’s test client (e.g., FastAPI’s `TestClient`).

Structure tests in a mirrored directory tree (`tests/domain`, `tests/application`, etc.) and run them with `pytest`.

## 🚀 API Usage Examples

### Create a User

```bash
curl -X POST http://127.0.0.1:8000/api/users \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "email": "john@example.com",
    "status": "active"
  }'
```

### Get User by ID

```bash
curl http://127.0.0.1:8000/api/users/1
```

### Update User Status

```bash
curl -X PATCH http://127.0.0.1:8000/api/users/1/status \
  -H "Content-Type: application/json" \
  -d '{"status": "inactive"}'
```

### List All Endpoints

Visit `http://127.0.0.1:8000/docs` for interactive API documentation.

## 🔧 Configuration Reference

### Environment Variables

| Variable            | Description                | Default                  |
| ------------------- | -------------------------- | ------------------------ |
| `DATABASE_URL`    | Database connection string | `sqlite:///./pluto.db` |
| `SQLALCHEMY_ECHO` | Log SQL queries            | `0`                    |
| `API_TITLE`       | API title in docs          | `Pluto API`            |
| `DEBUG`           | Enable debug mode          | `1`                    |
| `HOST`            | Server host                | `127.0.0.1`            |
| `PORT`            | Server port                | `8000`                 |
| `LOG_LEVEL`       | Logging level              | `INFO`                 |

### Production Deployment

```bash
# Set production environment variables
export DATABASE_URL="postgresql://user:pass@host/db"
export DEBUG=0
export SQLALCHEMY_ECHO=0

# Run with production server
pip install gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker src.main:app
```

## 📚 Learning Path

### For Beginners

1. **Start Here**: Explore the `/docs` endpoint to understand the API
2. **Read the Code**: Follow a request from `user_endpoints.py` → `UserService` → `UserRepository`
3. **Make Changes**: Try adding a new field to the User model
4. **Run Migrations**: Use `alembic` to apply your changes
5. **Test Your Changes**: Use the `/docs` interface to test

### Advanced Topics

- **Custom Repositories**: Implement caching, read replicas
- **Background Jobs**: Add Celery for async processing
- **Authentication**: Add JWT tokens, user roles
- **Monitoring**: Integrate OpenTelemetry, Prometheus
- **Testing**: Comprehensive test coverage
- **Docker**: Containerize the application

## 🤝 Contributing

1. Follow the architecture patterns shown
2. Add tests for new features
3. Update documentation
4. Use type hints consistently
5. Follow the existing code style

---

**This project demonstrates production-ready Python API development. Use it as a foundation for learning clean architecture, proper testing, and modern development practices.**
