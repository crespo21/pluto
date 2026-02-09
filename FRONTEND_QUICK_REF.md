# Quick Reference: Pluto Frontend

## Start the App

```bash
# 1. Start Backend
cd c:\Users\sabas\Documents\pluto
python run.py

# 2. Open Frontend
# Double-click: frontend/index.html
# Or open in browser: file:///c:/Users/sabas/Documents/pluto/frontend/index.html
```

## Project Structure

```
frontend/
├── index.html          # UI Template
├── js/
│   ├── api.js         # API Client
│   └── app.js         # App Logic  
└── styles/
    └── main.css       # Styles
```

## File Locations

| File | Purpose |
|------|---------|
| `frontend/index.html` | HTML template with all UI elements |
| `frontend/js/api.js` | API client - handles all HTTP requests |
| `frontend/js/app.js` | Main logic - event handlers and state |
| `frontend/styles/main.css` | Responsive stylesheet |
| `frontend/README.md` | Frontend documentation |
| `FRONTEND_SETUP.md` | Setup instructions |
| `FRONTEND_INTEGRATION.md` | Integration guide |

## Key API Methods

### Authentication
```javascript
api.register(username, email, password)   // Create account
api.login(username, password)             // Login
api.logout()                              // Logout
api.isAuthenticated()                     // Check if logged in
```

### Products
```javascript
api.listProducts()                        // Get all products
api.getProduct(productId)                 // Get one product
api.searchProducts(query)                 // Search products
```

### Categories
```javascript
api.listCategories()                      // Get all categories
api.getCategory(categoryId)               // Get one category
```

### Cart
```javascript
api.createCart()                          // Create new cart
api.getCart(cartId)                       // Get cart items
api.addToCart(cartId, productId, qty)     // Add item
api.removeFromCart(cartId, itemId)        // Remove item
api.updateCartItem(cartId, itemId, qty)   // Update quantity
api.clearCart(cartId)                     // Clear cart
```

### Checkout
```javascript
api.createCheckout(cartId, address, method)  // Create order
api.processPayment(checkoutId)               // Process payment
```

## State Object (appState)

```javascript
appState = {
    currentUser: null,           // Logged-in user
    products: [],                // All products
    categories: [],              // All categories
    cartItems: [],               // Items in cart
    cartId: null,                // Current cart ID
    currentSection: 'home',      // Active page
}
```

## Page Sections

| Section | ID | Function |
|---------|----|----|
| Home | `home` | Hero section with welcome |
| Products | `products` | Browse and filter products |
| Cart | `cart` | View and manage cart |
| Checkout | `checkout` | Shipping and payment |
| Modals | N/A | Login and register forms |

## UI Elements

### Login Modal
- Username field
- Password field
- Submit button
- Register link
- Close button (X or ESC)

### Register Modal
- Username field
- Email field  
- Password field
- Submit button
- Login link
- Password requirements shown

### Product Grid
- Product card (image, name, price, category)
- "Add to Cart" button
- Category filter dropdown
- Search box
- "View Details" link (optional)

### Cart Table
- Product name
- Unit price
- Quantity (with +/- buttons)
- Line total
- Remove button (trash icon)
- Subtotal / Tax / Total display

### Checkout Form
- Shipping address fields
- Payment method selector
- Order summary
- Complete Order button

## Authentication Flow

```
1. User clicks Register/Login
2. Modal opens
3. User fills form
4. Submit → api.register() or api.login()
5. If success:
   - Token saved to localStorage
   - User info saved to appState
   - UI updates with user name
   - Modal closes
6. If error:
   - Error message shown
   - User can retry
```

## Add to Cart Flow

```
1. User clicks "Add to Cart"
2. addToCart(productId, name, price) called
3. Check if item already in cart
4. If yes: increase quantity
5. If no: add new item
6. Update appState.cartItems
7. Refresh cart UI
8. Show success alert
9. Update cart badge (item count)
```

## Common Issues & Fixes

| Issue | Fix |
|-------|-----|
| Products not loading | Restart backend: `python run.py` |
| Login fails | Check password meets requirements (12+ chars, complex) |
| CORS errors | Enable CORS in backend |
| Cart not saving | Cart is in-memory; refresh clears it |
| API not responding | Check backend is running on localhost:8000 |

## Configuration

