# 🚀 Pluto - Clean Architecture FastAPI Project

A modern, production-ready Python web API built with **Clean Architecture** principles, **FastAPI**, **SQLAlchemy**, and **Alembic migrations**.

## 🎯 Perfect for Learning

This project is designed to teach clean architecture through hands-on development. You'll learn:

- Clean Architecture (Domain/Application/Infrastructure/Presentation layers)
- Modern Python web development with FastAPI
- Database design and migrations with SQLAlchemy + Alembic
- Dependency injection and separation of concerns
- RESTful API design patterns

## 📁 Project Structure

```
src/
├── domain/                 # 🧠 Business Logic & Rules
│   ├── entities/          # Core business objects
│   ├── enums/             # Domain enumerations
│   ├── exceptions/        # Domain-specific errors
│   └── repositories/      # Data access interfaces
├── application/           # 🔧 Use Cases & Services  
│   ├── dto/               # Data transfer objects
│   └── services/          # Application business logic
├── infrastructure/        # 🔌 External Concerns
│   └── database/          # Database implementations
│       ├── models/        # SQLAlchemy models
│       └── repositories/  # Repository implementations
├── presentation/          # 🌐 API Layer
│   └── api/               # FastAPI routes and controllers
│       └── endpoints/     # Organized endpoint modules
├── properties/            # ⚙️ Configuration
│   └── settings.py        # Environment-based settings
└── main.py               # 🚀 Application entry point
```

## ⚡ Quick Start (For Complete Beginners)

### Prerequisites

- Python 3.9+ installed on your system
- Basic terminal/command line knowledge

### Step 1: Get the Code

```bash
# Clone the repository (or download ZIP)
git clone <your-repo-url>
cd pluto
```

### Step 2: Set Up Python Environment

```bash
# Create a virtual environment
python3 -m venv .venv

# Activate it (Mac/Linux)
source .venv/bin/activate

# Activate it (Windows)
# .venv\Scripts\activate

# You should see (.venv) in your terminal prompt
```

### Step 3: Install Dependencies

```bash
# Install all required packages
pip install -r requirements.txt

# This installs: FastAPI, SQLAlchemy, Alembic, python-dotenv, etc.
```

### Step 4: Set Up Environment Variables

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env file with your settings (or keep defaults for local development)
# The defaults work fine for getting started!
```

### Step 5: Set Up the Database

```bash
# Create the database tables
alembic upgrade head

# You should see: "Running upgrade -> xxxxx, initial schema"
```

### Step 6: Start the Application

```bash
# Run the development server
uvicorn src.main:app --reload

# You should see:
# INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

### Step 7: Test That Everything Works

**🌐 Using your web browser:**

1. Visit http://127.0.0.1:8000 - should show: `{"status":"OK","message":"Pluto API is running"}`
2. Visit http://127.0.0.1:8000/docs - interactive API documentation (try creating users!)

**🔧 Using curl (if you have it):**

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

## 🔧 Common Issues & Solutions

**❌ `python: command not found`**
✅ Use `python3` instead of `python`

**❌ `ERROR: Address already in use`**
✅ Another instance is running. Stop it with `Ctrl+C` or change the port in `.env`

**❌ `ModuleNotFoundError`**
✅ Make sure your virtual environment is activated: `source .venv/bin/activate`

**❌ Database errors**
✅ Run `alembic upgrade head` to create/update database tables

**❌ `alembic: command not found`**
✅ Virtual environment isn't activated or dependencies aren't installed

## 🧪 Learning to Add Tests (No Tests Yet - Let's Build Them!)

**Important**: This project doesn't have tests yet - this is your chance to learn how to add them!

### Why Tests Matter

- Ensure your code works correctly
- Prevent bugs when making changes
- Help you understand how code should behave
- Industry standard practice

### Quick Test Setup

1. **Install test dependencies:**

```bash
# Make sure virtual environment is active
source .venv/bin/activate

# Install testing packages
pip install pytest pytest-asyncio httpx

# Save to requirements
pip freeze > requirements.txt
```

