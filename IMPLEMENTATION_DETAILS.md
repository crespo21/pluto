# Products & Categories Implementation Details

## Frontend Structure

### JavaScript Files Organization

#### `frontend/js/api.js`
Handles all HTTP communication with backend
- **APIClient class**: Main API communication handler
- **Methods for Products**:
  - `getProducts()` - GET /api/products
  - `getProduct(id)` - GET /api/products/{id}
  - `createProduct(name, sku, price, status)` - POST /api/products
  - `updateProduct(id, data)` - PATCH /api/products/{id}
  - `deleteProduct(id)` - DELETE /api/products/{id}

- **Methods for Categories**:
  - `getCategories()` - GET /api/categories
  - `getCategory(id)` - GET /api/categories/{id}
  - `createCategory(name, description, status)` - POST /api/categories
  - `updateCategory(id, data)` - PATCH /api/categories/{id}
  - `deleteCategory(id)` - DELETE /api/categories/{id}

#### `frontend/js/pages.js`
Handles page rendering and user interactions
- **Shop Page** (`renderShop()`):
  - `loadShopProducts()` - Loads products and categories in parallel
  - `renderShopProducts(products)` - Renders product grid
  - `populateCategoryFilter(categories)` - Populates category dropdown
  - `filterProducts()` - Filters by category and status
  - `resetFilters()` - Resets all filters

- **Products Management** (`renderProducts()`):
  - `loadAdminProducts()` - Loads products for admin view
  - `renderProductsTable(products)` - Displays products in table
  - `showProductForm()` / `hideProductForm()` - Toggle form visibility
  - `handleProductSubmit(e)` - Form submission handler
  - `deleteProduct(id)` - Delete product handler
  - `editProduct(id)` - Edit product handler (coming soon)

- **Categories Management** (`renderCategories()`):
  - `loadCategories()` - Loads categories for admin view
  - `renderCategoriesTable(categories)` - Displays categories in table
  - `showCategoryForm()` / `hideCategoryForm()` - Toggle form visibility
  - `handleCategorySubmit(e)` - Form submission handler
  - `deleteCategory(id)` - Delete category handler
  - `editCategory(id)` - Edit category handler (coming soon)

#### `frontend/js/app.js`
Main application logic and state management
- **appState object**: Global application state
  - `isLoggedIn`: Boolean
  - `currentUser`: User object
  - `products`: Array of products
  - `categories`: Array of categories
  - `cart`: Shopping cart items

#### `frontend/js/utils.js`
Shared utility functions
- `showNotification()` - Display toast notifications
- `formatCurrency()` - Format numbers as currency
- `formatDate()` - Format dates
- Storage helpers (set, get, remove, clear)

---

## Backend Structure

### API Endpoints

#### Product Endpoints
Base: `/api/products`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Get all products |
| POST | `/` | Create product |
| GET | `/{id}` | Get product by ID |
| PATCH | `/{id}` | Update product |
| PATCH | `/{id}/status` | Update product status |
| DELETE | `/{id}` | Delete product |

#### Category Endpoints
Base: `/api/categories`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Get all categories |
| POST | `/` | Create category |
| GET | `/{id}` | Get category by ID |
| PATCH | `/{id}` | Update category |
| PATCH | `/{id}/status` | Update category status |
| DELETE | `/{id}` | Delete category |

### Backend Files

#### `src/presentation/api/endpoints/product/product_endpoints.py`
Product API route handlers
- `create_product()` - POST handler
- `get_all_products()` - GET all handler
- `get_product_by_id()` - GET by ID handler
- `update_product_partial()` - PATCH handler
- `update_product_status()` - Status update handler
- `delete_product()` - DELETE handler

#### `src/presentation/api/endpoints/category/category_endpoints.py`
Category API route handlers
- `create_category()` - POST handler
- `get_all_categories()` - GET all handler
- `get_category_by_id()` - GET by ID handler
- `update_category_partial()` - PATCH handler
- `update_category_status()` - Status update handler
- `delete_category()` - DELETE handler

### Data Models

#### Product Model
- **id**: Integer (Primary Key)
- **name**: String (unique, max 100)
- **sku**: String (unique, max 50)
- **price**: Float
- **status**: String (AVAILABLE, OUT_OF_STOCK, DISCONTINUED)

#### Category Model
- **id**: Integer (Primary Key)
- **name**: String (unique, max 100)
- **description**: String (optional, max 500)
- **status**: String (ACTIVE, INACTIVE)

---

## Data Flow Diagrams

### Create Product Flow
```
User Input Form
        ↓
handleProductSubmit()
        ↓
api.createProduct()
        ↓
HTTP POST /api/products
        ↓
Backend: create_product()
        ↓
Validate & Store in DB
        ↓
Return ProductResponse
        ↓
Frontend: Show Success Notification
        ↓
loadAdminProducts()
        ↓
Refresh Products Table
```

### Shop Page Load Flow
```
User clicks "Shop"
        ↓
renderShop()
        ↓
loadShopProducts()
        ↓
Promise.all([
  api.getProducts(),
  api.getCategories()
])
        ↓
HTTP GET /api/products
HTTP GET /api/categories
        ↓
Store in window globals
        ↓
populateCategoryFilter()
renderShopProducts()
        ↓
Display Shop Page
```

