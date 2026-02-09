# Pluto Frontend & Backend Troubleshooting Guide

## Common Issues & Solutions

### Backend Won't Start

#### Error: `ModuleNotFoundError: No module named 'src'`

**Cause**: Wrong working directory

**Solution**:
```bash
# Make sure you're in the project root directory
cd c:\Users\sabas\Documents\pluto

# Then run
python run.py
```

---

#### Error: `sqlite3.OperationalError: unable to open database file`

**Cause**: Missing database file or permission issues

**Solution**:
```bash
# Recreate database
rm pluto.db  # Delete old database

# Run migrations
alembic upgrade head

# Start backend
python run.py
```

---

#### Error: `Address already in use`

**Cause**: Port 8000 is already in use

**Solution**:
```bash
# Find process using port 8000
lsof -i :8000  # On Linux/Mac

# OR (Windows) - Find and kill it
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Then restart backend
python run.py
```

OR change the port in `run.py`:
```python
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)  # Change 8000 to 8001
```

---

#### Error: `ImportError: cannot import name 'X' from 'src.domain.enums'`

**Cause**: Missing enum definition

**Solution**:
1. Check the specific enum file (e.g., `src/domain/enums/product_enums.py`)
2. Verify the enum class is defined
3. If missing, add the enum class definition
4. Restart backend

Example fix:
```python
# src/domain/enums/product_enums.py
from enum import Enum

class ProductStatus(Enum):
    AVAILABLE = "available"
    OUT_OF_STOCK = "out_of_stock"
    DISCONTINUED = "discontinued"
    ARCHIVED = "archived"
```

---

### Frontend Won't Load

#### Issue: Blank white page

**Cause**: JavaScript errors preventing page load

**Solution**:
1. Open browser DevTools: `F12`
2. Go to Console tab
3. Check for red errors
4. Fix the reported errors
5. Refresh page: `Ctrl+R`

**Common errors**:
- `Uncaught ReferenceError: api is not defined`
  - Solution: Check that `api.js` is included in `index.html` before `app.js`

- `Uncaught SyntaxError: Unexpected token`
  - Solution: Check for syntax errors in JavaScript files

---

#### Issue: Styles not loading (page looks broken)

**Cause**: CSS file not found or wrong path

**Solution**:
1. Check file path in HTML:
   ```html
   <link rel="stylesheet" href="styles/main.css">  <!-- Correct -->
   ```
2. Verify file exists: `frontend/styles/main.css`
3. Hard refresh browser: `Ctrl+Shift+R`

---

#### Issue: Products page shows "undefined" instead of products

**Cause**: API not returning data or error in rendering

**Solution**:
1. Check backend is running: `python run.py`
2. Open DevTools (F12) → Network tab
3. Go to Products section
4. Look for request to `/api/products`
5. Check response:
   - Status 200 = success
   - Status 500 = server error
   - Status 0 = connection refused

**If request returns 500**:
```bash
# Check backend logs in terminal
python run.py  # Look for error messages
```

**If request returns 0 (connection refused)**:
```bash
# Verify backend is running
python run.py

# Verify it's on port 8000
curl http://localhost:8000/docs  # Should open Swagger UI
```

---

### Authentication Issues

#### Issue: Login fails with "Invalid username or password"

**Possible causes**:
1. User doesn't exist
2. Password is wrong
3. Password doesn't meet requirements

**Solution**:
1. Check if user exists in database:
   ```bash
   sqlite3 pluto.db "SELECT username, email FROM user WHERE username='testuser';"
   ```

2. If user doesn't exist, register first

3. Verify password meets requirements:
   - Minimum 12 characters
   - At least 1 uppercase letter
   - At least 1 lowercase letter
   - At least 1 digit
   - At least 1 special character

Example valid password: `SecurePass123!`

---

#### Issue: Register shows password validation error

**Cause**: Password doesn't meet complexity requirements

**Solution**:
Use a password that meets all requirements:
- `SecurePass123!`
- `MyP@ssw0rd2024`
- `TestPass@123`

---

#### Issue: Token not saved to localStorage

**Cause**: Browser blocking localStorage or HTTPS/HTTP mismatch

**Solution**:
1. Check browser settings allow localStorage
2. Check DevTools → Application → Local Storage
3. Should see `auth_token` key after login
4. If not, check console for CORS errors

To manually set token for testing:
```javascript
// In DevTools Console
localStorage.setItem('auth_token', 'your-token-here');
```

