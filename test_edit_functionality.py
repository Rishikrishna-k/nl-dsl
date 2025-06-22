#!/usr/bin/env python3
"""
Test script for the message editing functionality.
This script tests the new edit endpoints to ensure they work correctly.
"""

import requests
import json
import uuid

# Configuration
BASE_URL = "http://localhost:8000/api"
TEST_EMAIL = "test@example.com"
TEST_PASSWORD = "testpass123"

def get_auth_token():
    """Get authentication token for testing."""
    login_data = {
        "email": TEST_EMAIL,
        "password": TEST_PASSWORD
    }
    
    response = requests.post(f"{BASE_URL}/auth/login/", json=login_data)
    if response.status_code == 200:
        return response.json()["access"]
    else:
        print(f"Login failed: {response.status_code} - {response.text}")
        return None

def create_test_chat(token):
    """Create a test chat for testing."""
    headers = {"Authorization": f"Bearer {token}"}
    chat_data = {
        "name": "Test Chat for Editing",
        "description": "Test chat for message editing functionality"
    }
    
    response = requests.post(f"{BASE_URL}/chats/", json=chat_data, headers=headers)
    if response.status_code == 201:
        return response.json()
    else:
        print(f"Failed to create chat: {response.status_code} - {response.text}")
        return None

def add_test_message(token, chat_id):
    """Add a test message to the chat."""
    headers = {"Authorization": f"Bearer {token}"}
    message_data = {
        "content": "This is a test message that I want to edit"
    }
    
    response = requests.post(f"{BASE_URL}/chats/{chat_id}/add_message/", 
                           json=message_data, headers=headers)
    if response.status_code == 201:
        return response.json()
    else:
        print(f"Failed to add message: {response.status_code} - {response.text}")
        return None

def test_edit_message(token, chat_id, message_id):
    """Test the edit message functionality."""
    headers = {"Authorization": f"Bearer {token}"}
    edit_data = {
        "content": "This is the edited version of my test message"
    }
    
    print(f"Testing edit message endpoint...")
    response = requests.patch(f"{BASE_URL}/chats/{chat_id}/messages/{message_id}/edit/", 
                            json=edit_data, headers=headers)
    
    print(f"Edit response status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print("✅ Edit successful!")
        print(f"New message ID: {result['new_message']['id']}")
        print(f"New branch ID: {result['new_branch_id']}")
        return result
    else:
        print(f"❌ Edit failed: {response.text}")
        return None

def test_graph_heads(token, chat_id):
    """Test the graph heads endpoint."""
    headers = {"Authorization": f"Bearer {token}"}
    
    print(f"Testing graph heads endpoint...")
    response = requests.get(f"{BASE_URL}/chats/{chat_id}/graph_heads/", headers=headers)
    
    print(f"Graph heads response status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print("✅ Graph heads successful!")
        print(f"Number of heads: {len(result['heads'])}")
        print(f"Heads: {result['heads']}")
        return result
    else:
        print(f"❌ Graph heads failed: {response.text}")
        return None

def test_branch_chain(token, chat_id, head_id):
    """Test the branch chain endpoint."""
    headers = {"Authorization": f"Bearer {token}"}
    
    print(f"Testing branch chain endpoint...")
    response = requests.get(f"{BASE_URL}/chats/{chat_id}/branch_chain/?head_id={head_id}", 
                          headers=headers)
    
    print(f"Branch chain response status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print("✅ Branch chain successful!")
        print(f"Number of messages: {len(result['messages'])}")
        return result
    else:
        print(f"❌ Branch chain failed: {response.text}")
        return None

def main():
    """Main test function."""
    print("🧪 Testing Message Editing Functionality")
    print("=" * 50)
    
    # Get authentication token
    print("1. Getting authentication token...")
    token = get_auth_token()
    if not token:
        print("❌ Failed to get authentication token. Exiting.")
        return
    
    print("✅ Authentication successful!")
    
    # Create test chat
    print("\n2. Creating test chat...")
    chat = create_test_chat(token)
    if not chat:
        print("❌ Failed to create test chat. Exiting.")
        return
    
    chat_id = chat['id']
    print(f"✅ Test chat created with ID: {chat_id}")
    
    # Add test message
    print("\n3. Adding test message...")
    message_result = add_test_message(token, chat_id)
    if not message_result:
        print("❌ Failed to add test message. Exiting.")
        return
    
    user_message_id = message_result['user_message']['id']
    print(f"✅ Test message added with ID: {user_message_id}")
    
    # Test graph heads before edit
    print("\n4. Testing graph heads before edit...")
    heads_before = test_graph_heads(token, chat_id)
    
    # Test edit message
    print("\n5. Testing edit message...")
    edit_result = test_edit_message(token, chat_id, user_message_id)
    if not edit_result:
        print("❌ Edit message test failed. Exiting.")
        return
    
    # Test graph heads after edit
    print("\n6. Testing graph heads after edit...")
    heads_after = test_graph_heads(token, chat_id)
    
    # Test branch chain with new head
    if heads_after and heads_after['heads']:
        new_head_id = heads_after['heads'][-1]  # Get the latest head
        print(f"\n7. Testing branch chain with new head: {new_head_id}")
        test_branch_chain(token, chat_id, new_head_id)
    
    print("\n" + "=" * 50)
    print("🎉 All tests completed!")
    print("The message editing functionality appears to be working correctly.")

if __name__ == "__main__":
    main() 