### Filter Products Flow
```
User selects filter
        ↓
filterProducts()
        ↓
Read from window.allProducts (cached)
        ↓
Apply category filter
Apply status filter
        ↓
renderShopProducts(filtered)
        ↓
Update display
```

---

## Error Handling Strategy

### Frontend Error Handling
1. **Network Errors**: Displayed as error notifications
2. **API Errors**: HTTP status codes trigger error messages
3. **Validation Errors**: Form validation before submission
4. **User Feedback**: Toast notifications for all operations

### Error Response Format
```javascript
{
  "error": "Error message",
  "detail": "Detailed error description",
  "status": 400
}
```

### Common Error Codes
- **400 Bad Request**: Invalid input
- **404 Not Found**: Resource doesn't exist
- **409 Conflict**: Duplicate SKU or name
- **500 Internal Server Error**: Server issue

---

## Performance Optimizations

### Current Optimizations
1. **Parallel Loading**: Shop page loads products and categories together
2. **Cached Data**: Products stored in `window.allProducts` for filtering
3. **Local Filtering**: Category/status filters apply locally without new API calls
4. **Debounced Search**: (Future) Implement debounced search

### Caching Strategy
```javascript
// Shop page caches data in global variables
window.allProducts = products;
window.allCategories = categories;

// Filter operations reuse cached data
filterProducts() {
  let filtered = window.allProducts; // No new API call
}
```

---

## Security Considerations

### Frontend Security
1. **Input Validation**: All forms validate before submission
2. **XSS Prevention**: User input sanitized before display
3. **CSRF Protection**: Relies on backend CSRF middleware
4. **Token Storage**: Auth tokens in localStorage

### Backend Security
1. **Authentication**: JWT-based authentication required
2. **Validation**: All inputs validated server-side
3. **Authorization**: Role-based access control
4. **SQL Injection**: Protected by ORM

---

## Testing Checklist

### Product Management
- [ ] Create product with valid data
- [ ] Create product with duplicate SKU (should fail)
- [ ] Update product status
- [ ] Delete product
- [ ] View all products in admin table
- [ ] Filter products by status

### Category Management
- [ ] Create category with valid data
- [ ] Create category with duplicate name (should fail)
- [ ] Update category status
- [ ] Delete category
- [ ] View all categories in admin table

### Shop Page
- [ ] Load shop page with products
- [ ] Filter by category from dropdown
- [ ] Filter by product status
- [ ] Reset filters returns all products
- [ ] Add product to cart
- [ ] Out of stock products show disabled button

### Error Handling
- [ ] Network error shows notification
- [ ] Invalid input shows error
- [ ] Missing required field shows error
- [ ] Duplicate SKU shows conflict error
- [ ] API errors display user-friendly messages

---

## Future Enhancements

### Planned Features
1. **Edit Operations**: Full edit functionality for products/categories
2. **Bulk Operations**: Bulk delete, bulk update status
3. **Product Images**: Upload and display product images
4. **Advanced Search**: Search by name, SKU, price range
5. **Pagination**: Large product lists with pagination
6. **Product Details**: Detailed product pages with reviews
7. **Inventory Tracking**: Low stock alerts
8. **Export/Import**: CSV export and import

### Code Improvements
1. **Component Architecture**: Break into reusable components
2. **State Management**: Implement proper state management
3. **Type Safety**: Add TypeScript for type checking
4. **Testing**: Unit and integration tests
5. **Documentation**: JSDoc comments on all functions

---

## API Request/Response Examples

### Create Product Request
```json
POST /api/products
{
  "name": "Wireless Keyboard",
  "sku": "TECH-KEYB-001",
  "price": 79.99,
  "status": "AVAILABLE"
}
```

### Create Product Response
```json
{
  "id": 5,
  "name": "Wireless Keyboard",
  "sku": "TECH-KEYB-001",
  "price": 79.99,
  "status": "AVAILABLE"
}
```

### Get All Products Response
```json
[
  {
    "id": 1,
    "name": "Gaming Mouse",
    "sku": "TECH-MOUSE-001",
    "price": 45.99,
    "status": "AVAILABLE"
  },
  {
    "id": 2,
    "name": "USB Hub",
    "sku": "TECH-HUB-001",
    "price": 35.50,
    "status": "OUT_OF_STOCK"
  }
]
```

### Filter Products Request
```
GET /api/products?status=AVAILABLE
GET /api/categories
```

---

## Debugging Tips

### Frontend
- Check browser console (F12) for JavaScript errors
- Use Network tab to inspect API calls
- Check localStorage for cached data
- Use `console.log()` to trace execution

### Backend
- Check server logs for request details
- Use breakpoints in IDE debugger
- Verify database contents directly
- Test endpoints with curl or Postman

### Common Issues
1. **Products don't load**: Check API connection
2. **Categories not in filter**: Verify categories exist in DB
3. **Delete not working**: Check permissions and ID validity
4. **Form not submitting**: Check for validation errors
5. **Filters not working**: Verify cached data exists
