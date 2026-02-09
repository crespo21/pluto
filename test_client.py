from src.main import app
from fastapi.testclient import TestClient

print("Creating TestClient...")
client = TestClient(app)

print("Testing GET /api/products...")
response = client.get('/api/products')
print(f'Status: {response.status_code}')
if response.status_code == 200:
    products = response.json()
    print(f'Found {len(products)} products:')
    for product in products[:3]:
        print(f'  - {product.get("name", "Unknown")}: ${product.get("price", 0)}')
else:
    print(f'Error: {response.text}')

print("\nAll tests completed!")