### Change API URL
Edit `frontend/js/api.js`:
```javascript
const API_BASE_URL = 'http://localhost:8000/api';  // Change here
```

### Change Colors
Edit `frontend/styles/main.css`:
```css
:root {
    --primary-color: #007bff;     /* Change primary color */
    --secondary-color: #6c757d;   /* Change secondary color */
    --success-color: #28a745;     /* Change success color */
    /* ... more colors ... */
}
```

### Change Branding
Edit `frontend/index.html`:
```html
<!-- Change logo text (line ~50) -->
<div class="navbar-logo">🚀 Pluto Shop</div>

<!-- Change page title (line ~9) -->
<title>Pluto E-Commerce Platform</title>
```

## Browser DevTools Tips

### Check API Calls
1. Open DevTools: `F12`
2. Go to Network tab
3. Perform action (login, add to cart, etc.)
4. See request/response details
5. Check status code (200 = OK, 401 = unauthorized, 400 = bad request)

### Debug JavaScript
1. Open DevTools: `F12`
2. Go to Console tab
3. Type JavaScript commands
4. Set breakpoints in Sources tab
5. Step through code execution

### Check Local Storage
1. Open DevTools: `F12`
2. Go to Application tab
3. Click Local Storage → file:// (or your domain)
4. See `auth_token` key with JWT token value

## Password Requirements

Passwords must have:
- ✓ Minimum 12 characters
- ✓ At least 1 uppercase letter (A-Z)
- ✓ At least 1 lowercase letter (a-z)
- ✓ At least 1 digit (0-9)
- ✓ At least 1 special character (!@#$%^&*)

Example valid password: `SecurePass123!`

## Responsive Breakpoints

| Device | Width | Behavior |
|--------|-------|----------|
| Mobile | < 480px | Single column, large buttons |
| Tablet | 480-768px | 2 columns, adjusted spacing |
| Desktop | > 768px | 3+ columns, full layout |

## Password Hashing

The app uses **bcrypt** for password security:
- Passwords never stored in plain text
- Each password hashed with 10 rounds
- Slow by design (~100ms per hash)
- Makes brute force attacks impractical

## Token Storage

JWT tokens stored in browser `localStorage`:
- Key: `auth_token`
- Format: `eyJhbGc...` (JWT format)
- Persists across page refreshes
- Cleared on logout
- Cleared if user deletes browser data

## API Error Format

```javascript
{
    status: 400,                           // HTTP status code
    message: "Invalid request data",       // Error message
    details: [                             // Validation details
        {
            field: "password",
            msg: "Password must be at least 12 characters",
            type: "value_error"
        }
    ]
}
```

## Useful Commands

```bash
# Start backend
python run.py

# Reset database
rm pluto.db
alembic upgrade head

# Run tests
pytest -v

# Run tests with coverage
pytest --cov=src tests/

# Check app imports
python -c "from src.main import app; print('✅ App imports successfully')"

# View API documentation
# Open: http://localhost:8000/docs

# Connect to database
sqlite3 pluto.db
# Then: SELECT * FROM user; (etc.)
```

## Files You'll Edit Most Often

1. **`frontend/js/app.js`** - Add event handlers, app logic
2. **`frontend/styles/main.css`** - Adjust styling, add animations
3. **`frontend/index.html`** - Add UI elements, modify layout
4. **`frontend/js/api.js`** - Add API endpoints, modify requests

## Deployment Checklist

- [ ] Change SECRET_KEY in backend
- [ ] Set DEBUG=False in backend
- [ ] Update API_BASE_URL in frontend
- [ ] Enable HTTPS
- [ ] Configure CORS for production domain
- [ ] Set up database backups
- [ ] Test all features in production
- [ ] Monitor error logs
- [ ] Set up alerting system

## Support Resources

- **Frontend README**: `frontend/README.md`
- **Setup Guide**: `FRONTEND_SETUP.md`
- **Integration Guide**: `FRONTEND_INTEGRATION.md`
- **Backend Docs**: `http://localhost:8000/docs` (Swagger UI)
- **Testing Guide**: `TESTING_GUIDE.md`
- **Production Guide**: `PRODUCTION_IMPLEMENTATION.md`

---

**Quick Start**: `python run.py` → Open `frontend/index.html` → Register → Test features! 🚀
