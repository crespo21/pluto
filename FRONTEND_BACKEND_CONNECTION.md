# 🚀 Frontend-Backend Connection Guide

## ✅ Connection is Already Working!

Your frontend and backend are already connected through the API. Here's how to verify and use it:

---

## 🧪 Test the Connection

### Option 1: Use the API Test Page (Recommended)

1. Start your backend server:

   ```bash
   python -m uvicorn src.main:app --reload
   ```

2. Open the test page in your browser:

   ```
   http://127.0.0.1:8000/frontend/api-test.html
   ```

3. Click the test buttons to verify:
   - ✅ Server Health
   - ✅ Products Endpoint
   - ✅ Categories Endpoint
   - ✅ User Creation
   - ✅ Authentication
   - ✅ CORS Configuration

### Option 2: Use Browser Console

1. Open your browser's DevTools (F12)
2. Go to Console tab
3. Run these commands:

```javascript
// Test 1: Fetch products
fetch('http://127.0.0.1:8000/api/products')
  .then(r => r.json())
  .then(d => console.log('Products:', d))
  .catch(e => console.error('Error:', e))

// Test 2: Fetch categories
fetch('http://127.0.0.1:8000/api/categories')
  .then(r => r.json())
  .then(d => console.log('Categories:', d))
  .catch(e => console.error('Error:', e))

// Test 3: Create a user
fetch('http://127.0.0.1:8000/api/users', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    username: 'testuser',
    email: 'test@example.com',
    password: 'Password123!',
    status: 'ACTIVE'
  })
})
  .then(r => r.json())
  .then(d => console.log('User created:', d))
  .catch(e => console.error('Error:', e))
```

---

## 🔌 How the Connection Works

```
┌─────────────────────────────┐
│     Browser (Frontend)      │
│  - HTML/CSS/JavaScript      │
│  - Located at /frontend/    │
└──────────┬──────────────────┘
           │
           │ HTTP Requests
           │ (GET, POST, PUT, DELETE)
           │
           ▼
┌─────────────────────────────┐
│    Backend (FastAPI)        │
│  - Serves frontend files    │
│  - Provides REST API        │
│  - Handles business logic   │
│  - Manages database         │
└─────────────────────────────┘
```

---

## 📡 API Endpoints Available

### Products
- **GET** `/api/products` - Get all products
- **GET** `/api/products/{id}` - Get specific product
- **POST** `/api/products` - Create product
- **PUT** `/api/products/{id}` - Update product
- **DELETE** `/api/products/{id}` - Delete product

### Categories
- **GET** `/api/categories` - Get all categories
- **GET** `/api/categories/{id}` - Get specific category
- **POST** `/api/categories` - Create category
- **PUT** `/api/categories/{id}` - Update category
- **DELETE** `/api/categories/{id}` - Delete category

### Users
- **GET** `/api/users` - Get all users
- **POST** `/api/users` - Create user (sign up)
- **GET** `/api/users/{id}` - Get user by ID
- **PUT** `/api/users/{id}` - Update user
- **DELETE** `/api/users/{id}` - Delete user

### Authentication
- **POST** `/api/authentications/login` - User login
- **POST** `/api/logouts` - User logout

### Cart
- **GET** `/api/carts` - Get user's cart
- **POST** `/api/carts` - Create cart
- **POST** `/api/carts/items` - Add item to cart
- **DELETE** `/api/carts/items/{id}` - Remove item

### Checkout
- **POST** `/api/checkouts` - Create checkout

---

## 🔐 Frontend API Client Setup

The frontend already has an API client configured. Location: `frontend/js/api.js`

**Configuration:**
```javascript
const API_BASE_URL = 'http://127.0.0.1:8000/api';
```

**Usage in frontend code:**
```javascript
// The api object is globally available
const client = new APIClient();

// Get products
const products = await client.getProducts();

// Create user
await client.signup(name, email, password);

// Login
await client.signin(email, password);

// Get categories
const categories = await client.getCategories();
```

---

## 🚀 Quick Start

### Terminal 1: Start Backend
```bash
cd c:\Users\sabas\Documents\pluto
.venv\Scripts\Activate.ps1
python -m uvicorn src.main:app --reload
```

**Output should show:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

### Terminal 2: Access Frontend
1. Open browser to: `http://127.0.0.1:8000/frontend/index.html`
2. Or test API connection: `http://127.0.0.1:8000/frontend/api-test.html`

---

## ✅ Verification Checklist

- ✅ Backend running on `http://127.0.0.1:8000`
- ✅ Frontend accessible at `http://127.0.0.1:8000/frontend/index.html`
- ✅ API responding at `http://127.0.0.1:8000/api`
- ✅ CORS configured for localhost connections
- ✅ Database persisting data (SQLite)
- ✅ Authentication endpoints working
- ✅ Frontend can fetch products
- ✅ Frontend can fetch categories

---

## 🐛 Troubleshooting

### Issue: "Failed to fetch" errors
**Solution:** Check if backend is running and CORS is enabled

### Issue: 400 Bad Request on OPTIONS
**Solution:** Already fixed! CORS middleware now properly handles OPTIONS requests

### Issue: Can't create user
**Solution:** Ensure valid email format and password meets requirements

### Issue: Login fails
**Solution:** Verify user exists and password is correct

### Issue: Frontend won't load
**Solution:** Make sure backend is running and visit `http://127.0.0.1:8000/frontend/index.html`

---

## 📊 Testing the Full Flow

1. **Open test page**: `http://127.0.0.1:8000/frontend/api-test.html`
2. **Click "Test Server"** - Verify backend is running
3. **Click "Get Products"** - Verify products endpoint works
4. **Click "Get Categories"** - Verify categories endpoint works
5. **Click "Create User"** - Create test user
6. **Click "Test Login"** - Verify authentication works
7. **Click "Test CORS"** - Verify CORS is configured

---

## 🎯 Next Steps

1. ✅ Verify connection using the test page
2. ✅ Test creating users and logging in
3. ✅ Add products and categories through the frontend
4. ✅ Add items to cart
5. ✅ Complete checkout flow

**Your frontend and backend are fully connected and ready to use!** 🚀
