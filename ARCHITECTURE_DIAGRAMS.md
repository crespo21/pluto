# Products & Categories - Architecture Diagrams

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                       WEB BROWSER                            │
│  ┌──────────────────────────────────────────────────────┐   │
│  │           Frontend (HTML/CSS/JavaScript)             │   │
│  │  ┌────────────────────────────────────────────────┐  │   │
│  │  │  Pages: Shop, Products, Categories, Profile   │  │   │
│  │  │  Components: Cards, Tables, Forms, Filters    │  │   │
│  │  └────────────────────────────────────────────────┘  │   │
│  └──────────────────────────────────────────────────────┘   │
│                          ↕ HTTP/JSON
└─────────────────────────────────────────────────────────────┘
                            ↓
            ┌───────────────────────────────┐
            │    FASTAPI Backend Server     │
            │    (http://localhost:8000)    │
            └───────────────────────────────┘
                            ↓
        ┌───────────────────────────────────────┐
        │         API Route Handlers             │
        │  ┌─────────────────────────────────┐  │
        │  │  /api/products                  │  │
        │  │  /api/categories                │  │
        │  │  /api/users                     │  │
        │  │  /api/authentications           │  │
        │  │  /api/carts                     │  │
        │  │  /api/checkouts                 │  │
        │  └─────────────────────────────────┘  │
        └───────────────────────────────────────┘
                            ↓
        ┌───────────────────────────────────────┐
        │      Services Layer (Business Logic)  │
        │  ┌─────────────────────────────────┐  │
        │  │  ProductService                 │  │
        │  │  CategoryService                │  │
        │  │  UserService                    │  │
        │  │  AuthenticationService          │  │
        │  │  CartService                    │  │
        │  └─────────────────────────────────┘  │
        └───────────────────────────────────────┘
                            ↓
        ┌───────────────────────────────────────┐
        │    Repository Layer (Data Access)    │
        │  ┌─────────────────────────────────┐  │
        │  │  ProductRepository              │  │
        │  │  CategoryRepository             │  │
        │  │  UserRepository                 │  │
        │  │  AuthenticationRepository       │  │
        │  └─────────────────────────────────┘  │
        └───────────────────────────────────────┘
                            ↓
        ┌───────────────────────────────────────┐
        │        SQLAlchemy ORM Layer           │
        └───────────────────────────────────────┘
                            ↓
        ┌───────────────────────────────────────┐
        │      SQLite/PostgreSQL Database       │
        │  ┌─────────────────────────────────┐  │
        │  │  products                       │  │
        │  │  categories                     │  │
        │  │  users                          │  │
        │  │  authentications                │  │
        │  │  user_profiles                  │  │
        │  │  carts                          │  │
        │  └─────────────────────────────────┘  │
        └───────────────────────────────────────┘
```

---

## Frontend Component Structure

```
Frontend Application
│
├── index.html
│   ├── Navigation Bar
│   ├── Main Content Area
│   │   ├── Home Page
│   │   │   ├── Hero Section
│   │   │   └── Features Grid
│   │   │
│   │   ├── Shop Page (NEW)
│   │   │   ├── Filter Section
│   │   │   │   ├── Category Dropdown
│   │   │   │   └── Status Filter
│   │   │   └── Product Grid
│   │   │       └── Product Cards
│   │   │
│   │   ├── Products Admin Page (NEW)
│   │   │   ├── Form Section
│   │   │   │   ├── Name Input
│   │   │   │   ├── SKU Input
│   │   │   │   ├── Price Input
│   │   │   │   └── Status Select
│   │   │   └── Products Table
│   │   │       ├── ID Column
│   │   │       ├── Name Column
│   │   │       ├── SKU Column
│   │   │       ├── Price Column
│   │   │       ├── Status Column
│   │   │       └── Actions (Edit, Delete)
│   │   │
│   │   ├── Categories Admin Page (NEW)
│   │   │   ├── Form Section
│   │   │   │   ├── Name Input
│   │   │   │   ├── Description Input
│   │   │   │   └── Status Select
│   │   │   └── Categories Table
│   │   │       ├── ID Column
│   │   │       ├── Name Column
│   │   │       ├── Description Column
│   │   │       ├── Status Column
│   │   │       └── Actions (Edit, Delete)
│   │   │
│   │   ├── Profile Page
│   │   │   ├── Profile Creation Modal (NEW)
│   │   │   ├── User Info Display
│   │   │   └── Logout Button
│   │   │
│   │   └── Cart & Checkout Pages
│   │
│   └── Footer
│
└── JavaScript Files
    │
    ├── api.js (API Communication)
    │   ├── APIClient Class
    │   │   ├── Authentication Methods
    │   │   ├── Product Methods (NEW/UPDATED)
    │   │   │   ├── getProducts()
    │   │   │   ├── createProduct()
    │   │   │   ├── updateProduct()
    │   │   │   └── deleteProduct()
    │   │   ├── Category Methods (NEW/UPDATED)
    │   │   │   ├── getCategories()
    │   │   │   ├── createCategory()
    │   │   │   ├── updateCategory()
    │   │   │   └── deleteCategory()
    │   │   └── Other Methods
    │   │
    │   └── Global Instance: const api = new APIClient()
    │
    ├── app.js (Application State)
    │   ├── appState Object
    │   │   ├── isLoggedIn
    │   │   ├── currentUser
    │   │   ├── products (CACHE)
    │   │   ├── categories (CACHE)
    │   │   └── cart
    │   │
    │   └── Event Listeners
    │
    ├── pages.js (Page Rendering)
    │   ├── Shop Page Functions (NEW)
    │   │   ├── renderShop()
    │   │   ├── loadShopProducts()
    │   │   ├── renderShopProducts()
    │   │   ├── filterProducts()
    │   │   ├── populateCategoryFilter()
    │   │   └── resetFilters()
    │   │
    │   ├── Products Admin Functions (UPDATED)
    │   │   ├── renderProducts()
    │   │   ├── loadAdminProducts()
    │   │   ├── renderProductsTable()
    │   │   ├── handleProductSubmit()
    │   │   ├── deleteProduct()
    │   │   └── editProduct()
    │   │
    │   ├── Categories Admin Functions (UPDATED)
    │   │   ├── renderCategories()
    │   │   ├── loadCategories()
    │   │   ├── renderCategoriesTable()
    │   │   ├── handleCategorySubmit()
    │   │   ├── deleteCategory()
    │   │   └── editCategory()
    │   │
    │   ├── Profile Functions (UPDATED)
    │   │   ├── showProfileCreationModal()
    │   │   └── handleProfileCreation()
    │   │
    │   └── Other Page Renderers
    │
    ├── utils.js (Utilities)
    │   ├── showNotification()
    │   ├── Storage Helpers
    │   ├── formatCurrency()
    │   ├── formatDate()
    │   ├── debounce()
    │   ├── throttle()
    │   └── deepClone()
    │
    └── styles/main.css (Styling)
        ├── Global Styles
        ├── Component Styles
        ├── Modal Styles
        ├── Form Styles
        ├── Table Styles
        ├── Product Card Styles
        └── Responsive Styles
```

---

## Backend Route Structure

```
API Routes (/api)
│
├── /users
│   ├── POST   /         (Create user)
│   ├── GET    /         (Get all users)
│   ├── GET    /{id}     (Get user by ID)
│   ├── PATCH  /{id}     (Update user)
│   ├── DELETE /{id}     (Delete user)
│   ├── GET    /current  (Get current user) [NEW]
│   ├── POST   /profile  (Create/update profile) [NEW]
│   ├── GET    /profile  (Get user profile) [NEW]
│   └── GET    /profile/check (Check if has profile) [NEW]
│
├── /products (NEW ENDPOINTS)
│   ├── POST   /         (Create product)
│   ├── GET    /         (Get all products)
│   ├── GET    /{id}     (Get product by ID)
│   ├── PATCH  /{id}     (Update product)
│   ├── PATCH  /{id}/status (Update status)
│   └── DELETE /{id}     (Delete product) [NEW]
│
├── /categories (NEW ENDPOINTS)
│   ├── POST   /         (Create category)
│   ├── GET    /         (Get all categories) [NEW]
│   ├── GET    /{id}     (Get category by ID) [NEW]
│   ├── PATCH  /{id}     (Update category) [NEW]
│   ├── PATCH  /{id}/status (Update status) [NEW]
│   └── DELETE /{id}     (Delete category) [NEW]
│
├── /authentications
│   ├── POST   /         (Create auth)
│   └── POST   /login    (Login user)
│
├── /logouts
│   └── POST   /         (Logout user)
│
├── /carts
│   ├── POST   /         (Create cart)
│   ├── GET    /{id}     (Get cart)
│   ├── PATCH  /{id}     (Update cart)
│   └── DELETE /{id}     (Delete cart)
│
└── /checkouts
    ├── POST   /         (Create checkout)
    ├── GET    /{id}     (Get checkout)
    └── PATCH  /{id}     (Update checkout)
```

---

## Data Model Relationships

```
┌──────────────────┐
│     users        │
├──────────────────┤
│ id (PK)          │
│ username         │
│ email            │
│ password         │
│ status           │
└──────────────────┘
        │
        │ 1:1
        │
┌──────────────────────┐
│  user_profiles       │
├──────────────────────┤
│ id (PK)              │
│ user_id (FK) [UNIQUE]│
│ first_name           │
│ last_name            │
│ phone                │
│ address              │
└──────────────────────┘


┌──────────────────┐         ┌──────────────────┐
│   categories     │─────────│    products      │
├──────────────────┤  1:N    ├──────────────────┤
│ id (PK)          │         │ id (PK)          │
│ name             │         │ name             │
│ description      │         │ sku              │
│ status           │         │ price            │
└──────────────────┘         │ status           │
                             │ category_id (FK) │
                             └──────────────────┘


┌──────────────────┐         ┌──────────────────┐
│     users        │─────────│     carts        │
├──────────────────┤  1:N    ├──────────────────┤
│ id (PK)          │         │ id (PK)          │
│ ...              │         │ user_id (FK)     │
└──────────────────┘         │ status           │
                             └──────────────────┘
                                     │
                                     │ 1:N
                                     │
                             ┌──────────────────┐
                             │   cart_items     │
                             ├──────────────────┤
                             │ id (PK)          │
                             │ cart_id (FK)     │
                             │ product_id (FK)  │
                             │ quantity         │
                             └──────────────────┘


┌──────────────────┐
│  authentications │
├──────────────────┤
│ id (PK)          │
│ user_id (FK)     │
│ token            │
│ status           │
│ created_at       │
└──────────────────┘
```

---

## Request/Response Flow Example: Shop Page Load

```
USER INTERACTION
      │
      └─→ User navigates to Shop page
           │
           ├─→ renderShop() is called
           │
           └─→ HTML elements rendered
                │
                └─→ loadShopProducts() called
                     │
                     ├─→ Promise.all([
                     │     api.getProducts(),
                     │     api.getCategories()
                     │   ])
                     │
                     ├─→ GET /api/products  ─┐
                     │                        │
                     │   ┌──────────────────────┤
                     │   │  Backend Processing:
                     │   │  1. Parse request
                     │   │  2. Query database
                     │   │  3. Convert to DTO
                     │   │  4. Serialize to JSON
                     │   │  5. Return response
                     │   └──────────────────────┤
                     │                        │
                     │← JSON Response ────────┤
                     │   [                    │
                     │     {id:1, name:..},  │
                     │     {id:2, name:..}   │
                     │   ]                    │
                     │
                     ├─→ GET /api/categories ─┐
                     │                        │
                     │   ┌──────────────────────┤
                     │   │  Backend Processing:
                     │   │  (same as above)
                     │   └──────────────────────┤
                     │                        │
                     │← JSON Response ────────┤
                     │   [                    │
                     │     {id:1, name:...}, │
                     │     {id:2, name:...}  │
                     │   ]                    │
                     │
                     ├─→ Store in globals:
                     │   window.allProducts = products
                     │   window.allCategories = categories
                     │
                     ├─→ populateCategoryFilter(categories)
                     │   └─→ Update dropdown options
                     │
                     └─→ renderShopProducts(products)
                         └─→ Display product grid
                             Each card shows:
                             - Product image
                             - Name
                             - SKU
                             - Price
                             - Status
                             - "Add to Cart" button
                                 (disabled if not AVAILABLE)
```

---

## User Interaction Flow: Create Product

```
STEP 1: Navigate to Products Page
    │
    └─→ router.navigate('products')
        └─→ renderProducts()
            └─→ loadAdminProducts()
                └─→ GET /api/products
                    └─→ renderProductsTable()

STEP 2: Click "Add Product"
    │
    └─→ showProductForm()
        └─→ Remove 'hidden' class from form

STEP 3: Fill Form
    │
    ├─→ Name: "Wireless Mouse"
    ├─→ SKU: "TECH-MOUSE-001"
    ├─→ Price: 45.99
    └─→ Status: "AVAILABLE"

STEP 4: Submit Form
    │
    └─→ handleProductSubmit(event)
        │
        ├─→ event.preventDefault()
        │
        ├─→ Extract form values
        │
        ├─→ api.createProduct(name, sku, price, status)
        │   │
        │   └─→ POST /api/products
        │       {
        │         "name": "Wireless Mouse",
        │         "sku": "TECH-MOUSE-001",
        │         "price": 45.99,
        │         "status": "AVAILABLE"
        │       }
        │       │
        │       └─→ Backend:
        │           1. Validate input
        │           2. Check SKU unique
        │           3. Create Product entity
        │           4. Save to database
        │           5. Return ProductResponse
        │
        ├─→ Success: showNotification("Product created...")
        │
        ├─→ hideProductForm()
        │
        ├─→ Clear all form fields
        │
        └─→ loadAdminProducts()
            └─→ Refresh table with new product
```

---

## State Management

```
Frontend State Management
│
├── localStorage
│   ├── authToken (JWT token)
│   ├── userId (Current user ID)
│   └── cartItems (Serialized cart)
│
├── appState (Global object)
│   ├── isLoggedIn (Boolean)
│   ├── currentUser (User object)
│   ├── products (Array) [DEPRECATED for fetch]
│   ├── categories (Array) [DEPRECATED for fetch]
│   └── cart (Array of cart items)
│
└── Window Globals (For Shop page)
    ├── window.allProducts (Array) [NEW]
    │   └─ Cached for fast filtering
    └── window.allCategories (Array) [NEW]
        └─ Cached for dropdown
```

---

## Caching Strategy

```
Page Load
    │
    ├─→ Shop Page
    │   └─→ Load and cache both:
    │       ├─ window.allProducts (from API)
    │       └─ window.allCategories (from API)
    │
    └─→ Other Pages
        └─→ API calls fresh data

Filtering (Shop Page)
    │
    ├─→ User selects category or status
    │
    └─→ filterProducts()
        │
        ├─→ Read from window.allProducts (cached)
        │
        ├─→ Apply filters locally (no API call)
        │
        └─→ Re-render results (instant)

Reset Filters
    │
    └─→ resetFilters()
        │
        ├─→ Clear dropdown values
        │
        └─→ Read from window.allProducts
            └─→ Display all products (instant)
```

---

## Error Handling Flow

```
API Request
    │
    ├─→ Network Error
    │   └─→ catch → showNotification("Failed to...")
    │
    ├─→ HTTP Error (4xx, 5xx)
    │   │
    │   └─→ handleResponse() checks response.ok
    │       │
    │       └─→ false → throw Error → catch
    │           └─→ showNotification with error details
    │
    └─→ Success (200-299)
        │
        └─→ Parse JSON and return data

Form Submission
    │
    ├─→ Validation error
    │   └─→ Form shows error, doesn't submit
    │
    └─→ API Error
        │
        ├─→ Duplicate SKU
        │   └─→ showNotification("SKU already exists")
        │
        └─→ Server Error
            └─→ showNotification("Failed to create...")
```

---

## Browser Network Timeline Example

```
Shop Page Load

Time    Event                              Duration
────────────────────────────────────────────────────
0ms     Page load starts
        └─ renderShop() called
           └─ loadShopProducts() called
              └─ Promise.all() starts
                 
~50ms   ├─→ GET /api/products request sent
        └─→ GET /api/categories request sent
           (Both in parallel)

~200ms  ├─ GET /api/products response (150ms)
        │  ├─ Database query: 100ms
        │  ├─ Serialization: 30ms
        │  └─ Network: 20ms
        │
        └─ GET /api/categories response (180ms)
           ├─ Database query: 120ms
           ├─ Serialization: 40ms
           └─ Network: 20ms

~210ms  Both responses received
        └─ window.allProducts = products
           window.allCategories = categories
           populateCategoryFilter()
           renderShopProducts()

~220ms  ✓ Shop page fully rendered
```

This visualization shows how parallel requests significantly reduce page load time compared to sequential requests.
