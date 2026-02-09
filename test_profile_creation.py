#!/usr/bin/env python
"""Test script for profile creation functionality."""

import requests
import json
import time

BASE_URL = "http://localhost:8000/api"

def test_create_user():
    """Test user creation."""
    print("\n=== Testing User Creation ===")
    user_data = {
        "username": f"testuser_{int(time.time())}",
        "email": f"test_{int(time.time())}@example.com",
        "password": "TestPassword123!@#",
        "status": "ACTIVE"
    }
    
    response = requests.post(f"{BASE_URL}/users", json=user_data)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.json() if response.status_code == 201 else None

def test_login(username, password):
    """Test user login."""
    print("\n=== Testing Login ===")
    credentials = {
        "username": username,
        "password": password
    }
    
    response = requests.post(f"{BASE_URL}/authentications/login", json=credentials)
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Response: {json.dumps(data, indent=2)}")
    return data if response.status_code == 200 else None

def test_check_profile(token, user_id):
    """Test profile check."""
    print("\n=== Testing Profile Check ===")
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.get(f"{BASE_URL}/users/profile/check", headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.json() if response.status_code == 200 else None

def test_create_profile(token, user_id):
    """Test profile creation."""
    print("\n=== Testing Profile Creation ===")
    profile_data = {
        "first_name": "Test",
        "last_name": "User",
        "phone": "+1 (555) 000-0000",
        "address": "123 Test Street"
    }
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(f"{BASE_URL}/users/profile", json=profile_data, headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.json() if response.status_code == 201 else None

def test_get_profile(token):
    """Test get profile."""
    print("\n=== Testing Get Profile ===")
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.get(f"{BASE_URL}/users/profile", headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.json() if response.status_code == 200 else None

def test_get_current_user(token):
    """Test get current user."""
    print("\n=== Testing Get Current User ===")
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.get(f"{BASE_URL}/users/current", headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.json() if response.status_code == 200 else None

if __name__ == "__main__":
    print("Testing Profile Creation Functionality...")
    
    # Create user
    user = test_create_user()
    if not user:
        print("Failed to create user")
        exit(1)
    
    user_id = user["id"]
    username = user["username"]
    
    # Login
    login_response = test_login(username, "TestPassword13!@#")
    if not login_response:
        print("Failed to login")
        exit(1)
    
    token = login_response["token"]
    
    # Check profile (should be false)
    profile_check = test_check_profile(token, user_id)
    if not profile_check:
        print("Failed to check profile")
        exit(1)
    
    print(f"Has profile before creation: {profile_check['has_profile']}")
    
    # Get current user
    current_user = test_get_current_user(token)
    
    # Create profile
    profile = test_create_profile(token, user_id)
    if not profile:
        print("Failed to create profile")
        exit(1)
    
    # Check profile again (should be true)
    profile_check = test_check_profile(token, user_id)
    print(f"Has profile after creation: {profile_check['has_profile']}")
    
    # Get profile
    profile = test_get_profile(token)
    
    print("\n=== All Tests Complete ===")
