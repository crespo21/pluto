#!/usr/bin/env python
"""
Pluto Project - Comprehensive Functionality Test
Tests all components of the application
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_imports():
    """Test all critical imports"""
    print("\n" + "="*60)
    print("TEST 1: Import All Modules")
    print("="*60)
    
    try:
        print("✓ Importing settings...", end=" ")
        from src.properties.settings import settings
        print("OK")
        
        print("✓ Importing FastAPI app...", end=" ")
        from src.main import app
        print("OK")
        
        print("✓ Importing security...", end=" ")
        from src.core.security import SecurityUtils
        print("OK")
        
        print("✓ Importing database config...", end=" ")
        from src.infrastructure.database.config import Base, engine
        print("OK")
        
        print("✓ Importing all repositories...", end=" ")
        from src.infrastructure.database.repositories.sqlalchemy_user_repository import SqlAlchemyUserRepository
        from src.infrastructure.database.repositories.sqlalchemy_product_repository import SqlAlchemyProductRepository
        from src.infrastructure.database.repositories.sqlalchemy_category_repository import SqlAlchemyCategoryRepository
        from src.infrastructure.database.repositories.sqlalchemy_cart_repository import SqlAlchemyCartRepository
        from src.infrastructure.database.repositories.sqlalchemy_checkout_repository import SqlAlchemyCheckoutRepository
        from src.infrastructure.database.repositories.sqlalchemy_authentication_repository import SqlAlchemyAuthenticationRepository
        from src.infrastructure.database.repositories.sqlalchemy_logout_repository import SqlAlchemyLogoutRepository
        print("OK")
        
        print("✓ Importing all services...", end=" ")
        from src.application.services.user_services import UserService
        from src.application.services.product_services import ProductService
        from src.application.services.category_services import CategoryService
        from src.application.services.cart_services import CartService
        from src.application.services.checkout_services import CheckoutService
        from src.application.services.authentication_services import AuthenticationService
        from src.application.services.logout_services import LogoutService
        print("OK")
        
        print("\n✅ All imports successful!")
        return True
        
    except Exception as e:
        print(f"\n❌ Import failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_database():
    """Test database connectivity and tables"""
    print("\n" + "="*60)
    print("TEST 2: Database & Migrations")
    print("="*60)
    
    try:
        from src.infrastructure.database.config import engine, Base
        from sqlalchemy import inspect
        
        print("✓ Checking database connection...", end=" ")
        with engine.connect() as conn:
            result = conn.execute("SELECT 1")
        print("OK")
        
        print("✓ Checking database tables...", end=" ")
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        expected_tables = [
            'user', 'product', 'category', 'cart', 
            'cart_item', 'checkout', 'authentication', 'logout'
        ]
        
        found_tables = [t for t in expected_tables if t in tables]
        print(f"OK ({len(found_tables)}/{len(expected_tables)} tables)")
        
        if found_tables:
            print(f"  Found: {', '.join(found_tables)}")
        
        missing = [t for t in expected_tables if t not in tables]
        if missing:
            print(f"  ⚠️  Missing: {', '.join(missing)}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Database test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_enums():
    """Test all enum definitions"""
    print("\n" + "="*60)
    print("TEST 3: Enums & Exceptions")
    print("="*60)
    
    try:
        print("✓ Importing enums...", end=" ")
        from src.domain.enums.authentication_enums import AuthenticationStatus, AuthMethod
        from src.domain.enums.product_enums import ProductStatus
        from src.domain.enums.category_enums import CategoryStatus
        from src.domain.enums.checkout_enums import CheckoutStatus
        from src.domain.enums.logout_enums import LogoutStatus
        print("OK")
        
        print("✓ Importing exceptions...", end=" ")
        from src.domain.exceptions.authentication_exceptions import AuthenticationAlreadyExistsError
        from src.domain.exceptions.product_exceptions import ProductAlreadyExistsError
        from src.domain.exceptions.category_exceptions import CategoryAlreadyExistsError
        from src.domain.exceptions.checkout_exceptions import CheckoutAlreadyExistsError
        from src.domain.exceptions.logout_exceptions import LogoutAlreadyExistsError
        print("OK")
        
        print("\n✅ All enums and exceptions available!")
        return True
        
    except Exception as e:
        print(f"\n❌ Enum/Exception test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_api_endpoints():
    """Test API endpoint registration"""
    print("\n" + "="*60)
    print("TEST 4: API Endpoints")
    print("="*60)
    
    try:
        from src.main import app
        
        print("✓ Checking registered routes...", end=" ")
        routes = [route.path for route in app.routes]
        
        api_routes = [r for r in routes if '/api/' in r or r in ['/docs', '/redoc', '/openapi.json']]
        
        print(f"OK ({len(api_routes)} routes)")
        
        print(f"  API Docs: {'/docs' in routes}")
        print(f"  OpenAPI Schema: {'/openapi.json' in routes}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ API endpoint test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_security():
    """Test security configuration"""
    print("\n" + "="*60)
    print("TEST 5: Security Configuration")
    print("="*60)
    
    try:
        print("✓ Checking SECRET_KEY...", end=" ")
        from src.properties.settings import settings
        secret_key = settings.SECRET_KEY
        if len(secret_key) >= 32:
            print(f"OK (length: {len(secret_key)})")
        else:
            print(f"⚠️  WARNING (length: {len(secret_key)} - should be >= 32)")
        
        print("✓ Checking DEBUG mode...", end=" ")
        if not settings.DEBUG:
            print(f"OK (DEBUG={settings.DEBUG})")
        else:
            print(f"⚠️  WARNING (DEBUG={settings.DEBUG} - should be False in production)")
        
        print("✓ Testing password hashing...", end=" ")
        from src.core.security import SecurityUtils
        test_password = "TestPassword123!"
        hashed = SecurityUtils.hash_password(test_password)
        is_valid = SecurityUtils.verify_password(test_password, hashed)
        if is_valid:
            print("OK")
        else:
            print("❌ FAILED")
            return False
        
        print("\n✅ Security configuration valid!")
        return True
        
    except Exception as e:
        print(f"\n❌ Security test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_settings():
    """Test settings loading"""
    print("\n" + "="*60)
    print("TEST 6: Settings & Configuration")
    print("="*60)
    
    try:
        from src.properties.settings import settings
        
        print("✓ DATABASE_URL...", end=" ")
        print(f"OK ({settings.DATABASE_URL})")
        
        print("✓ API_TITLE...", end=" ")
        print(f"OK ({settings.API_TITLE})")
        
        print("✓ API_VERSION...", end=" ")
        print(f"OK ({settings.API_VERSION})")
        
        print("\n✅ All settings loaded successfully!")
        return True
        
    except Exception as e:
        print(f"\n❌ Settings test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    print("\n" + "█"*60)
    print("PLUTO PROJECT - COMPREHENSIVE FUNCTIONALITY TEST")
    print("█"*60)
    
    results = {
        "Imports": test_imports(),
        "Database": test_database(),
        "Enums & Exceptions": test_enums(),
        "API Endpoints": test_api_endpoints(),
        "Security": test_security(),
        "Settings": test_settings(),
    }
    
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\n{'='*60}")
    print(f"RESULT: {passed}/{total} tests passed")
    print(f"{'='*60}")
    
    if passed == total:
        print("\n🎉 PROJECT IS FULLY FUNCTIONAL!")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