2. **Create test structure:**

```bash
# Create directories
mkdir -p tests/{unit,integration,e2e}/{domain,application,infrastructure,api}

# Add Python package files
find tests -type d -exec touch {}/__init__.py \;
```

3. **Write your first test** (`tests/unit/domain/test_user_entity.py`):

```python
"""Test User domain entity - your first test!"""

from src.domain.entities.user import User
from src.domain.enums.user_enums import UserStatus

def test_user_creation():
    """Test creating a user entity."""
    # Arrange & Act
    user = User(
        user_id=1,
        username="testuser", 
        email="test@example.com",
        status=UserStatus.ACTIVE
    )
  
    # Assert
    assert user.user_id == 1
    assert user.user_name == "testuser"
    assert user.user_email == "test@example.com"
    assert user.user_status == UserStatus.ACTIVE

def test_user_deactivate():
    """Test user deactivation."""
    # Arrange
    user = User(1, "testuser", "test@example.com", UserStatus.ACTIVE)
  
    # Act  
    user.deactivate()
  
    # Assert
    assert user.user_status == UserStatus.INACTIVE
```

4. **Run your tests:**

```bash
pytest tests/ -v
```

### Test Types to Learn

**🔹 Unit Tests** (`tests/unit/`): Test individual components in isolation
**🔹 Integration Tests** (`tests/integration/`): Test components working together
**🔹 E2E Tests** (`tests/e2e/`): Test complete user workflows via API

This gives you a foundation to build comprehensive test coverage as you learn!

## 🏗️ Architecture Overview

This project follows **Clean Architecture** principles:

### 🧠 Domain Layer (`src/domain/`)

- **Pure business logic** - no external dependencies
- **Entities**: Core business objects (`User`)
- **Repositories**: Interfaces for data access (contracts only)
- **Exceptions**: Business rule violations

### 🔧 Application Layer (`src/application/`)

- **Use cases and services** - coordinates business operations
- **DTOs**: Data transfer between layers
- **Services**: Application business logic using domain entities

### 🔌 Infrastructure Layer (`src/infrastructure/`)

- **External concerns** - databases, file systems, APIs
- **Repository implementations** using SQLAlchemy
- **Database models** and migrations

### 🌐 Presentation Layer (`src/presentation/`)

- **HTTP API** using FastAPI
- **Controllers/Endpoints** that handle HTTP requests
- **Request/Response** formatting

### ⚙️ Configuration (`src/properties/`)

- **Environment-based settings** using python-dotenv
- **Centralized configuration** management

## 🔄 Complete Guide: Adding New Features

This comprehensive step-by-step guide shows exactly how to add a new feature (e.g., "Product") to the system. **Follow every step in order** - this is the complete workflow used by professional developers.

### 📋 Overview: What We'll Build

We'll add a Product feature with these operations:

- Create product
- Get product by ID
- Get all products
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

# Review the generated file in: migrations/alembic/versions/
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

from src.application.dto.product_dto import ProductDTO
from src.domain.repositories.product_repository import ProductRepository

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

Update `src/presentation/api/dependencies.py` by adding these imports and functions:

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

Add these classes to `src/presentation/api/models.py`:

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

@router.put(
    "/{product_id}",
    response_model=ProductResponse,
    summary="Update product",
)
async def update_product(
    product_id: int,
    product_data: ProductUpdate,
    product_service: ProductService = Depends(get_product_service),
):
    """Update an existing product."""
    try:
        # Get existing product first
        existing_product = product_service.get_product_by_id(product_id)
        if not existing_product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with ID {product_id} not found",
            )
      
        # Update only provided fields
        updated_dto = ProductDTO(
            id=product_id,
            name=product_data.name if product_data.name else existing_product.name,
            price=product_data.price if product_data.price else existing_product.price,
            description=product_data.description if product_data.description else existing_product.description,
        )
      
        updated_product = product_service.update_product(updated_dto)
        return _dto_to_response(updated_product)
    except ProductNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )

