# Frontend-Backend Integration Guide

## Overview

This guide explains how the frontend and backend components work together in the Pluto e-commerce platform.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Web Browser                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │         Frontend (HTML + CSS + JavaScript)           │   │
│  │  ┌────────────────┐  ┌─────────────┐  ┌──────────┐  │   │
│  │  │   index.html   │  │  main.css   │  │  app.js  │  │   │
│  │  │  (UI Elements) │  │  (Styling)  │  │ (Logic)  │  │   │
│  │  └────────────────┘  └─────────────┘  └──────────┘  │   │
│  │  ┌──────────────────────────────────────────────┐   │   │
│  │  │      api.js (API Client)                    │   │   │
│  │  │  - Handles HTTP requests                    │   │   │
│  │  │  - Manages JWT authentication               │   │   │
│  │  │  - Calls backend endpoints                  │   │   │
│  │  └──────────────────────────────────────────────┘   │   │
│  └──────────────────────────────────────────────────────┘   │
│                            ↓ HTTP/JSON                       │
└─────────────────────────────────────────────────────────────┘

                    Network (CORS Enabled)

┌─────────────────────────────────────────────────────────────┐
│           FastAPI Backend (http://localhost:8000)            │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Presentation Layer (API Endpoints)                  │   │
│  │  - /api/auth/* (Authentication)                      │   │
│  │  - /api/products/* (Product Management)              │   │
│  │  - /api/categories/* (Category Management)           │   │
│  │  - /api/cart/* (Shopping Cart)                       │   │
│  │  - /api/checkout/* (Order Processing)                │   │
│  │  - /api/users/* (User Management)                    │   │
│  └──────────────────────────────────────────────────────┘   │
│                            ↓                                  │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Application Services Layer                          │   │
│  │  - Business Logic                                    │   │
│  │  - Data Validation                                   │   │
│  │  - Authentication & Authorization                   │   │
│  └──────────────────────────────────────────────────────┘   │
│                            ↓                                  │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Domain Layer                                        │   │
│  │  - Entities & Value Objects                          │   │
│  │  - Business Rules                                    │   │
│  │  - Exceptions & Enums                                │   │
│  └──────────────────────────────────────────────────────┘   │
│                            ↓                                  │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Infrastructure Layer                                │   │
│  │  - SQLAlchemy Repositories                           │   │
│  │  - Database Connections                              │   │
│  │  - Password Hashing (bcrypt)                         │   │
│  └──────────────────────────────────────────────────────┘   │
│                            ↓                                  │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  SQLite Database (pluto.db)                          │   │
│  │  - Users, Products, Categories                       │   │
│  │  - Cart Items, Orders, Checkouts                     │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Data Flow Examples

### User Registration Flow

```
Frontend (browser)                          Backend (FastAPI)
      ↓                                           ↓
1. User fills registration form
   ↓
2. Validate input (JavaScript)
   ├─ Username: alphanumeric + underscore
   ├─ Email: valid email format
   └─ Password: 12+ chars, complex
   ↓
3. Call api.register()
   ↓
4. POST /api/auth/register
   ├─ Method: POST
   ├─ Body: {username, email, password}
   └─ Headers: Content-Type: application/json
      ↓
      5. Validate request (backend)
      ├─ Check username format
      ├─ Check email validity
      ├─ Check password strength
      └─ Check user doesn't exist
      ↓
      6. Hash password with bcrypt
      ↓
      7. Create user in database
      ↓
      8. Return response: {id, username, email}
   ↓
9. Show success message
   ↓
10. Clear form, show login option
```

### Product Browsing Flow

```
Frontend                                    Backend
      ↓                                           ↓
1. Load Products page
   ↓
2. Call api.listProducts()
   ↓
3. GET /api/products
   ↓
   (Optional: GET /api/categories)
   ↓
      4. Query database for products
      ↓
      5. Filter by active status
      ↓
      6. Return paginated results
   ↓
7. Render product grid
   ├─ Display product image
   ├─ Show name, price, category
   └─ Add "Add to Cart" buttons
```

### Shopping Cart Flow

```
Frontend                                    Backend
      ↓                                           ↓
1. User clicks "Add to Cart"
   ↓
2. appState.cartItems.push(product)
   ↓
3. updateCartUI() - Update display
   ↓
4. Show "Added to cart" alert
   ↓
5. Update cart badge with count
```

### Checkout Flow

```
Frontend                                    Backend
      ↓                                           ↓
1. User clicks "Proceed to Checkout"
   ↓
2. Validate shipping address
   ↓
3. Select payment method
   ↓
4. Call api.createCheckout()
   ↓
5. POST /api/checkout
   ├─ cartId: string
   ├─ shippingAddress: {street, city, zip, country}
   └─ paymentMethod: "credit_card"|"paypal"|"bank_transfer"
      ↓
      6. Validate checkout data
      ↓
      7. Verify cart items still available
      ↓
      8. Calculate totals (subtotal + tax)
      ↓
      9. Create checkout record
      ↓
      10. Return: {checkoutId, status, total, cartItems}
   ↓
11. Show order confirmation
   ↓
12. Clear cart (optional: create new cart)
   ↓
13. Show order summary
```

## API Endpoints Reference

### Authentication Endpoints

```javascript
// Register new user
POST /api/auth/register
Body: {
  username: "john_doe",
  email: "john@example.com",
  password: "SecurePass123!"
}
Response: { id, username, email }

// Login user
POST /api/auth/login
Body: {
  username: "john_doe",
  password: "SecurePass123!"
}
Response: { access_token, token_type: "bearer", user: {...} }

// Logout user
POST /api/auth/logout
Headers: { Authorization: "Bearer <token>" }
Response: { message: "Logged out successfully" }
```

### Product Endpoints

```javascript
// List all products
GET /api/products?skip=0&limit=10
Response: [{ id, name, price, category, description, ... }]

// Get specific product
GET /api/products/{product_id}
Response: { id, name, price, category, description, ... }

// Search products
GET /api/products/search?query=laptop&category=electronics
Response: [{ id, name, price, ... }]

// Create product (admin only)
POST /api/products
Headers: { Authorization: "Bearer <admin_token>" }
Body: { name, price, category, description }
Response: { id, name, ... }
```

### Cart Endpoints

```javascript
// Create cart
POST /api/cart
Response: { id, user_id, items: [], created_at }

// Get cart
GET /api/cart/{cart_id}
Response: { id, user_id, items: [...], subtotal, tax, total }

// Add item to cart
POST /api/cart/{cart_id}/items
Body: { product_id, quantity }
Response: { cartItem: {...} }

// Update cart item
PUT /api/cart/{cart_id}/items/{item_id}
Body: { quantity }
Response: { cartItem: {...} }

// Remove item from cart
DELETE /api/cart/{cart_id}/items/{item_id}
Response: { message: "Item removed" }

// Clear cart
DELETE /api/cart/{cart_id}
Response: { message: "Cart cleared" }
```

### Checkout Endpoints

```javascript
// Create checkout
POST /api/checkout
Headers: { Authorization: "Bearer <token>" }
Body: {
  cart_id: "abc123",
  shipping_address: {
    street: "123 Main St",
    city: "Springfield",
    zip: "12345",
    country: "USA"
  },
  payment_method: "credit_card"
}
Response: {
  id,
  status: "pending",
  cart_id,
  shipping_address,
  payment_method,
  subtotal,
  tax,
  total,
  created_at
}

// Get checkout
GET /api/checkout/{checkout_id}
Headers: { Authorization: "Bearer <token>" }
Response: { checkout details }

// Process payment
POST /api/checkout/{checkout_id}/payment
Headers: { Authorization: "Bearer <token>" }
Body: { payment_details: {...} }
Response: { status: "completed", order_id }
```

## Authentication (JWT)

### How It Works

```
1. User logs in via frontend
   ↓
2. POST /api/auth/login with credentials
   ↓
3. Backend validates credentials and hashes password with bcrypt
   ↓
4. If valid, backend generates JWT token
   ↓
5. Token is returned to frontend
   ↓
6. Frontend stores token in localStorage as 'auth_token'
   ↓
7. For protected endpoints, frontend sends:
   Authorization: Bearer <token>
   ↓
8. Backend validates JWT signature and claims
   ↓
9. If valid, user is authenticated
   ↓
10. If expired/invalid, return 401 Unauthorized
```

### Token Structure

```javascript
// JWT Token Format
Header: {
  "alg": "HS256",
  "typ": "JWT"
}

Payload: {
  "sub": "user_id",
  "iat": 1234567890,
  "exp": 1234571490
}

Signature: HMACSHA256(
  base64UrlEncode(header) + "." +
  base64UrlEncode(payload),
  SECRET_KEY
)
```

### Frontend Token Management

```javascript
// In api.js
class PletoAPIClient {
    constructor() {
        this.token = localStorage.getItem('auth_token');
    }
    
    async request(endpoint, options = {}) {
        const headers = {
            'Content-Type': 'application/json',
            ...options.headers,
        };
        
        // Automatically add token to headers
        if (this.token) {
            headers['Authorization'] = `Bearer ${this.token}`;
        }
        
        // Make request...
    }
}
```

## CORS Configuration

### Problem
- Frontend runs on `file://` or `localhost:3000`
- Backend runs on `localhost:8000`
- Browsers block cross-origin requests by default

### Solution
Add CORS middleware to backend:

```python
# In src/main.py
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Development: allow all
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# For production, be more restrictive:
# allow_origins=["https://yourdomain.com"],
# allow_credentials=True,
# allow_methods=["GET", "POST", "PUT", "DELETE"],
# allow_headers=["*"],
```

## Error Handling

### Frontend Error Handling

```javascript
// In app.js
async function handleLogin() {
    try {
        await api.login(username, password);
        // Success
        showAlert('Login successful!', 'success');
        // Redirect or update UI
    } catch (error) {
        // Error handling
        if (error.status === 401) {
            showAlert('Invalid username or password', 'error');
        } else if (error.status === 400) {
            showAlert(error.details[0].msg, 'error');
        } else {
            showAlert('An unexpected error occurred', 'error');
        }
    }
}
```

### Backend Error Handling

```python
# In src/core/exceptions.py
class ApplicationException(Exception):
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

# Usage in endpoints
@router.post("/login")
async def login(request: LoginRequest):
    try:
        user = authenticate_user(request.username, request.password)
        if not user:
            raise ApplicationException("Invalid credentials", 401)
        return {"token": generate_token(user)}
    except ApplicationException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
```

## Database Transactions

### Cart Operations
```
1. User adds product to cart
2. Frontend stores in appState (in-memory)
3. (Optional) POST /api/cart/{id}/items to backend
4. Backend updates database
5. Frontend shows confirmation
```

### Checkout Operations
```
1. User submits checkout form
2. Frontend validates data
3. POST /api/checkout to backend
4. Backend creates checkout record
5. Backend updates order status
6. Backend clears cart
7. Frontend shows confirmation
8. (Optional) Backend sends confirmation email
```

## State Management

### Frontend State (appState object)

```javascript
const appState = {
    // User management
    currentUser: null,          // { id, username, email }
    
    // Shopping
    products: [],               // [{ id, name, price, ... }]
    categories: [],             // [{ id, name, ... }]
    cartItems: [],              // [{ id, name, price, quantity }]
    cartId: null,               // Cart ID from backend
    
    // Navigation
    currentSection: 'home',     // Which page is visible
};
```

### Backend State (Database)

```
Users
├─ id (UUID)
├─ username (unique)
├─ email (unique)
├─ password (hashed)
├─ created_at
└─ updated_at

Products
├─ id
├─ name
├─ price
├─ description
├─ category_id
├─ status (AVAILABLE, OUT_OF_STOCK, etc.)
└─ created_at

Cart
├─ id
├─ user_id (nullable - supports guest carts)
├─ items (CartItem relationships)
└─ created_at

CartItem
├─ id
├─ cart_id
├─ product_id
├─ quantity
└─ added_at

Checkout
├─ id
├─ cart_id
├─ user_id
├─ shipping_address
├─ payment_method
├─ status (PENDING, COMPLETED, FAILED, etc.)
├─ total
└─ created_at
```

## Performance Considerations

### Frontend Optimization
- Vanilla JS (no frameworks) = fast load
- Minimal HTTP requests (batch operations)
- Local storage for tokens (no re-login)
- Event delegation for dynamic elements
- CSS grid for responsive layouts

### Backend Optimization
- SQLAlchemy ORM with lazy loading
- Database indexing on common queries
- Pagination for large result sets
- JWT for stateless authentication
- Bcrypt for password hashing (slow by design)

## Security Features

### Password Security
- Minimum 12 characters
- Requires uppercase, lowercase, digit, special char
- Hashed with bcrypt (10 rounds)
- Never transmitted in plain text

### Authentication
- JWT tokens with expiration
- Tokens stored in localStorage (browser memory)
- Authorization header for protected endpoints
- Logout clears tokens

### Data Validation
- Frontend validation (UX)
- Backend validation (security)
- Email format validation
- Username format validation
- Cart/checkout data validation

### CORS
- Restricts cross-origin requests
- Whitelist allowed origins
- Support credentials with authentication

## Testing the Integration

### 1. Start Backend
```bash
cd c:\Users\sabas\Documents\pluto
python run.py
```

### 2. Open Frontend
```
Open frontend/index.html in your browser
```

### 3. Test User Registration
```
- Click "Register"
- Fill in form (valid password required!)
- Submit
- Check success message
```

### 4. Test Login
```
- Click "Login"
- Enter credentials from step 3
- Submit
- Should see "Welcome, [username]" in navbar
```

### 5. Test Products
```
- Go to Products section
- Should see list of products
- Filter by category
- Search for products
```

### 6. Test Cart
```
- Click "Add to Cart" on any product
- View cart
- Adjust quantity
- See total update
```

### 7. Test Checkout
```
- Click "Proceed to Checkout"
- Fill in shipping address
- Select payment method
- Click "Complete Order"
- See confirmation
```

## Troubleshooting

### Issue: Products not loading
**Check:**
1. Backend running on localhost:8000
2. Browser console (F12) for errors
3. Network tab shows API call
4. API returns products (check /docs)

**Solution:**
1. Restart backend: `python run.py`
2. Check database has products
3. Run script: `python -c "from src.application.services.product_services import ProductService; print(ProductService.list_products())"`

### Issue: Login fails
**Check:**
1. Backend running
2. User exists in database
3. Password meets requirements

**Solution:**
1. Verify password: min 12 chars, 1 upper, 1 lower, 1 digit, 1 special
2. Check database for user: `sqlite3 pluto.db "SELECT * FROM user;"`
3. Restart backend

### Issue: Cart not updating
**Check:**
1. JavaScript enabled
2. Browser console for errors
3. Check localStorage: F12 → Application → Local Storage

**Solution:**
1. Check appState.cartItems is being updated
2. Add console.log() in addToCart function
3. Refresh page and try again

## Next Steps

1. **Customize Branding**
   - Change logo text in navbar
   - Update colors in CSS variables
   - Modify footer content

2. **Add Features**
   - Product reviews
   - Wishlist
   - Order history
   - User profile page

3. **Enhance UX**
   - Add product images (currently emoji)
   - Add loading spinners
   - Add progress indicators
   - Add notifications

4. **Production Deployment**
   - Change SECRET_KEY
   - Set DEBUG=False
   - Enable HTTPS
   - Set up database backups
   - Configure email notifications

---

**Version**: 1.0.0
**Last Updated**: 2024
