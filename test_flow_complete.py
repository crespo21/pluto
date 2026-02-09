"""
Comprehensive end-to-end test of the e-commerce application flow.
Tests: Authentication → Products → Cart → Checkout
"""
from src.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

print("=" * 70)
print("COMPLETE E-COMMERCE FLOW TEST")
print("=" * 70)

# Step 1: Register a new user
print("\n1. REGISTER USER")
print("-" * 70)
register_data = {
    "username": "testuser",
    "email": "testuser@example.com",
    "password": "SecurePassword123!",
    "status": "ACTIVE"
}
response = client.post('/api/users', json=register_data)
print(f"   Status: {response.status_code}")
if response.status_code in [200, 201]:
    user = response.json()
    user_id = user.get("id")
    print(f"   ✓ User registered: ID={user_id}, Username={user.get('username')}")
else:
    print(f"   ✗ Error: {response.json()}")
    user_id = None

# Step 2: Get all products
print("\n2. GET PRODUCTS CATALOG")
print("-" * 70)
response = client.get('/api/products')
print(f"   Status: {response.status_code}")
if response.status_code == 200:
    products = response.json()
    print(f"   ✓ Found {len(products)} products")
    # Take first 3 products
    selected_products = products[:3]
    for i, product in enumerate(selected_products, 1):
        print(f"      {i}. {product.get('name')}: ${product.get('price')} (ID: {product.get('id')})")
    product_ids = [p.get('id') for p in selected_products]
else:
    print(f"   ✗ Error: {response.json()}")
    product_ids = []

# Step 3: Create a cart
print("\n3. CREATE SHOPPING CART")
print("-" * 70)
if user_id:
    cart_data = {"user_id": user_id}
    response = client.post('/api/carts', json=cart_data)
    print(f"   Status: {response.status_code}")
    if response.status_code in [200, 201]:
        cart = response.json()
        cart_id = cart.get('id')
        print(f"   ✓ Cart created: ID={cart_id}, Status={cart.get('status')}")
    else:
        print(f"   ✗ Error: {response.json()}")
        cart_id = None
else:
    print("   ✗ Skipped (no user)")
    cart_id = None

# Step 4: Add products to cart
print("\n4. ADD PRODUCTS TO CART")
print("-" * 70)
if cart_id and product_ids:
    for product_id in product_ids:
        cart_item_data = {"cart_id": cart_id, "product_id": product_id, "quantity": 1}
        response = client.post('/api/carts/items', json=cart_item_data)
        print(f"   Status: {response.status_code} for Product ID {product_id}")
        if response.status_code in [200, 201]:
            print(f"      ✓ Product {product_id} added to cart")
        else:
            print(f"      ✗ Error: {response.json()}")
else:
    print("   ✗ Skipped (no cart or products)")

# Step 5: Get cart details
print("\n5. VIEW CART DETAILS")
print("-" * 70)
if cart_id:
    response = client.get(f'/api/carts/{cart_id}')
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        cart = response.json()
        print(f"   ✓ Cart ID: {cart.get('id')}")
        print(f"   ✓ Status: {cart.get('status')}")
        print(f"   ✓ User ID: {cart.get('user_id')}")
    else:
        print(f"   ✗ Error: {response.json()}")
else:
    print("   ✗ Skipped (no cart)")

# Step 6: Checkout
print("\n6. CHECKOUT")
print("-" * 70)
if cart_id:
    checkout_data = {"cart_id": cart_id, "payment_method": "CREDIT_CARD"}
    response = client.post('/api/checkout', json=checkout_data)
    print(f"   Status: {response.status_code}")
    if response.status_code in [200, 201]:
        checkout = response.json()
        print(f"   ✓ Checkout successful!")
        print(f"   ✓ Checkout ID: {checkout.get('id')}")
        print(f"   ✓ Payment Method: {checkout.get('payment_method')}")
    else:
        print(f"   ✗ Error: {response.json()}")
else:
    print("   ✗ Skipped (no cart)")

# Step 7: Get user profile
print("\n7. GET USER PROFILE")
print("-" * 70)
if user_id:
    response = client.get(f'/api/users/{user_id}')
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        user = response.json()
        print(f"   ✓ Username: {user.get('username')}")
        print(f"   ✓ Email: {user.get('email')}")
        print(f"   ✓ Status: {user.get('status')}")
    else:
        print(f"   ✗ Error: {response.json()}")
else:
    print("   ✗ Skipped (no user)")

print("\n" + "=" * 70)
print("FLOW TEST COMPLETED")
print("=" * 70)
