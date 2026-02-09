# Frontend Setup Guide

## Quick Start

### 1. Start the Backend Server

```bash
cd c:\Users\sabas\Documents\pluto
python run.py
```

The API will be available at `http://localhost:8000`

### 2. Open the Frontend

Simply open `frontend/index.html` in your web browser:

- **Option 1**: Double-click `frontend/index.html`
- **Option 2**: Right-click → "Open with" → Your preferred browser
- **Option 3**: Use VS Code's Live Server extension

The frontend will be available at `file:///c:/Users/sabas/Documents/pluto/frontend/index.html`

### 3. Test the Application

1. **Register a new account**
   - Click "Register" button
   - Fill in username, email, and password (must meet complexity requirements)
   - Password must contain: uppercase, lowercase, numbers, special characters, min 12 chars

2. **Browse Products**
   - Products load automatically on the Products page
   - Filter by category using the dropdown
   - Search for products using the search box

3. **Add to Cart**
   - Click "Add to Cart" on any product
   - Adjust quantity in the cart
   - View cart summary with tax calculation (10%)

4. **Checkout**
   - Fill in shipping address
   - Select payment method
   - Click "Complete Order"

## CORS Configuration

If you see CORS errors in the browser console, add CORS middleware to the backend:

In `src/core/middleware.py` or `src/main.py`:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## API Configuration

The frontend is configured to connect to `http://localhost:8000/api`

To change the API URL, edit `frontend/js/api.js`:

```javascript
const API_BASE_URL = 'http://localhost:8000/api'; // Change this URL if needed
```

## Database Initialization

The database is automatically created when you run:

```bash
python run.py
```

To reset the database and run migrations:

```bash
# Remove the old database
rm pluto.db

# Run migrations
alembic upgrade head

# Start the server
python run.py
```

## Testing API Endpoints

You can test the API endpoints using:

1. **Postman** (import the collection if available)
2. **cURL commands**
3. **Frontend application** (recommended - most realistic test)

Example cURL to register:

```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "SecurePass123!"
  }'
```

## Troubleshooting

### Products Not Loading
- Check that backend is running on `localhost:8000`
- Open browser DevTools (F12) → Network tab
- Verify API request to `/api/products` returns 200 status

### Login Not Working
- Check password meets requirements:
  - Minimum 12 characters
  - At least one uppercase letter
  - At least one lowercase letter
  - At least one digit
  - At least one special character

### CORS Errors
- Backend CORS middleware may not be enabled
- Check browser console for specific error
- Add CORS middleware to backend (see above)

### Cart Not Persisting
- This is a demo - cart is stored in browser memory
- Refresh page clears the cart
- To persist, implement backend cart storage

### Token Issues
- Check browser DevTools → Application → Local Storage
- Look for `auth_token` key
- Delete and try logging in again if issues persist

## Running Tests

```bash
# Run all tests
pytest -v

# Run specific test file
pytest tests/integration/test_auth_endpoints.py -v

# Run with coverage
pytest --cov=src tests/
```

## Development Tips

### Adding New API Endpoints

1. Add endpoint method to `frontend/js/api.js`
2. Call the method in `frontend/js/app.js`
3. Update UI in `frontend/index.html`
4. Add styling to `frontend/styles/main.css`

### Debugging JavaScript

1. Open browser DevTools: `F12` or `Ctrl+Shift+I`
2. Check Console tab for errors
3. Check Network tab for API requests
4. Set breakpoints in Sources tab

### Modifying Styles

1. Edit `frontend/styles/main.css`
2. Refresh browser (Ctrl+R) to see changes
3. Check mobile view with DevTools (Ctrl+Shift+M)

## Production Deployment

### Before Deploying to Production:

1. **Change SECRET_KEY** in `.env`:
   ```
   SECRET_KEY=your-very-secure-random-key-here
   ```

2. **Set DEBUG=False** in `.env`:
   ```
   DEBUG=False
   ```

3. **Update API_BASE_URL** in `frontend/js/api.js`:
   ```javascript
   const API_BASE_URL = 'https://your-production-api.com/api';
   ```

4. **Enable HTTPS** - Use a proper SSL certificate

5. **Review Security Settings**:
   - Check CORS is properly configured
   - Verify password hashing is enabled
   - Review JWT token expiration

6. **Run Security Tests**:
   ```bash
   pytest -v  # Run all tests
   ```

## File Structure

```
pluto/
├── frontend/                    # Frontend application
│   ├── index.html              # Main HTML template
│   ├── README.md               # Frontend documentation
│   ├── js/
│   │   ├── api.js             # API client
│   │   └── app.js             # App logic
│   └── styles/
│       └── main.css           # Styles
├── src/                         # Backend source code
│   ├── main.py                # App entry point
│   ├── application/           # Services and DTOs
│   ├── domain/                # Business logic
│   ├── infrastructure/        # Database and config
│   ├── core/                  # Middleware and security
│   └── properties/            # Settings
├── requirements.txt            # Python dependencies
├── run.py                      # Start the app
└── alembic.ini               # Database migrations config
```

## Next Steps

1. ✅ Start backend: `python run.py`
2. ✅ Open frontend: Open `frontend/index.html`
3. ✅ Register user and test features
4. ✅ Review the code and customize as needed
5. ✅ Deploy to production when ready

## Support & Documentation

- **API Documentation**: Available at `http://localhost:8000/docs` (Swagger UI)
- **Frontend README**: `frontend/README.md`
- **Production Guide**: `PRODUCTION_IMPLEMENTATION.md`
- **Testing Guide**: `TESTING_GUIDE.md`

---

**Happy coding! 🚀**