---

#### Issue: "403 Unauthorized" on protected endpoints

**Cause**: Invalid or missing JWT token

**Solution**:
1. Login again to get fresh token
2. Check token in localStorage
3. Clear localStorage and re-login:
   ```javascript
   // In DevTools Console
   localStorage.clear();
   // Then login again in frontend
   ```

---

### Cart Issues

#### Issue: Cart is empty after refresh

**This is expected behavior** - Frontend cart is in-memory only

**Solution** (optional):
To persist cart, implement backend cart storage:
1. Store cart_id in session
2. Implement persistent cart API
3. Load cart on page load

Temporary workaround - save to localStorage:
```javascript
// In app.js, after updating cart
localStorage.setItem('cart_items', JSON.stringify(appState.cartItems));

// On page load
appState.cartItems = JSON.parse(localStorage.getItem('cart_items')) || [];
```

---

#### Issue: Cart total doesn't match (wrong tax calculation)

**Cause**: Tax calculation is hardcoded to 10%

**Solution**:
If you need different tax rate, edit `app.js`:
```javascript
// Find this line in updateCartUI()
const tax = subtotal * 0.10;  // Change 0.10 to your rate (e.g., 0.08 for 8%)
```

---

### API Issues

#### Issue: "CORS error - No 'Access-Control-Allow-Origin' header"

**Cause**: Backend doesn't have CORS enabled

**Solution**:
Add CORS middleware to backend. Edit `src/main.py`:
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Then restart backend: `python run.py`

---

#### Issue: API returns 500 error (Internal Server Error)

**Cause**: Backend error - check backend logs

**Solution**:
1. Look at backend terminal for error messages
2. Check backend logs for details
3. Common causes:
   - Database connection error
   - Missing data in request
   - Invalid data type
   - Unhandled exception

**Debug**:
```bash
# Run backend with verbose output
python run.py  # Watch for error messages
```

---

#### Issue: API timeout (request takes very long)

**Cause**: Backend processing slowly or database issue

**Solution**:
1. Check backend is running: `python run.py`
2. Check database isn't locked:
   ```bash
   sqlite3 pluto.db ".open"  # Should open without errors
   ```
3. Check if there's a lot of data in database
4. Consider adding pagination to API

---

### Database Issues

#### Issue: "database is locked"

**Cause**: Another process accessing database

**Solution**:
```bash
# Close any open connections
# End any running backends (Ctrl+C)

# Verify database is accessible
sqlite3 pluto.db ".tables"

# Start backend fresh
python run.py
```

---

#### Issue: Data doesn't persist after restart

**Cause**: Database not being created properly

**Solution**:
```bash
# Check database exists
ls -la pluto.db  # Should show file size > 0

# Check tables exist
sqlite3 pluto.db ".tables"  # Should list tables

# Recreate if needed
rm pluto.db
alembic upgrade head
python run.py
```

---

#### Issue: "Column 'X' does not exist"

**Cause**: Migration not applied

**Solution**:
```bash
# Apply all migrations
alembic upgrade head

# Check migration history
alembic history

# Verify column exists
sqlite3 pluto.db "PRAGMA table_info(user);"  # For user table
```

---

### UI/UX Issues

#### Issue: Modal doesn't close

**Cause**: Event listener not working or modal is hidden

**Solution**:
1. Click the X button (top right of modal)
2. Press ESC key
3. Click outside the modal

If none work:
```javascript
// In DevTools Console
document.getElementById('loginModal').style.display = 'none';
// or
document.getElementById('registerModal').style.display = 'none';
```

---

#### Issue: Buttons don't respond

**Cause**: JavaScript error preventing event listeners

**Solution**:
1. Check DevTools Console (F12) for errors
2. Verify button has correct id in HTML
3. Verify event listener is added in app.js
4. Refresh page: `Ctrl+R`

---

#### Issue: Page looks wrong on mobile

**Cause**: CSS media queries not working

**Solution**:
1. Check viewport meta tag in HTML:
   ```html
   <meta name="viewport" content="width=device-width, initial-scale=1.0">
   ```

2. Test responsive design with DevTools:
   - Open DevTools: `F12`
   - Click mobile icon (Ctrl+Shift+M)
   - Select different device sizes

---

### Performance Issues

#### Issue: Frontend loads slowly

**Cause**: Large files or slow network

**Solution**:
1. Minimize HTTP requests
2. Combine CSS/JS files
3. Compress images
4. Check network tab (F12 → Network) for slow requests

