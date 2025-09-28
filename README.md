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

## 🚀 Development Workflow

### Making Database Changes
```bash
# 1. Modify your models in src/infrastructure/database/models/
# 2. Generate migration
alembic revision --autogenerate -m "describe your changes"

# 3. Review the generated migration file
# 4. Apply migration
alembic upgrade head
```

### Adding New Features
1. **Start with Domain**: Add entities, value objects, repository interfaces
2. **Application Layer**: Create DTOs and services using domain
3. **Infrastructure**: Implement repositories, database models
4. **Presentation**: Add API endpoints that use application services
5. **Tests**: Write tests for each layer

### Code Style
- Follow PEP 8 Python style guidelines
- Use type hints for better code documentation
- Keep functions focused on single responsibilities
- Use descriptive variable and function names

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

- **Clean Architecture**: Robert C. Martin's "Clean Architecture" book
- **FastAPI Tutorial**: https://fastapi.tiangolo.com/tutorial/
- **SQLAlchemy Tutorial**: https://docs.sqlalchemy.org/en/20/tutorial/
- **Python Type Hints**: https://docs.python.org/3/library/typing.html

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**🎓 Happy Learning!** This project is designed to grow with you as you master clean architecture and modern Python development.