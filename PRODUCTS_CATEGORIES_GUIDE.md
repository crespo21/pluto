# Product & Category Management - Quick Reference

## Frontend Pages

### Shop Page (`/shop`)
Browse and purchase products
- **URL**: http://localhost:8080/#shop
- **Features**:
  - View all available products
  - Filter by category
  - Filter by product status (Available, Out of Stock, Discontinued)
  - Add products to cart
  - Reset filters

**Flow**:
1. Click "Shop" in navigation
2. Browse available products
3. Use dropdown to filter by category
4. Use status filter to show/hide specific product types
5. Click "Add to Cart" on available products

---

### Products Page (Admin)
Manage all products in the system
- **URL**: http://localhost:8080/#products
- **Features**:
  - View all products in table format
  - Create new products
  - Delete products
  - Edit products (coming soon)

**Create Product**:
1. Click "Products" in navigation
2. Click "+ Add Product" button
3. Fill in form:
   - Name: Product name
   - SKU: Stock keeping unit (unique identifier)
   - Price: Numeric price
   - Status: AVAILABLE, OUT_OF_STOCK, or DISCONTINUED
4. Click "Create Product"
5. Product appears in table immediately

**Delete Product**:
1. Find product in table
2. Click "Delete" button
3. Confirm deletion
4. Product removed from system

---

### Categories Page (Admin)
Manage product categories
- **URL**: http://localhost:8080/#categories
- **Features**:
  - View all categories in table format
  - Create new categories
  - Delete categories
  - Edit categories (coming soon)

**Create Category**:
1. Click "Categories" in navigation
2. Click "+ Add Category" button
3. Fill in form:
   - Name: Category name
   - Description: Category description (optional)
   - Status: ACTIVE or INACTIVE
4. Click "Create Category"
5. Category appears in table immediately

**Delete Category**:
1. Find category in table
2. Click "Delete" button
3. Confirm deletion
4. Category removed from system

---

## API Integration Details

### What Happens When You:

#### Create a Product
```
Frontend → API POST /api/products → Backend
Backend → Validate & Store → Database
Database → Returns Product → Frontend
Frontend → Shows success notification
```

#### View All Products
```
Frontend → API GET /api/products → Backend
Backend → Query Database → Returns List
Frontend → Renders Table/Grid
```

#### Delete a Product
```
Frontend → API DELETE /api/products/{id} → Backend
Backend → Removes from Database
Backend → Returns 204 No Content
Frontend → Removes from display
```

#### Filter Products by Category
```
Frontend → API GET /api/categories → Populate filter
User → Selects category
Frontend → Filters cached products locally
Frontend → Re-renders filtered results
```

---

## Data Fields Reference

### Product
- **id**: Auto-generated unique identifier
- **name**: Product name (required, max 100 chars)
- **sku**: Stock Keeping Unit (required, unique)
- **price**: Product price (required, positive number)
- **status**: AVAILABLE | OUT_OF_STOCK | DISCONTINUED

### Category
- **id**: Auto-generated unique identifier
- **name**: Category name (required, max 100 chars)
- **description**: Category description (optional, max 500 chars)
- **status**: ACTIVE | INACTIVE

---

## Common Issues & Solutions

### Issue: Products don't appear in Shop filter
**Solution**: Ensure categories have been created first, then refresh page

### Issue: "Failed to create product" error
**Solution**: Check that:
- All required fields are filled
- Price is a valid number
- SKU is unique (not already used)
- Status is valid

### Issue: Delete button doesn't work
**Solution**: 
- Ensure you have proper permissions
- Check browser console for errors
- Try refreshing the page and try again

### Issue: Category not appearing in filter
**Solution**:
- Ensure category status is ACTIVE
- Refresh the page
- Check that products are linked to the category

---

## Best Practices

1. **Unique SKUs**: Always use unique SKU values - it's the product identifier
2. **Clear Naming**: Use descriptive product and category names
3. **Status Management**: Keep products OUT_OF_STOCK instead of deleting them
4. **Category Organization**: Create categories before adding products
5. **Regular Updates**: Update product statuses as inventory changes

---

## API Response Examples

### Get All Products Response
```json
[
  {
    "id": 1,
    "name": "Laptop",
    "sku": "TECH-001",
    "price": 999.99,
    "status": "AVAILABLE"
  },
  {
    "id": 2,
    "name": "Mouse",
    "sku": "TECH-002",
    "price": 25.50,
    "status": "AVAILABLE"
  }
]
```

### Get All Categories Response
```json
[
  {
    "id": 1,
    "name": "Electronics",
    "description": "Electronic devices and accessories",
    "status": "ACTIVE"
  },
  {
    "id": 2,
    "name": "Books",
    "description": "Books and reading materials",
    "status": "ACTIVE"
  }
]
```

---

## Navigation Map

```
Home (/)
├── Shop (/shop)
│   ├── Browse Products
│   ├── Filter by Category
│   ├── Add to Cart
│   └── Proceed to Checkout
├── Products (/products) [Admin]
│   ├── Create Product
│   ├── View Products Table
│   ├── Delete Product
│   └── Edit Product [Coming Soon]
├── Categories (/categories) [Admin]
│   ├── Create Category
│   ├── View Categories Table
│   ├── Delete Category
│   └── Edit Category [Coming Soon]
└── Profile
```

---

## Keyboard Shortcuts (Future)
- `Ctrl + K`: Quick search
- `Shift + P`: Go to Products
- `Shift + C`: Go to Categories
- `Shift + S`: Go to Shop

(To be implemented in future version)