@router.delete(
    "/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete product",
)
async def delete_product(
    product_id: int,
    product_service: ProductService = Depends(get_product_service),
):
    """Delete a product by ID."""
    success = product_service.delete_product(product_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {product_id} not found",
        )
```

### Step 8: Register Router in Main Application

**What**: Tell FastAPI about your new endpoints

Update `src/main.py` by adding these lines:

```python
# Add this import at the top
from src.presentation.api.endpoints.product.product_endpoints import router as product_router

# Add this line after the existing router registration
app.include_router(product_router, prefix="/api")
```

### Step 9: Test Your New Feature

**What**: Verify everything works correctly

#### 9.1 Start the Application

```bash
# Make sure you're in virtual environment
source .venv/bin/activate

# Start the server
uvicorn src.main:app --reload
```

#### 9.2 Test the API

**Using Browser (Interactive API docs):**

1. Visit http://127.0.0.1:8000/docs
2. Find the "products" section
3. Try creating a product using the POST endpoint
4. Try getting the product back using GET endpoint

**Using curl:**

```bash
# Create a product
curl -X POST http://127.0.0.1:8000/api/products \
  -H "Content-Type: application/json" \
  -d '{"name":"Laptop","price":999.99,"description":"High-performance laptop"}'

# Get all products
curl http://127.0.0.1:8000/api/products

# Get specific product
curl http://127.0.0.1:8000/api/products/1

# Update a product
curl -X PUT http://127.0.0.1:8000/api/products/1 \
  -H "Content-Type: application/json" \
  -d '{"name":"Gaming Laptop","price":1299.99}'

# Delete a product
curl -X DELETE http://127.0.0.1:8000/api/products/1
```

### 🎉 Congratulations!

You've successfully added a complete new feature following Clean Architecture principles. Your students now understand:

- **Domain Layer**: Business entities, rules, and interfaces
- **Application Layer**: Use cases and DTOs
- **Infrastructure Layer**: Database models and repository implementations
- **Presentation Layer**: HTTP APIs and request/response handling
- **Dependency Injection**: How layers communicate without tight coupling

This is the exact workflow professional developers use in enterprise applications!

### Next Steps for Students

1. **Add validation** to your domain entities
2. **Add more business rules** (e.g., product categories, inventory)
3. **Add error handling** for edge cases
4. **Add tests** for each layer
5. **Add logging** throughout the application

## 🚀 Quick Database Changes

### Making Database Changes

```bash
# 1. Modify your models in src/infrastructure/database/models/
# 2. Generate migration
alembic revision --autogenerate -m "describe your changes"

# 3. Review the generated migration file
# 4. Apply migration
alembic upgrade head
```

## 📚 Key Technologies

- **[FastAPI](https://fastapi.tiangolo.com/)** - Modern, fast web framework with automatic API docs
- **[SQLAlchemy](https://www.sqlalchemy.org/)** - Powerful ORM for database operations
- **[Alembic](https://alembic.sqlalchemy.org/)** - Database migration tool
- **[Pydantic](https://pydantic-docs.helpmanual.io/)** - Data validation using Python type annotations
- **[python-dotenv](https://pypi.org/project/python-dotenv/)** - Environment variable management

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes following the architecture principles
4. Add tests for your changes
5. Commit your changes (`git commit -m 'Add some amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## 📝 Learning Resources

- **Clean Architecture**: Robert C. Martin's "Clean Architecture" [book](https://agorism.dev/book/software-architecture/%28Robert%20C.%20Martin%20Series%29%20Robert%20C.%20Martin%20-%20Clean%20Architecture_%20A%20Craftsman’s%20Guide%20to%20Software%20Structure%20and%20Design-Prentice%20Hall%20%282017%29.pdf) 
- **FastAPI Tutorial**: https://fastapi.tiangolo.com/tutorial/
- **SQLAlchemy Tutorial**: https://docs.sqlalchemy.org/en/20/tutorial/
- **Python Type Hints**: https://docs.python.org/3/library/typing.html

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**🎓 Happy Learning!** This project is designed to grow with you as you master clean architecture and modern Python development.
