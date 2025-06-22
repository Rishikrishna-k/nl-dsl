#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import time

# API base URL
BASE_URL = "http://localhost:8000/api"

def test_api_only():
    """Test the enhanced edit functionality using only API endpoints"""
    
    print("=== Testing Enhanced Edit Functionality (API Only) ===")
    
    # Test user credentials
    test_user = {
        "username": "testuser_api",
        "email": "testuser_api@example.com",
        "password": "testpass123"
    }
    
    # Step 1: Register user
    print("\n1. Registering test user...")
    register_response = requests.post(f"{BASE_URL}/auth/register/", json=test_user)
    print(f"Register response: {register_response.status_code} {register_response.text}")
    
    if register_response.status_code == 201:
        print("✓ User registered successfully")
        user_data = register_response.json()
        print(f"   User ID: {user_data.get('id')}")
    elif register_response.status_code == 400:
        print("! User might already exist, trying to login...")
    else:
        print(f"✗ Registration failed: {register_response.status_code}")
        print(register_response.text)
        return
    
    # Step 2: Login
    print("\n2. Logging in...")
    login_data = {
        "email": test_user["email"],
        "password": test_user["password"]
    }
    
    login_response = requests.post(f"{BASE_URL}/auth/login/", json=login_data)
    print(f"Login response: {login_response.status_code} {login_response.text}")
    
    if login_response.status_code == 200:
        print("✓ Login successful")
        auth_data = login_response.json()
        token = auth_data.get('access')
        headers = {"Authorization": f"Bearer {token}"}
        print(f"   Token: {token[:20]}...")
    else:
        print(f"✗ Login failed: {login_response.status_code}")
        print(login_response.text)
        return
    
    # Step 3: Create a chat
    print("\n3. Creating a new chat...")
    chat_data = {"name": "Test Chat for Enhanced Edit"}
    chat_response = requests.post(f"{BASE_URL}/chats/", json=chat_data, headers=headers)
    print(f"Chat creation response: {chat_response.status_code} {chat_response.text}")
    
    if chat_response.status_code == 201:
        print("✓ Chat created successfully")
        chat = chat_response.json()
        chat_id = chat['id']
        print(f"   Chat ID: {chat_id}")
    else:
        print(f"✗ Chat creation failed: {chat_response.status_code}")
        print(chat_response.text)
        return
    
    # Step 4: Add initial messages
    print("\n4. Adding initial messages...")
    print(f"Chat ID: {chat_id}")
    messages = [
        {"content": "Hello, this is the first message", "role": "user"},
        {"content": "This is the assistant's response", "role": "assistant"},
        {"content": "Let me ask a follow-up question", "role": "user"}
    ]
    message_ids = []
    for i, msg in enumerate(messages):
        print("\n------------------------------")
        print(f"Adding message {i+1} to chat {chat_id} at endpoint: {BASE_URL}/chats/{chat_id}/add_message/")
        print(f"Payload: {msg}")
        msg_response = requests.post(
            f"{BASE_URL}/chats/{chat_id}/add_message/", 
            json=msg, 
            headers=headers
        )
        print(f"Message {i+1} status: {msg_response.status_code}")
        print(f"Message {i+1} response: {msg_response.text}")
        if msg_response.status_code == 201:
            message_data = msg_response.json()
            # The add_message endpoint returns {user_message: {...}, ai_message: {...}}
            # We want to collect both message IDs
            if 'user_message' in message_data and 'id' in message_data['user_message']:
                message_ids.append(message_data['user_message']['id'])
                print(f"✓ User message added: {message_data['user_message']['content'][:30]}...")
            if 'ai_message' in message_data and 'id' in message_data['ai_message']:
                message_ids.append(message_data['ai_message']['id'])
                print(f"✓ AI message added: {message_data['ai_message']['content'][:30]}...")
        else:
            print(f"✗ Failed to add message {i+1}: {msg_response.status_code}")
            return
        print("------------------------------")
    
    # Step 5: Get current branch info
    print("\n5. Getting current branch info...")
    branch_response = requests.get(f"{BASE_URL}/chats/{chat_id}/branches/", headers=headers)
    if branch_response.status_code == 200:
        branches = branch_response.json()
        print(f"✓ Found {len(branches)} branches")
        for branch in branches:
            print(f"   Branch {branch['id']}: {branch['name']} (head: {branch['head_message_id']})")
    else:
        print(f"✗ Failed to get branches: {branch_response.status_code}")
        print(branch_response.text)
    
    # Step 6: Test enhanced edit (edit the second message)
    print("\n6. Testing enhanced edit...")
    message_to_edit = message_ids[1]  # Edit the assistant's response
    
    edit_data = {
        "original_message_id": message_to_edit,
        "new_content": "This is the EDITED assistant's response with new information"
    }
    
    edit_response = requests.post(
        f"{BASE_URL}/chats/{chat_id}/edit_with_branch/",
        json=edit_data,
        headers=headers
    )
    
    if edit_response.status_code == 201:
        print("✓ Enhanced edit successful!")
        edit_result = edit_response.json()
        
        print("\n=== EDIT DEBUG INFO ===")
        print(f"Original message ID: {edit_result.get('original_message_id')}")
        print(f"New message ID: {edit_result.get('new_message_id')}")
        print(f"New branch ID: {edit_result.get('new_branch_id')}")
        print(f"Edit record ID: {edit_result.get('edit_id')}")
        
        # Show original vs edited content
        if 'original_content' in edit_result and 'new_content' in edit_result:
            print(f"\nOriginal content: {edit_result['original_content']}")
            print(f"New content: {edit_result['new_content']}")
        
        # Show branch comparison if available
        if 'original_branch_messages' in edit_result and 'new_branch_messages' in edit_result:
            print(f"\nOriginal branch has {len(edit_result['original_branch_messages'])} messages")
            print(f"New branch has {len(edit_result['new_branch_messages'])} messages")
            
            print("\nOriginal branch messages:")
            for msg in edit_result['original_branch_messages']:
                print(f"  [{msg['role']}] {msg['content'][:50]}...")
            
            print("\nNew branch messages:")
            for msg in edit_result['new_branch_messages']:
                print(f"  [{msg['role']}] {msg['content'][:50]}...")
        
    else:
        print(f"✗ Enhanced edit failed: {edit_response.status_code}")
        print(edit_response.text)
        return
    
    # Step 7: Get updated branch info
    print("\n7. Getting updated branch info...")
    branch_response = requests.get(f"{BASE_URL}/chats/{chat_id}/branches/", headers=headers)
    
    if branch_response.status_code == 200:
        branches = branch_response.json()
        print(f"✓ Now have {len(branches)} branches")
        for branch in branches:
            print(f"   Branch {branch['id']}: {branch['name']} (head: {branch['head_message_id']})")
    else:
        print(f"✗ Failed to get updated branches: {branch_response.status_code}")
    
    # Step 8: Test switching between branches
    print("\n8. Testing branch switching...")
    branch_response = requests.get(f"{BASE_URL}/chats/{chat_id}/branches/", headers=headers)
    
    if branch_response.status_code == 200:
        branches = branch_response.json()
        if len(branches) >= 2:
            # Switch to the new branch
            new_branch = branches[-1]  # Assuming the new branch is the last one
            print(f"Switching to branch: {new_branch['name']}")
            
            # Get messages for this branch
            branch_messages_response = requests.get(
                f"{BASE_URL}/chats/{chat_id}/branches/{new_branch['id']}/messages/",
                headers=headers
            )
            
            if branch_messages_response.status_code == 200:
                branch_messages = branch_messages_response.json()
                print(f"✓ Branch {new_branch['name']} has {len(branch_messages)} messages:")
                for msg in branch_messages:
                    print(f"  [{msg['role']}] {msg['content'][:50]}...")
            else:
                print(f"✗ Failed to get branch messages: {branch_messages_response.status_code}")
    
    print("\n=== Test completed successfully! ===")

if __name__ == "__main__":
    test_api_only() 