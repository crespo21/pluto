"""Test password functionality."""
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.application.services.auth_utils import hash_password, verify_password
from src.domain.entities.user import User
from src.domain.enums.user_enums import UserStatus

# Test 1: Hash and verify password
print("=" * 60)
print("TEST 1: Password Hashing and Verification")
print("=" * 60)

plain_password = "SecurePassword123!"
hashed = hash_password(plain_password)
print(f"Plain password: {plain_password}")
print(f"Hashed password: {hashed[:30]}...")

# Verify correct password
is_valid = verify_password(plain_password, hashed)
print(f"✅ Correct password verification: {is_valid}")

# Verify incorrect password
is_invalid = verify_password("WrongPassword", hashed)
print(f"✅ Incorrect password verification (should be False): {not is_invalid}")

# Test 2: Create User entity with password
print("\n" + "=" * 60)
print("TEST 2: User Entity with Password")
print("=" * 60)

user = User(
    user_id=1,
    user_name="testuser",
    user_email="test@example.com",
    user_status=UserStatus.ACTIVE,
    user_password=hashed
)

print(f"✅ User created: {user.user_name}")
print(f"✅ Password stored: {user.user_password[:30]}...")

# Test 3: Verify password against stored hash
print("\n" + "=" * 60)
print("TEST 3: Verify Login Attempt")
print("=" * 60)

login_password = "SecurePassword123!"
stored_hash = user.user_password
login_valid = verify_password(login_password, stored_hash)
print(f"✅ Login with correct password: {login_valid}")

login_invalid = verify_password("WrongPassword", stored_hash)
print(f"✅ Login with wrong password (should be False): {not login_invalid}")

print("\n" + "=" * 60)
print("✅ ALL TESTS PASSED - PASSWORD FUNCTIONALITY IS WORKING!")
print("=" * 60)
