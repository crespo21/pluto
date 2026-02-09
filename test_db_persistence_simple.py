#!/usr/bin/env python3
"""Simple and direct data persistence test."""
import sys, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///test_persistence.db"
passed, failed = 0, 0

def setup_db():
    """Setup test database"""
    global passed, failed
    print("\n" + "="*70)
    print("DATABASE SETUP")
    print("="*70 + "\n")
    
    try:
        engine = create_engine(DATABASE_URL, echo=False)
        with engine.connect() as conn:
            conn.execute(text("DROP TABLE IF EXISTS test_products"))
            conn.execute(text("DROP TABLE IF EXISTS test_categories"))
            conn.execute(text("DROP TABLE IF EXISTS test_users"))
            
            conn.execute(text("CREATE TABLE test_users (id INTEGER PRIMARY KEY, username VARCHAR UNIQUE, email VARCHAR UNIQUE, password VARCHAR, status VARCHAR DEFAULT 'active')"))
            conn.execute(text("CREATE TABLE test_categories (id INTEGER PRIMARY KEY, name VARCHAR UNIQUE, description TEXT, status VARCHAR DEFAULT 'active')"))
            conn.execute(text("CREATE TABLE test_products (id INTEGER PRIMARY KEY, name VARCHAR, description TEXT, price REAL, sku VARCHAR UNIQUE, status VARCHAR DEFAULT 'available', category_id INTEGER, FOREIGN KEY (category_id) REFERENCES test_categories(id))"))
            
            conn.commit()
        print("✓ Database tables created\n")
        return engine
    except Exception as e:
        print(f"✗ Setup failed: {e}")
        sys.exit(1)

def test1_user_persistence(engine):
    """Test 1: User persistence"""
    global passed, failed
    print("="*70)
    print("TEST 1: USER DATA PERSISTENCE")
    print("="*70 + "\n")
    
    try:
        Session = sessionmaker(bind=engine)
        session = Session()
        
        print("✓ Inserting test user...")
        session.execute(text("INSERT INTO test_users (username, email, password, status) VALUES ('testuser', 'test@example.com', 'hashed_pwd_123', 'active')"))
        session.commit()
        
        print("✓ Retrieving user...")
        result = session.execute(text("SELECT * FROM test_users WHERE username = 'testuser'"))
        user = result.fetchone()
        
        if user:
            print("✓ User retrieved successfully")
            print(f"  ID: {user[0]}, Username: {user[1]}, Email: {user[2]}, Status: {user[4]}")
            passed += 1
        else:
            print("✗ User not found")
            failed += 1
        
        session.close()
    except Exception as e:
        print(f"✗ Test failed: {e}")
        failed += 1
    
    print()

def test2_product_crud(engine):
    """Test 2: Product CRUD"""
    global passed, failed
    print("="*70)
    print("TEST 2: PRODUCT CRUD OPERATIONS")
    print("="*70 + "\n")
    
    try:
        Session = sessionmaker(bind=engine)
        session = Session()
        
        # CREATE
        print("✓ Creating product...")
        session.execute(text("INSERT INTO test_products (name, description, price, sku, status) VALUES ('Test Laptop', 'High-performance laptop', 1299.99, 'TEST-001', 'available')"))
        session.commit()
        
        # READ
        print("✓ Reading product...")
        result = session.execute(text("SELECT * FROM test_products WHERE sku = 'TEST-001'"))
        product = result.fetchone()
        if product:
            print(f"✓ Product found: ID={product[0]}, Name={product[1]}, Price=${product[3]}")
        
        # UPDATE
        print("✓ Updating product...")
        product_id = product[0]
        session.execute(text(f"UPDATE test_products SET price = 1499.99, status = 'discontinued' WHERE id = {product_id}"))
        session.commit()
        
        # VERIFY UPDATE
        result = session.execute(text(f"SELECT price, status FROM test_products WHERE id = {product_id}"))
        updated = result.fetchone()
        if updated[0] == 1499.99 and updated[1] == 'discontinued':
            print("✓ Update verified - data persisted correctly")
        else:
            print("✗ Update verification failed")
            failed += 1
            session.close()
            return
        
        # DELETE
        print("✓ Deleting product...")
        session.execute(text(f"DELETE FROM test_products WHERE id = {product_id}"))
        session.commit()
        
        # VERIFY DELETE
        result = session.execute(text(f"SELECT * FROM test_products WHERE id = {product_id}"))
        deleted = result.fetchone()
        if deleted is None:
            print("✓ Deletion verified - product not found")
            passed += 1
        else:
            print("✗ Deletion verification failed")
            failed += 1
        
        session.close()
    except Exception as e:
        print(f"✗ Test failed: {e}")
        failed += 1
    
    print()

