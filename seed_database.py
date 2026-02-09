"""
Seed script to populate the database with sample products.
Run this script to add sample products to the database.
"""

from src.main import app
from src.infrastructure.database.config import SessionLocal
from src.application.services.product_services import ProductService
from src.application.dto.product_dto import ProductDTO
from src.domain.enums.product_enums import ProductStatus
from src.infrastructure.database.repositories.sqlalchemy_product_repository import SqlAlchemyProductRepository

def seed_products():
    """Add sample products to the database."""
    session = SessionLocal()
    
    try:
        product_repo = SqlAlchemyProductRepository(session)
        product_service = ProductService(product_repo)
        
        # Sample products
        sample_products = [
            ProductDTO(
                id=None,
                name="Laptop Pro",
                description="High-performance laptop for professionals",
                price=1299.99,
                status=ProductStatus.AVAILABLE
            ),
            ProductDTO(
                id=None,
                name="Wireless Mouse",
                description="Ergonomic wireless mouse with 2.4GHz connection",
                price=29.99,
                status=ProductStatus.AVAILABLE
            ),
            ProductDTO(
                id=None,
                name="USB-C Cable",
                description="Premium USB-C cable for fast charging and data transfer",
                price=14.99,
                status=ProductStatus.AVAILABLE
            ),
            ProductDTO(
                id=None,
                name="Mechanical Keyboard",
                description="RGB mechanical keyboard with Cherry switches",
                price=149.99,
                status=ProductStatus.AVAILABLE
            ),
            ProductDTO(
                id=None,
                name="4K Monitor",
                description="27-inch 4K UHD monitor with HDR support",
                price=499.99,
                status=ProductStatus.AVAILABLE
            ),
            ProductDTO(
                id=None,
                name="Webcam HD",
                description="1080p HD webcam with noise-canceling microphone",
                price=89.99,
                status=ProductStatus.AVAILABLE
            ),
        ]
        
        # Create products
        created_count = 0
        for product_dto in sample_products:
            try:
                created_product = product_service.create_product(product_dto)
                print(f"✅ Created: {created_product.name} (${created_product.price})")
                created_count += 1
            except Exception as e:
                print(f"⚠️  Failed to create {product_dto.name}: {str(e)}")
        
        print(f"\n✅ Successfully seeded {created_count} products!")
        
    except Exception as e:
        print(f"❌ Error seeding database: {str(e)}")
    finally:
        session.close()

if __name__ == "__main__":
    seed_products()
