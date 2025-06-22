#!/usr/bin/env python3
import requests
import json

BASE_URL = "http://localhost:8000/api"

def test_api():
    print("Testing API endpoints...")
    
    # Test health check
    try:
        response = requests.get(f"{BASE_URL}/health/")
        print(f"Health check: {response.status_code}")
        if response.status_code == 200:
            print("✅ Backend is running")
        else:
            print("❌ Backend health check failed")
            return
    except Exception as e:
        print(f"❌ Cannot connect to backend: {e}")
        return
    
    # Test registration
    try:
        user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpass123"
        }
        response = requests.post(f"{BASE_URL}/auth/register/", json=user_data)
        print(f"Registration: {response.status_code}")
        if response.status_code == 201:
            print("✅ User registered successfully")
            tokens = response.json()
            access_token = tokens.get('access')
            if access_token:
                headers = {'Authorization': f'Bearer {access_token}'}
                
                # Test creating a chat
                chat_data = {"name": "Test Chat"}
                response = requests.post(f"{BASE_URL}/chats/", json=chat_data, headers=headers)
                print(f"Create chat: {response.status_code}")
                if response.status_code == 201:
                    chat = response.json()
                    chat_id = chat.get('id')
                    print(f"✅ Chat created: {chat_id}")
                    
                    # Test adding a message
                    message_data = {"content": "Hello, this is a test message!"}
                    response = requests.post(f"{BASE_URL}/chats/{chat_id}/add_message/", 
                                          json=message_data, headers=headers)
                    print(f"Add message: {response.status_code}")
                    if response.status_code == 201:
                        print("✅ Message added successfully")
                        message_response = response.json()
                        print(f"User message: {message_response.get('user_message', {}).get('content')}")
                        print(f"AI response: {message_response.get('ai_message', {}).get('content')}")
                    else:
                        print(f"❌ Failed to add message: {response.text}")
                else:
                    print(f"❌ Failed to create chat: {response.text}")
        else:
            print(f"❌ Registration failed: {response.text}")
    except Exception as e:
        print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    test_api() 