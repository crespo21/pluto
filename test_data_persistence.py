#!/usr/bin/env python3
"""
Comprehensive test suite for data persistence and CRUD operations.
Tests that all data is properly saved and retrieved from the database.
"""

import sys
import os
from datetime import datetime
from typing import Optional, Dict, Any

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from sqlalchemy.orm import Session
from infrastructure.database.config import init_db, get_session
from infrastructure.database.models.user_model import UserModel
from infrastructure.database.models.user_profile_model import UserProfileModel
from infrastructure.database.models.product_model import ProductModel
from infrastructure.database.models.category_model import CategoryModel
from domain.entities.user import User
from domain.entities.user_profile import UserProfile
from domain.entities.product import Product
from domain.entities.category import Category
from domain.enums.product_enums import ProductStatus
from domain.enums.category_enums import CategoryStatus
from application.services.user_services import UserService
from application.services.product_services import ProductService
from application.services.category_services import CategoryService
from application.services.user_profile_services import UserProfileService


class Colors:
    """ANSI color codes for terminal output"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'


def print_test(name: str):
    """Print test header"""
    print(f"\n{Colors.BLUE}{'='*70}")
    print(f"TEST: {name}")
    print(f"{'='*70}{Colors.END}")


def print_pass(message: str):
    """Print success message"""
    print(f"{Colors.GREEN}✓ PASS: {message}{Colors.END}")


def print_fail(message: str, error: Optional[str] = None):
    """Print failure message"""
    print(f"{Colors.RED}✗ FAIL: {message}{Colors.END}")
    if error:
        print(f"{Colors.RED}  Error: {error}{Colors.END}")


def print_info(message: str):
    """Print info message"""
    print(f"{Colors.YELLOW}ℹ {message}{Colors.END}")


class DataPersistenceTestSuite:
    """Test suite for verifying data persistence"""
    
    def __init__(self):
        self.session: Optional[Session] = None
        self.test_results = {
            'passed': 0,
            'failed': 0,
            'tests': []
        }
        
    def setup(self):
        """Initialize database and session"""
        print_test("Setting up test environment")
        try:
            print_info("Initializing database...")
            init_db()
            print_pass("Database initialized")
            
            print_info("Creating session...")
            self.session = next(get_session())
            print_pass("Session created")
            
            self.test_results['tests'].append({
                'name': 'Setup',
                'status': 'PASS'
            })
        except Exception as e:
            print_fail("Setup failed", str(e))
            self.test_results['tests'].append({
                'name': 'Setup',
                'status': 'FAIL',
                'error': str(e)
            })
            sys.exit(1)
    
    def teardown(self):
        """Clean up session"""
        if self.session:
            self.session.close()
            print_info("Session closed")
    
    def test_user_creation(self):
        """Test user creation and persistence"""
        print_test("User Creation and Persistence")
        test_name = "User Creation"
        
        try:
            # Create test user via database
            print_info("Creating test user...")
            user_model = UserModel(
                username="testuser_persistence",
                email="testuser@persistence.com",
                password="hashed_password_123",
                status="active"
            )
            self.session.add(user_model)
            self.session.commit()
            user_id = user_model.id
            print_pass(f"User created with ID: {user_id}")
            
            # Verify user is persisted
            print_info("Verifying user persistence...")
            retrieved_user = self.session.query(UserModel).filter(
                UserModel.id == user_id
            ).first()
            
            if retrieved_user and retrieved_user.username == "testuser_persistence":
                print_pass("User successfully persisted and retrieved")
                print_info(f"  - ID: {retrieved_user.id}")
                print_info(f"  - Username: {retrieved_user.username}")
                print_info(f"  - Email: {retrieved_user.email}")
                self.test_results['passed'] += 1
            else:
                raise ValueError("User not found or data mismatch")
                
            self.test_results['tests'].append({
                'name': test_name,
                'status': 'PASS',
                'user_id': user_id
            })
            
        except Exception as e:
            print_fail(test_name, str(e))
            self.test_results['failed'] += 1
            self.test_results['tests'].append({
                'name': test_name,
                'status': 'FAIL',
                'error': str(e)
            })
    
    def test_user_profile_creation(self):
        """Test user profile creation and persistence"""
        print_test("User Profile Creation and Persistence")
        test_name = "User Profile Creation"
        
        try:
            # First create a user
            print_info("Creating parent user...")
            user_model = UserModel(
                username="testuser_profile",
                email="testprofile@test.com",
                password="hashed_password_456",
                status="active"
            )
            self.session.add(user_model)
            self.session.commit()
            user_id = user_model.id
            print_pass(f"User created with ID: {user_id}")
            
            # Create user profile
            print_info("Creating user profile...")
            profile_model = UserProfileModel(
                user_id=user_id,
                first_name="John",
                last_name="Doe",
                phone="+1234567890",
                address="123 Test Street, Test City"
            )
            self.session.add(profile_model)
            self.session.commit()
            profile_id = profile_model.id
            print_pass(f"Profile created with ID: {profile_id}")
            
            # Verify profile is persisted
            print_info("Verifying profile persistence...")
            retrieved_profile = self.session.query(UserProfileModel).filter(
                UserProfileModel.id == profile_id
            ).first()
            
            if retrieved_profile:
                print_pass("Profile successfully persisted and retrieved")
                print_info(f"  - ID: {retrieved_profile.id}")
                print_info(f"  - User ID: {retrieved_profile.user_id}")
                print_info(f"  - First Name: {retrieved_profile.first_name}")
                print_info(f"  - Last Name: {retrieved_profile.last_name}")
                print_info(f"  - Phone: {retrieved_profile.phone}")
                print_info(f"  - Address: {retrieved_profile.address}")
                
                # Verify relationship
                print_info("Verifying user-profile relationship...")
                if retrieved_profile.user_id == user_id:
                    print_pass("User-profile relationship verified")
                
                self.test_results['passed'] += 1
            else:
                raise ValueError("Profile not found")
                
            self.test_results['tests'].append({
                'name': test_name,
                'status': 'PASS',
                'profile_id': profile_id
            })
            
        except Exception as e:
            print_fail(test_name, str(e))
            self.test_results['failed'] += 1
            self.test_results['tests'].append({
                'name': test_name,
                'status': 'FAIL',
                'error': str(e)
            })
    
    def test_product_crud(self):
        """Test product CRUD operations and persistence"""
        print_test("Product CRUD Operations and Persistence")
        test_name = "Product CRUD"
        
        try:
            # CREATE
            print_info("Creating product...")
            product_model = ProductModel(
                name="Test Laptop Pro",
                description="High-performance testing laptop",
                price=1499.99,
                sku="TEST-LAPTOP-001",
                status="available"
            )
            self.session.add(product_model)
            self.session.commit()
            product_id = product_model.id
            print_pass(f"Product created with ID: {product_id}")
            
            # READ
            print_info("Reading product...")
            retrieved = self.session.query(ProductModel).filter(
                ProductModel.id == product_id
            ).first()
            if retrieved:
                print_pass("Product retrieved successfully")
                print_info(f"  - ID: {retrieved.id}")
                print_info(f"  - Name: {retrieved.name}")
                print_info(f"  - Price: ${retrieved.price}")
                print_info(f"  - SKU: {retrieved.sku}")
                print_info(f"  - Status: {retrieved.status}")
            
            # UPDATE
            print_info("Updating product...")
            retrieved.name = "Test Laptop Pro Updated"
            retrieved.price = 1599.99
            self.session.commit()
            print_pass("Product updated")
            
            # VERIFY UPDATE
            print_info("Verifying update...")
            updated = self.session.query(ProductModel).filter(
                ProductModel.id == product_id
            ).first()
            if updated.name == "Test Laptop Pro Updated" and updated.price == 1599.99:
                print_pass("Update verified in database")
            else:
                raise ValueError("Update verification failed")
            
            # DELETE
            print_info("Deleting product...")
            self.session.delete(updated)
            self.session.commit()
            print_pass("Product deleted")
            
            # VERIFY DELETE
            print_info("Verifying deletion...")
            deleted = self.session.query(ProductModel).filter(
                ProductModel.id == product_id
            ).first()
            if deleted is None:
                print_pass("Deletion verified - product not found")
            else:
                raise ValueError("Product still exists after deletion")
            
            self.test_results['passed'] += 1
            self.test_results['tests'].append({
                'name': test_name,
                'status': 'PASS'
            })
            
        except Exception as e:
            print_fail(test_name, str(e))
            self.test_results['failed'] += 1
            self.test_results['tests'].append({
                'name': test_name,
                'status': 'FAIL',
                'error': str(e)
            })
    
    def test_category_crud(self):
        """Test category CRUD operations and persistence"""
        print_test("Category CRUD Operations and Persistence")
        test_name = "Category CRUD"
        
        try:
            # CREATE
            print_info("Creating category...")
            category_model = CategoryModel(
                name="Test Electronics",
                description="Electronics for testing",
                status="active"
            )
            self.session.add(category_model)
            self.session.commit()
            category_id = category_model.id
            print_pass(f"Category created with ID: {category_id}")
            
            # READ
            print_info("Reading category...")
            retrieved = self.session.query(CategoryModel).filter(
                CategoryModel.id == category_id
            ).first()
            if retrieved:
                print_pass("Category retrieved successfully")
                print_info(f"  - ID: {retrieved.id}")
                print_info(f"  - Name: {retrieved.name}")
                print_info(f"  - Description: {retrieved.description}")
                print_info(f"  - Status: {retrieved.status}")
            
            # UPDATE
            print_info("Updating category...")
            retrieved.name = "Test Electronics Updated"
            retrieved.description = "Updated electronics category"
            self.session.commit()
            print_pass("Category updated")
            
            # VERIFY UPDATE
            print_info("Verifying update...")
            updated = self.session.query(CategoryModel).filter(
                CategoryModel.id == category_id
            ).first()
            if updated.name == "Test Electronics Updated":
                print_pass("Update verified in database")
            else:
                raise ValueError("Update verification failed")
            
            # DELETE
            print_info("Deleting category...")
            self.session.delete(updated)
            self.session.commit()
            print_pass("Category deleted")
            
            # VERIFY DELETE
            print_info("Verifying deletion...")
            deleted = self.session.query(CategoryModel).filter(
                CategoryModel.id == category_id
            ).first()
            if deleted is None:
                print_pass("Deletion verified - category not found")
            else:
                raise ValueError("Category still exists after deletion")
            
            self.test_results['passed'] += 1
            self.test_results['tests'].append({
                'name': test_name,
                'status': 'PASS'
            })
            
        except Exception as e:
            print_fail(test_name, str(e))
            self.test_results['failed'] += 1
            self.test_results['tests'].append({
                'name': test_name,
                'status': 'FAIL',
                'error': str(e)
            })
    
    def test_product_category_relationship(self):
        """Test product-category relationship"""
        print_test("Product-Category Relationship")
        test_name = "Product-Category Relationship"
        
        try:
            # Create category
            print_info("Creating category...")
            category_model = CategoryModel(
                name="Test Accessories",
                description="Accessories for testing",
                status="active"
            )
            self.session.add(category_model)
            self.session.commit()
            category_id = category_model.id
            print_pass(f"Category created with ID: {category_id}")
            
            # Create product with category
            print_info("Creating product with category...")
            product_model = ProductModel(
                name="Test USB Cable",
                description="USB-C cable for testing",
                price=19.99,
                sku="TEST-USB-001",
                status="available",
                category_id=category_id
            )
            self.session.add(product_model)
            self.session.commit()
            product_id = product_model.id
            print_pass(f"Product created with ID: {product_id}")
            
            # Verify relationship
            print_info("Verifying product-category relationship...")
            retrieved_product = self.session.query(ProductModel).filter(
                ProductModel.id == product_id
            ).first()
            
            if retrieved_product and retrieved_product.category_id == category_id:
                print_pass("Product-category relationship verified")
                print_info(f"  - Product: {retrieved_product.name}")
                print_info(f"  - Category ID: {retrieved_product.category_id}")
            else:
                raise ValueError("Relationship verification failed")
            
            # Clean up
            self.session.delete(retrieved_product)
            category = self.session.query(CategoryModel).filter(
                CategoryModel.id == category_id
            ).first()
            if category:
                self.session.delete(category)
            self.session.commit()
            
            self.test_results['passed'] += 1
            self.test_results['tests'].append({
                'name': test_name,
                'status': 'PASS'
            })
            
        except Exception as e:
            print_fail(test_name, str(e))
            self.test_results['failed'] += 1
            self.test_results['tests'].append({
                'name': test_name,
                'status': 'FAIL',
                'error': str(e)
            })
    
    def test_data_integrity(self):
        """Test data type integrity"""
        print_test("Data Type and Integrity Validation")
        test_name = "Data Integrity"
        
        try:
            # Create and verify data types
            print_info("Creating product with various data types...")
            product_model = ProductModel(
                name="Data Integrity Test",
                description="Testing data types and constraints",
                price=99.99,
                sku="TEST-DATA-001",
                status="available"
            )
            self.session.add(product_model)
            self.session.commit()
            product_id = product_model.id
            
            print_info("Verifying data types...")
            retrieved = self.session.query(ProductModel).filter(
                ProductModel.id == product_id
            ).first()
            
            checks = [
                ("Name is string", isinstance(retrieved.name, str)),
                ("Price is float", isinstance(retrieved.price, (int, float))),
                ("ID is integer", isinstance(retrieved.id, int)),
                ("Status is string", isinstance(retrieved.status, str)),
            ]
            
            for check_name, result in checks:
                if result:
                    print_pass(f"  ✓ {check_name}")
                else:
                    raise ValueError(f"  ✗ {check_name}")
            
            # Clean up
            self.session.delete(retrieved)
            self.session.commit()
            
            self.test_results['passed'] += 1
            self.test_results['tests'].append({
                'name': test_name,
                'status': 'PASS'
            })
            
        except Exception as e:
            print_fail(test_name, str(e))
            self.test_results['failed'] += 1
            self.test_results['tests'].append({
                'name': test_name,
                'status': 'FAIL',
                'error': str(e)
            })
    
    def run_all_tests(self):
        """Run all tests"""
        print(f"\n{Colors.BLUE}{'='*70}")
        print("STARTING COMPREHENSIVE DATA PERSISTENCE TEST SUITE")
        print(f"{'='*70}{Colors.END}\n")
        
        self.setup()
        
        try:
            self.test_user_creation()
            self.test_user_profile_creation()
            self.test_product_crud()
            self.test_category_crud()
            self.test_product_category_relationship()
            self.test_data_integrity()
        finally:
            self.teardown()
        
        self.print_summary()
    
    def print_summary(self):
        """Print test summary"""
        print(f"\n{Colors.BLUE}{'='*70}")
        print("TEST SUMMARY")
        print(f"{'='*70}{Colors.END}\n")
        
        total = self.test_results['passed'] + self.test_results['failed']
        
        print(f"Total Tests: {total}")
        print(f"{Colors.GREEN}Passed: {self.test_results['passed']}{Colors.END}")
        print(f"{Colors.RED}Failed: {self.test_results['failed']}{Colors.END}")
        
        if self.test_results['failed'] == 0:
            print(f"\n{Colors.GREEN}✓ ALL TESTS PASSED!{Colors.END}")
        else:
            print(f"\n{Colors.RED}✗ SOME TESTS FAILED{Colors.END}")
        
        print(f"\n{Colors.BLUE}Test Details:{Colors.END}")
        for i, test in enumerate(self.test_results['tests'], 1):
            status_color = Colors.GREEN if test['status'] == 'PASS' else Colors.RED
            print(f"  {i}. {status_color}{test['name']}: {test['status']}{Colors.END}")
            if 'error' in test:
                print(f"     Error: {test['error']}")


def main():
    """Main entry point"""
    try:
        suite = DataPersistenceTestSuite()
        suite.run_all_tests()
        return 0 if suite.test_results['failed'] == 0 else 1
    except Exception as e:
        print(f"{Colors.RED}Fatal error: {e}{Colors.END}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
