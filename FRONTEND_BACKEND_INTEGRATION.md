# Frontend-Backend Integration Guide

## Overview
This document explains how the frontend interacts with the backend API for products and categories.

## API Endpoints

### Products Endpoints

#### GET `/api/products`
- **Description**: Retrieve all products
- **Response**: Array of ProductResponse objects
- **Response Schema**:
```json
[
  {
    "id": 1,
    "name": "Product Name",
    "sku": "PROD-001",
    "price": 29.99,
    "status": "AVAILABLE"
  }
]
```

#### POST `/api/products`
- **Description**: Create a new product
- **Request Body**:
```json
{
  "name": "Product Name",
  "sku": "PROD-001",
  "price": 29.99,
  "status": "AVAILABLE"
}
```

#### GET `/api/products/{product_id}`
- **Description**: Get a specific product by ID
- **Parameters**: `product_id` (integer)

#### PATCH `/api/products/{product_id}`
- **Description**: Update a product partially
- **Request Body**: Any of the product fields

#### PATCH `/api/products/{product_id}/status`
- **Description**: Update only the product status
- **Request Body**:
```json
{
  "status": "AVAILABLE"
}
```

#### DELETE `/api/products/{product_id}`
- **Description**: Delete a product
- **Status Code**: 204 No Content

---

### Categories Endpoints

#### GET `/api/categories`
- **Description**: Retrieve all categories
- **Response**: Array of CategoryResponse objects
- **Response Schema**:
```json
[
  {
    "id": 1,
    "name": "Electronics",
    "description": "Electronic devices and accessories",
    "status": "ACTIVE"
  }
]
```

#### POST `/api/categories`
- **Description**: Create a new category
- **Request Body**:
```json
{
  "name": "Electronics",
  "description": "Electronic devices and accessories",
  "status": "ACTIVE"
}
```

#### GET `/api/categories/{category_id}`
- **Description**: Get a specific category by ID
- **Parameters**: `category_id` (integer)

#### PATCH `/api/categories/{category_id}`
- **Description**: Update a category partially
- **Request Body**: Any of the category fields

#### PATCH `/api/categories/{category_id}/status`
- **Description**: Update only the category status
- **Request Body**:
```json
{
  "status": "ACTIVE"
}
```

#### DELETE `/api/categories/{category_id}`
- **Description**: Delete a category
- **Status Code**: 204 No Content

---

## Frontend Implementation

### API Client Methods (api.js)

#### Products
- `api.getProducts()` - Fetch all products
- `api.getProduct(productId)` - Fetch specific product
- `api.createProduct(name, sku, price, status)` - Create product
- `api.updateProduct(productId, data)` - Update product
- `api.deleteProduct(productId)` - Delete product

#### Categories
- `api.getCategories()` - Fetch all categories
- `api.getCategory(categoryId)` - Fetch specific category
- `api.createCategory(name, description, status)` - Create category
- `api.updateCategory(categoryId, data)` - Update category
- `api.deleteCategory(categoryId)` - Delete category

### Page Renderers (pages.js)

#### renderProducts()
- Displays admin panel for product management
- Shows form to create new products
- Displays table of all products with edit/delete buttons

#### renderCategories()
- Displays admin panel for category management
- Shows form to create new categories
- Displays table of all categories with edit/delete buttons

#### renderShop()
- Displays shop page with product browsing
- Includes filters by category and status
- Shows product cards with "Add to Cart" button
- Loads both products and categories for filtering

#### renderHome()
- Home page with promotional content
- Shows platform features
- Links to shop and products pages

### Key Functions

#### loadShopProducts()
- Fetches all products and categories in parallel
- Stores them globally for filtering
- Populates category filter dropdown
- Renders product cards

#### filterProducts()
- Filters products by selected category and status
- Uses cached product data for fast filtering
- Re-renders product grid

#### handleProductSubmit(e)
- Form handler for creating new products
- Validates form input
- Calls API to create product
- Refreshes product list

#### handleCategorySubmit(e)
- Form handler for creating new categories
- Validates form input
- Calls API to create category
- Refreshes category list

---

## Data Flow

### Product Management Flow
1. User navigates to "Products" page
2. Frontend calls `api.getProducts()`
3. Backend returns list of all products
4. Frontend displays products in table format
5. User can:
   - Create new product via form
   - Edit product (feature in progress)
   - Delete product via API call

### Shop Page Flow
1. User navigates to "Shop" page
2. Frontend loads both products and categories in parallel
3. Products displayed in grid with category options
4. User can:
   - Filter by category from dropdown
   - Filter by product status
   - Add product to cart
   - Reset filters

### Category Management Flow
1. User navigates to "Categories" page
2. Frontend calls `api.getCategories()`
3. Backend returns list of all categories
4. Frontend displays categories in table format
5. User can:
   - Create new category via form
   - Edit category (feature in progress)
   - Delete category via API call

---

## Status Codes

### Product/Category Statuses
- `AVAILABLE` - Product is available for purchase
- `OUT_OF_STOCK` - Product is out of stock
- `DISCONTINUED` - Product is discontinued
- `ACTIVE` - Category is active (for categories)
- `INACTIVE` - Category is inactive (for categories)

---

## Error Handling

All API calls include error handling:
- Network errors are caught and displayed as notifications
- HTTP errors are returned with descriptive messages
- Failed operations show user-friendly error messages
- Notifications display success/error status

---

## Frontend Improvements Made

1. **Unified API Client** - All products/categories methods now properly integrated
2. **Delete Operations** - Proper DELETE endpoint calls instead of status updates
3. **Filtering** - Category and status filtering with cached data
4. **Parallel Loading** - Shop page loads products and categories simultaneously
5. **Error Handling** - Comprehensive error notifications for all operations
6. **Form Validation** - Clear input fields after successful submission

---

## Testing the Integration

### Test Product Creation
1. Navigate to Products page
2. Click "Add Product" button
3. Fill in: Name, SKU, Price, Status
4. Click "Create Product"
5. Product should appear in table

### Test Product Filtering
1. Navigate to Shop page
2. Wait for products and categories to load
3. Select a category from dropdown
4. Products should filter by selection

### Test Category Creation
1. Navigate to Categories page
2. Click "Add Category" button
3. Fill in: Name, Description, Status
4. Click "Create Category"
5. Category should appear in table

---

## Future Enhancements

1. **Edit Operations** - Implement product/category edit functionality
2. **Product Images** - Add image upload support
3. **Advanced Filtering** - Price range, search by name
4. **Bulk Operations** - Bulk product management
5. **Product Details** - Detailed product information pages