def test3_category_persistence(engine):
    """Test 3: Category persistence"""
    global passed, failed
    print("="*70)
    print("TEST 3: CATEGORY PERSISTENCE")
    print("="*70 + "\n")
    
    try:
        Session = sessionmaker(bind=engine)
        session = Session()
        
        # INSERT
        print("✓ Inserting category...")
        session.execute(text("INSERT INTO test_categories (name, description, status) VALUES ('Electronics', 'Electronic devices and accessories', 'active')"))
        session.commit()
        
        # SELECT
        print("✓ Retrieving category...")
        result = session.execute(text("SELECT * FROM test_categories WHERE name = 'Electronics'"))
        category = result.fetchone()
        
        if category:
            print("✓ Category retrieved successfully")
            print(f"  ID: {category[0]}, Name: {category[1]}, Status: {category[3]}")
            passed += 1
        else:
            print("✗ Category not found")
            failed += 1
        
        session.close()
    except Exception as e:
        print(f"✗ Test failed: {e}")
        failed += 1
    
    print()

def test4_relationships(engine):
    """Test 4: Product-Category relationships"""
    global passed, failed
    print("="*70)
    print("TEST 4: PRODUCT-CATEGORY RELATIONSHIPS")
    print("="*70 + "\n")
    
    try:
        Session = sessionmaker(bind=engine)
        session = Session()
        
        # Create category
        print("✓ Creating category...")
        session.execute(text("INSERT INTO test_categories (name, description, status) VALUES ('Accessories', 'Computer accessories', 'active')"))
        session.commit()
        
        # Get category ID
        result = session.execute(text("SELECT id FROM test_categories WHERE name = 'Accessories'"))
        category_id = result.fetchone()[0]
        print(f"✓ Category created with ID: {category_id}")
        
        # Create product with category
        print("✓ Creating product with category...")
        session.execute(text(f"INSERT INTO test_products (name, description, price, sku, status, category_id) VALUES ('USB Cable', 'High-speed USB-C cable', 29.99, 'ACC-001', 'available', {category_id})"))
        session.commit()
        
        # Verify relationship
        print("✓ Verifying relationship...")
        result = session.execute(text(f"SELECT p.name, p.price, c.name FROM test_products p JOIN test_categories c ON p.category_id = c.id WHERE p.sku = 'ACC-001'"))
        joined = result.fetchone()
        
        if joined:
            print("✓ Relationship verified")
            print(f"  Product: {joined[0]}, Price: ${joined[1]}, Category: {joined[2]}")
            passed += 1
        else:
            print("✗ Relationship verification failed")
            failed += 1
        
        session.close()
    except Exception as e:
        print(f"✗ Test failed: {e}")
        failed += 1
    
    print()

def test5_concurrent_operations(engine):
    """Test 5: Multiple concurrent operations"""
    global passed, failed
    print("="*70)
    print("TEST 5: MULTIPLE CONCURRENT OPERATIONS")
    print("="*70 + "\n")
    
    try:
        Session = sessionmaker(bind=engine)
        session = Session()
        
        print("✓ Performing multiple inserts...")
        for i in range(3):
            sku = f"BULK-{i+1:03d}"
            session.execute(text(f"INSERT INTO test_products (name, description, price, sku, status) VALUES ('Product {i+1}', 'Test product {i+1}', {50*(i+1)}, '{sku}', 'available')"))
        session.commit()
        
        # Verify all inserted
        print("✓ Verifying all products persisted...")
        result = session.execute(text("SELECT COUNT(*) FROM test_products WHERE sku LIKE 'BULK-%'"))
        count = result.fetchone()[0]
        
        if count == 3:
            print(f"✓ All {count} products persisted correctly")
            passed += 1
        else:
            print(f"✗ Expected 3 products, found {count}")
            failed += 1
        
        session.close()
    except Exception as e:
        print(f"✗ Test failed: {e}")
        failed += 1
    
    print()

def print_summary():
    """Print test summary"""
    global passed, failed
    total = passed + failed
    print("="*70)
    print("TEST SUMMARY")
    print("="*70 + "\n")
    print(f"Total Tests: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}\n")
    
    if failed == 0:
        print("✓ ALL TESTS PASSED!\n")
        print("Database persists all data correctly:")
        print("  ✓ Users are saved and retrieved")
        print("  ✓ Products are created, updated, and deleted")
        print("  ✓ Categories persist properly")
        print("  ✓ Relationships between entities work")
        print("  ✓ Multiple operations complete successfully\n")
        return 0
    else:
        print("✗ SOME TESTS FAILED\n")
        return 1

if __name__ == "__main__":
    print("\n" + "="*70)
    print("DATA PERSISTENCE TEST SUITE")
    print("="*70)
    
    engine = setup_db()
    test1_user_persistence(engine)
    test2_product_crud(engine)
    test3_category_persistence(engine)
    test4_relationships(engine)
    test5_concurrent_operations(engine)
    
    exit_code = print_summary()
    sys.exit(exit_code)
