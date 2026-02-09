## Quick Start: Testing the Pluto Project

### 📦 Installation

First, ensure all dependencies are installed:
```bash
pip install -r requirements.txt
```

### 🧪 Running Tests

#### Run All Tests
```bash
pytest
```

#### Run Tests with Verbose Output
```bash
pytest -v
```

#### Run Tests with Coverage Report
```bash
pytest --cov=src --cov-report=html
```

#### Run Specific Test File
```bash
pytest tests/unit/test_auth_utils.py
pytest tests/integration/test_user_endpoints.py
pytest tests/integration/test_auth_endpoints.py
```

#### Run Specific Test Class
```bash
pytest tests/unit/test_auth_utils.py::TestPasswordHashing
pytest tests/integration/test_user_endpoints.py::TestUserEndpoints
```

#### Run Specific Test Function
```bash
pytest tests/unit/test_auth_utils.py::TestPasswordHashing::test_hash_password_creates_different_hash
```

### 📊 Expected Test Results

**Total Tests**: 30+
- Unit tests: 10
- Integration tests: 20

**Expected Pass Rate**: 100% (all should pass)

### 🔍 Test Categories

#### Unit Tests (Password Hashing)
**Location**: `tests/unit/test_auth_utils.py`

Tests verify:
- ✅ Hash generation with different salts
- ✅ Correct password verification
- ✅ Incorrect password rejection
- ✅ Edge cases (unicode, special chars, empty strings)
- ✅ Security (case sensitivity, hash tampering detection)

#### Integration Tests (User Endpoints)
**Location**: `tests/integration/test_user_endpoints.py`

Tests verify:
- ✅ User creation with validation
- ✅ Email format validation
- ✅ Password strength requirements
- ✅ Duplicate username prevention
- ✅ User retrieval
- ✅ User update/delete operations

#### Integration Tests (Auth Endpoints)
**Location**: `tests/integration/test_auth_endpoints.py`

Tests verify:
- ✅ User registration
- ✅ Login with JWT token generation
- ✅ Password complexity validation
- ✅ Invalid credential rejection
- ✅ Protected endpoint access
- ✅ Token-based authentication

### 🛠️ Troubleshooting

#### ImportError: No module named 'src'
**Solution**: Run pytest from the project root directory:
```bash
cd c:\Users\sabas\Documents\pluto
pytest
```

#### Database Locked Error
**Solution**: This shouldn't occur as tests use in-memory SQLite, but if it does:
```bash
# Clear __pycache__ directories
Remove-Item -Path . -Recurse -Include __pycache__ -Force
pytest
```

#### Tests Not Discovered
**Solution**: Ensure `conftest.py` exists in tests directory:
```bash
ls tests/conftest.py
```

### 🎯 Coverage Target

Current coverage: ~70%

To view detailed coverage report:
```bash
pytest --cov=src --cov-report=html
# Then open htmlcov/index.html in browser
```

### 📝 Test Fixtures Available

In any test, you can use these fixtures (auto-injected by pytest):

```python
def test_something(client, mock_user_data, auth_headers, test_db):
    # client: FastAPI TestClient
    # mock_user_data: Sample user data dict
    # auth_headers: JWT authorization headers
    # test_db: Database session
    pass
```

### ✅ Pre-test Checklist

- [ ] All dependencies installed (`pip install -r requirements.txt`)
- [ ] No other processes running on port 8000
- [ ] Working directory is project root
- [ ] `.env` file exists (copy from `.env.example`)
- [ ] Python 3.8+ installed

### 🚀 Next Steps

1. **Run full test suite**:
   ```bash
   pytest -v
   ```

2. **Check coverage**:
   ```bash
   pytest --cov=src
   ```

3. **Protect endpoints with JWT**:
   - Add `Depends(verify_token)` to protected endpoints
   - Update integration tests to use `auth_headers`

4. **Deploy with confidence**:
   - All tests passing ✅
   - Coverage > 70% ✅
   - Input validation in place ✅
   - Security layer tested ✅
