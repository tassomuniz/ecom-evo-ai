#!/usr/bin/env python3
"""
Test script for profile update API
Use this on the server to test the new functionality
"""

import requests
import json
import sys

def test_profile_api(base_url="http://localhost:8000", email="admin@admin.com", password="admin123"):
    """Test the profile update API"""
    
    print("🧪 Testing Profile Update API")
    print("=" * 50)
    
    # Step 1: Login to get JWT token
    print("\n📋 Step 1: Login to get JWT token...")
    login_data = {
        "email": email,
        "password": password
    }
    
    try:
        response = requests.post(f"{base_url}/auth/login", json=login_data)
        if response.status_code != 200:
            print(f"❌ Login failed: {response.status_code} - {response.text}")
            return False
            
        token_data = response.json()
        token = token_data.get("access_token")
        print(f"✅ Login successful, token obtained")
        
    except Exception as e:
        print(f"❌ Login error: {e}")
        return False
    
    # Step 2: Get current profile
    print("\n📋 Step 2: Get current profile...")
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.post(f"{base_url}/auth/me", headers=headers)
        if response.status_code != 200:
            print(f"❌ Get profile failed: {response.status_code} - {response.text}")
            return False
            
        current_profile = response.json()
        print(f"✅ Current profile: {json.dumps(current_profile, indent=2)}")
        
    except Exception as e:
        print(f"❌ Get profile error: {e}")
        return False
    
    # Step 3: Test profile update (name only)
    print("\n📋 Step 3: Test profile update (name only)...")
    update_data = {
        "name": "Admin Updated"
    }
    
    try:
        response = requests.put(f"{base_url}/auth/profile", json=update_data, headers=headers)
        if response.status_code != 200:
            print(f"❌ Profile update failed: {response.status_code} - {response.text}")
            return False
            
        updated_profile = response.json()
        print(f"✅ Profile updated successfully: {json.dumps(updated_profile, indent=2)}")
        
    except Exception as e:
        print(f"❌ Profile update error: {e}")
        return False
    
    # Step 4: Verify the update
    print("\n📋 Step 4: Verify the update...")
    try:
        response = requests.post(f"{base_url}/auth/me", headers=headers)
        if response.status_code != 200:
            print(f"❌ Verification failed: {response.status_code} - {response.text}")
            return False
            
        verified_profile = response.json()
        print(f"✅ Verified profile: {json.dumps(verified_profile, indent=2)}")
        
        if verified_profile.get("name") == "Admin Updated":
            print("✅ Name update verified successfully!")
        else:
            print("❌ Name update verification failed!")
            return False
            
    except Exception as e:
        print(f"❌ Verification error: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("🎯 ALL TESTS PASSED! ✅")
    print("🚀 Profile update functionality is working!")
    
    return True

def main():
    """Main function"""
    if len(sys.argv) > 1:
        base_url = sys.argv[1]
    else:
        base_url = "http://localhost:8000"
    
    print(f"Testing API at: {base_url}")
    
    success = test_profile_api(base_url)
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main()) 