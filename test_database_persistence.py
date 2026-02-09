#!/usr/bin/env python3
"""
Standalone test for data persistence without import conflicts.
Tests database operations directly using SQLAlchemy.
"""

import sys
import os
from datetime import datetime
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session

# Ensure we're in the right directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Create in-memory database for testing
DATABASE_URL = "sqlite:///test_persistence.db"

def print_header(text):
    """Print section header"""
    print(f"\n{'='*70}")
    print(f"  {text}")
    print(f"{'='*70}\n")

def print_success(text):
    """Print success message"""
    print(f"✓ {text}")

def print_error(text):
    """Print error message"""
    print(f"✗ {text}")

def print_info(text):
    """Print info message"""
    print(f"ℹ {text}")

class DataPersistenceTest:
    """Standalone database persistence test"""
    
    def __init__(self):
        self.engine = None
        self.SessionLocal = None
        self.passed = 0
        self.failed = 0
    
    def setup(self):
        """Initialize database connection"""
        print_header("DATABASE SETUP")
        
        try:
            print_info(f"Connecting to {DATABASE_URL}...")
            self.engine = create_engine(DATABASE_URL, echo=False)
            self.SessionLocal = sessionmaker(bind=self.engine)
            
            # Create tables
            print_info("Creating test tables...")
            from sqlalchemy import text
            with self.engine.connect() as conn:
                # Drop existing tables for clean test
                conn.execute(text("DROP TABLE IF EXISTS test_products"))
                conn.execute(text("DROP TABLE IF EXISTS test_categories"))
                conn.execute(text("DROP TABLE IF EXISTS test_users"))
                conn.commit()
                
                # Create test_users table
                conn.execute(text("""
                    CREATE TABLE test_users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username VARCHAR(255) UNIQUE NOT NULL,
                        email VARCHAR(255) UNIQUE NOT NULL,
                        password VARCHAR(255) NOT NULL,
                        status VARCHAR(50) DEFAULT 'active',
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """))
                
                # Create test_categories table
                conn.execute(text("""
                    CREATE TABLE test_categories (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name VARCHAR(255) UNIQUE NOT NULL,
                        description TEXT,
                        status VARCHAR(50) DEFAULT 'active',
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """))
                
                # Create test_products table
                conn.execute(text("""
                    CREATE TABLE test_products (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name VARCHAR(255) NOT NULL,
                        description TEXT,
                        price REAL NOT NULL,
                        sku VARCHAR(100) UNIQUE,
                        status VARCHAR(50) DEFAULT 'available',
                        category_id INTEGER,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (category_id) REFERENCES test_categories(id)
                    )
                """))
                
                conn.commit()
            
            print_success("Database tables created")
            
        except Exception as e:
            print_error(f"Database setup failed: {e}")
            sys.exit(1)
    
    def test_user_persistence(self):
        """Test user data persistence"""
        print_header("TEST 1: USER DATA PERSISTENCE")
        
        try:
            from sqlalchemy import text
            session = self.SessionLocal()
            
            # INSERT
            print_info("Inserting test user...")
            session.execute(text("""
                INSERT INTO test_users (username, email, password, status)
                VALUES ('testuser', 'test@example.com', 'hashed_pwd_123', 'active')
            """))
            session.commit()
            print_success("User inserted into database")
            
            # SELECT
            print_info("Retrieving user from database...")
            result = session.execute(text("SELECT * FROM test_users WHERE username = 'testuser'"))
            user = result.fetchone()
            
            if user:
                print_success("User retrieved successfully")
                print_info(f"  ID: {user[0]}")
                print_info(f"  Username: {user[1]}")
                print_info(f"  Email: {user[2]}")
                print_info(f"  Status: {user[4]}")
                self.passed += 1
            else:
                print_error("User not found in database")
                self.failed += 1
            
            session.close()
            
        except Exception as e:
            print_error(f"User persistence test failed: {e}")
            self.failed += 1
    
    def test_product_crud(self):
        """Test product CRUD operations"""
        print_header("TEST 2: PRODUCT CRUD OPERATIONS")
        
        try:
            session = self.SessionLocal()
            
            # CREATE
            print_info("Creating product...")
            session.execute("""
                INSERT INTO test_products (name, description, price, sku, status)
                VALUES ('Test Laptop', 'High-performance laptop', 1299.99, 'TEST-001', 'available')
            """)
            session.commit()
            print_success("Product created")
            
            # READ
            print_info("Reading product...")
            result = session.execute("SELECT * FROM test_products WHERE sku = 'TEST-001'")
            product = result.fetchone()
            if product:
                print_success("Product read successfully")
                print_info(f"  ID: {product[0]}")
                print_info(f"  Name: {product[1]}")
                print_info(f"  Price: ${product[3]}")
                print_info(f"  Status: {product[5]}")
            
            # UPDATE
            print_info("Updating product...")
            product_id = product[0]
            session.execute(f"""
                UPDATE test_products 
                SET price = 1499.99, status = 'discontinued'
                WHERE id = {product_id}
            """)
            session.commit()
            print_success("Product updated")
            
            # VERIFY UPDATE
            print_info("Verifying update...")
            result = session.execute(f"SELECT price, status FROM test_products WHERE id = {product_id}")
            updated = result.fetchone()
            if updated[0] == 1499.99 and updated[1] == 'discontinued':
                print_success("Update verified - data persisted correctly")
            else:
                print_error("Update verification failed")
                self.failed += 1
                session.close()
                return
            
            # DELETE
            print_info("Deleting product...")
            session.execute(f"DELETE FROM test_products WHERE id = {product_id}")
            session.commit()
            print_success("Product deleted")
            
            # VERIFY DELETE
            print_info("Verifying deletion...")
            result = session.execute(f"SELECT * FROM test_products WHERE id = {product_id}")
            deleted = result.fetchone()
            if deleted is None:
                print_success("Deletion verified - product not found")
                self.passed += 1
            else:
                print_error("Deletion verification failed")
                self.failed += 1
            
            session.close()
            
        except Exception as e:
            print_error(f"Product CRUD test failed: {e}")
            self.failed += 1
    
    def test_category_persistence(self):
        """Test category persistence"""
        print_header("TEST 3: CATEGORY PERSISTENCE")
        
        try:
            session = self.SessionLocal()
            
            # INSERT
            print_info("Inserting category...")
            session.execute("""
                INSERT INTO test_categories (name, description, status)
                VALUES ('Electronics', 'Electronic devices and accessories', 'active')
            """)
            session.commit()
            print_success("Category inserted")
            
            # SELECT
            print_info("Retrieving category...")
            result = session.execute("SELECT * FROM test_categories WHERE name = 'Electronics'")
            category = result.fetchone()
            
            if category:
                print_success("Category retrieved successfully")
                print_info(f"  ID: {category[0]}")
                print_info(f"  Name: {category[1]}")
                print_info(f"  Description: {category[2]}")
                print_info(f"  Status: {category[3]}")
                self.passed += 1
            else:
                print_error("Category not found")
                self.failed += 1
            
            session.close()
            
        except Exception as e:
            print_error(f"Category persistence test failed: {e}")
            self.failed += 1
    
    def test_relationships(self):
        """Test product-category relationships"""
        print_header("TEST 4: PRODUCT-CATEGORY RELATIONSHIPS")
        
        try:
            session = self.SessionLocal()
            
            # Create category
            print_info("Creating category for relationship test...")
            session.execute("""
                INSERT INTO test_categories (name, description, status)
                VALUES ('Accessories', 'Computer accessories', 'active')
            """)
            session.commit()
            
            # Get category ID
            result = session.execute("SELECT id FROM test_categories WHERE name = 'Accessories'")
            category_id = result.fetchone()[0]
            print_success(f"Category created with ID: {category_id}")
            
            # Create product with category
            print_info("Creating product with category...")
            session.execute(f"""
                INSERT INTO test_products (name, description, price, sku, status, category_id)
                VALUES ('USB Cable', 'High-speed USB-C cable', 29.99, 'ACC-001', 'available', {category_id})
            """)
            session.commit()
            print_success("Product created with category relationship")
            
            # Verify relationship
            print_info("Verifying relationship...")
            result = session.execute(f"""
                SELECT p.name, p.price, c.name 
                FROM test_products p
                JOIN test_categories c ON p.category_id = c.id
                WHERE p.sku = 'ACC-001'
            """)
            joined = result.fetchone()
            
            if joined:
                print_success("Relationship verified")
                print_info(f"  Product: {joined[0]}")
                print_info(f"  Price: ${joined[1]}")
                print_info(f"  Category: {joined[2]}")
                self.passed += 1
            else:
                print_error("Relationship verification failed")
                self.failed += 1
            
            session.close()
            
        except Exception as e:
            print_error(f"Relationship test failed: {e}")
            self.failed += 1
    
    def test_concurrent_operations(self):
        """Test multiple concurrent-like operations"""
        print_header("TEST 5: MULTIPLE CONCURRENT OPERATIONS")
        
        try:
            session = self.SessionLocal()
            
            print_info("Performing multiple inserts...")
            for i in range(3):
                session.execute(f"""
                    INSERT INTO test_products (name, description, price, sku, status)
                    VALUES ('Product {i+1}', 'Test product {i+1}', {50*(i+1)}, 'BULK-{i+1:03d}', 'available')
                """)
            session.commit()
            print_success("Multiple products inserted successfully")
            
            # Verify all inserted
            print_info("Verifying all products were persisted...")
            result = session.execute("SELECT COUNT(*) FROM test_products WHERE sku LIKE 'BULK-%'")
            count = result.fetchone()[0]
            
            if count == 3:
                print_success(f"All {count} products persisted correctly")
                self.passed += 1
            else:
                print_error(f"Expected 3 products, found {count}")
                self.failed += 1
            
            session.close()
            
        except Exception as e:
            print_error(f"Concurrent operations test failed: {e}")
            self.failed += 1
    
    def run_all_tests(self):
        """Run all tests"""
        print("\n" + "="*70)
        print("  DATA PERSISTENCE TEST SUITE")
        print("="*70)
        
        self.setup()
        
        self.test_user_persistence()
        self.test_product_crud()
        self.test_category_persistence()
        self.test_relationships()
        self.test_concurrent_operations()
        
        self.print_summary()
    
    def print_summary(self):
        """Print test summary"""
        print_header("TEST SUMMARY")
        
        total = self.passed + self.failed
        print(f"Total Tests: {total}")
        print(f"Passed: {self.passed}")
        print(f"Failed: {self.failed}")
        
        if self.failed == 0:
            print(f"\n✓ ALL TESTS PASSED!")
            print(f"\nDatabase persists all data correctly:")
            print(f"  ✓ Users are saved and retrieved")
            print(f"  ✓ Products are created, updated, and deleted")
            print(f"  ✓ Categories persist properly")
            print(f"  ✓ Relationships between entities work")
            print(f"  ✓ Multiple operations complete successfully")
            return 0
        else:
            print(f"\n✗ SOME TESTS FAILED")
            return 1


def main():
    """Main entry point"""
    try:
        test = DataPersistenceTest()
        test.run_all_tests()
        return 0 if test.failed == 0 else 1
    except Exception as e:
        print(f"\nFatal error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