---

#### Issue: Backend responds slowly

**Cause**: Database queries slow or lots of data

**Solution**:
1. Add indexes to frequently queried fields:
   ```python
   # In models, add index
   username = Column(String, index=True)
   ```

2. Use pagination for large datasets:
   ```bash
   GET /api/products?skip=0&limit=10
   ```

3. Check database size:
   ```bash
   ls -lh pluto.db  # Check file size
   sqlite3 pluto.db "SELECT COUNT(*) FROM product;"  # Count products
   ```

---

### Testing Issues

#### Issue: Tests fail to run

**Cause**: pytest not installed

**Solution**:
```bash
# Install pytest
pip install pytest pytest-cov

# Run tests
pytest -v

# Run with coverage
pytest --cov=src tests/
```

---

#### Issue: Tests show import errors

**Cause**: src not in Python path

**Solution**:
```bash
# Add current directory to Python path
set PYTHONPATH=%PYTHONPATH%;c:\Users\sabas\Documents\pluto

# Then run tests
pytest -v
```

Or modify `conftest.py`:
```python
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
```

---

## Quick Debug Checklist

When something goes wrong:

- [ ] Backend running? → `python run.py`
- [ ] Frontend file exists? → Check `frontend/index.html`
- [ ] API responding? → Check Network tab (F12)
- [ ] JavaScript errors? → Check Console tab (F12)
- [ ] CSS loading? → Check Network tab for main.css
- [ ] Database exists? → Check `pluto.db` file
- [ ] Ports correct? → Backend on 8000, Frontend on file://
- [ ] CORS enabled? → Check backend middleware
- [ ] Tokens working? → Check localStorage
- [ ] Data valid? → Check request/response in Network tab

---

## Getting Help

### 1. Check the Logs

**Backend logs**:
```bash
# Terminal where you ran python run.py
# Shows error messages and HTTP requests
```

**Frontend logs**:
```bash
# Open DevTools: F12
# Console tab shows all errors and logs
# Network tab shows API requests
```

### 2. Check Documentation

- `frontend/README.md` - Frontend overview
- `FRONTEND_SETUP.md` - Setup instructions
- `FRONTEND_INTEGRATION.md` - Architecture details
- `TESTING_GUIDE.md` - Testing instructions
- `PRODUCTION_IMPLEMENTATION.md` - Production tips

### 3. Debug Tools

**Browser DevTools** (F12):
- Console: JavaScript errors
- Network: API requests
- Application: LocalStorage, Cookies
- Sources: Set breakpoints, step through code
- Performance: Check page load speed

**Database Tools**:
```bash
# Open database
sqlite3 pluto.db

# Common queries
.tables                          # List all tables
.schema user                     # Show user table structure
SELECT * FROM user;            # View all users
SELECT COUNT(*) FROM product;  # Count products
```

**API Testing**:
```bash
# Use curl to test API
curl http://localhost:8000/api/products
curl http://localhost:8000/docs  # Swagger UI
```

---

## Performance Optimization Tips

### Frontend Optimization
```javascript
// Use debounce for search
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Use in app.js
const debouncedSearch = debounce(searchProducts, 300);
```

### Backend Optimization
```python
# Add pagination
@router.get("/products")
async def list_products(skip: int = 0, limit: int = 10):
    # Returns only 10 items, better performance
    return repository.list_products(skip, limit)
```

---

## Security Best Practices

1. **Never commit secrets**:
   ```bash
   # Add to .gitignore
   echo ".env" >> .gitignore
   ```

2. **Use environment variables**:
   ```bash
   # In .env
   SECRET_KEY=your-secret-key-here
   DEBUG=False
   ```

3. **Validate all inputs**:
   ```javascript
   // Frontend validation
   if (!email.includes('@')) {
       showAlert('Invalid email', 'error');
       return;
   }
   ```

4. **Hash passwords**:
   ```python
   # Backend uses bcrypt automatically
   # Never store plain text passwords
   ```

5. **Use HTTPS in production**:
   ```python
   # In production, use HTTPS
   # Not needed for local development
   ```

---

**Still having issues?** 

1. Check the error message carefully
2. Look at the logs (backend terminal or browser console)
3. Search for similar issues in documentation
4. Test individual components (API, database, frontend)
5. Create minimal test case to isolate issue

---

**Version**: 1.0.0
**Last Updated**: 2024
