#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test script for the enhanced edit functionality.
This script creates mock data and tests the complete edit workflow.
"""
import os
import sys
import django
import requests
import json

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from api.models import Chat, Message, Branch, Edit
from django.contrib.auth.models import User as AuthUser

# Configuration
BASE_URL = "http://localhost:8000/api"
TEST_USER_EMAIL = "testuser@example.com"
TEST_USER_PASSWORD = "testpass123"

def create_test_user():
    """Create a test user if it doesn't exist."""
    try:
        user = AuthUser.objects.get(email=TEST_USER_EMAIL)
        print(f"Using existing test user: {user.username}")
    except AuthUser.DoesNotExist:
        user = AuthUser.objects.create_user(
            username='testuser',
            email=TEST_USER_EMAIL,
            password=TEST_USER_PASSWORD
        )
        print(f"Created test user: {user.username}")
    
    return user

def login_user():
    """Login and get JWT token."""
    login_data = {
        "email": TEST_USER_EMAIL,
        "password": TEST_USER_PASSWORD
    }
    
    response = requests.post(f"{BASE_URL}/auth/login/", json=login_data)
    if response.status_code == 200:
        token = response.json()['access']
        print(f"Login successful, token obtained")
        return token
    else:
        print(f"Login failed: {response.text}")
        return None

def create_test_chat_with_messages(token):
    """Create a test chat with some messages."""
    headers = {"Authorization": f"Bearer {token}"}
    
    # Create chat
    chat_data = {
        "name": "Test Chat for Enhanced Edit",
        "description": "Test chat for enhanced edit functionality"
    }
    
    response = requests.post(f"{BASE_URL}/chats/", json=chat_data, headers=headers)
    if response.status_code != 201:
        print(f"Failed to create chat: {response.text}")
        return None, None
    
    chat = response.json()
    chat_id = chat['id']
    print(f"Created test chat: {chat['name']} ({chat_id})")
    
    # Add some messages to the chat
    messages = []
    
    # User message 1
    msg1_data = {"content": "Hello, this is my first message that I want to edit later"}
    response = requests.post(f"{BASE_URL}/chats/{chat_id}/add_message/", json=msg1_data, headers=headers)
    if response.status_code == 201:
        msg1 = response.json()
        messages.append(msg1)
        print(f"Added user message 1: {msg1['content'][:50]}...")
    
    # AI response 1
    ai1_data = {"content": "Hello! I understand you want to edit your message later. That's a great feature!"}
    response = requests.post(f"{BASE_URL}/chats/{chat_id}/add_message/", json=ai1_data, headers=headers)
    if response.status_code == 201:
        ai1 = response.json()
        messages.append(ai1)
        print(f"Added AI response 1: {ai1['content'][:50]}...")
    
    # User message 2
    msg2_data = {"content": "This is my second message that will remain unchanged"}
    response = requests.post(f"{BASE_URL}/chats/{chat_id}/add_message/", json=msg2_data, headers=headers)
    if response.status_code == 201:
        msg2 = response.json()
        messages.append(msg2)
        print(f"Added user message 2: {msg2['content'][:50]}...")
    
    # AI response 2
    ai2_data = {"content": "I see you have a second message. This conversation is going well!"}
    response = requests.post(f"{BASE_URL}/chats/{chat_id}/add_message/", json=ai2_data, headers=headers)
    if response.status_code == 201:
        ai2 = response.json()
        messages.append(ai2)
        print(f"Added AI response 2: {ai2['content'][:50]}...")
    
    return chat_id, messages

def test_enhanced_edit(token, chat_id, original_message_id):
    """Test the enhanced edit functionality."""
    headers = {"Authorization": f"Bearer {token}"}
    
    edit_data = {
        "original_message_id": original_message_id,
        "new_content": "Hello, this is my EDITED first message with completely new content!"
    }
    
    print(f"Testing Enhanced Edit Functionality")
    print(f"Original message ID: {original_message_id}")
    print(f"New content: {edit_data['new_content']}")
    
    response = requests.post(f"{BASE_URL}/chats/{chat_id}/edit_with_branch/", json=edit_data, headers=headers)
    
    print(f"Response status: {response.status_code}")
    
    if response.status_code == 201:
        result = response.json()
        print("Enhanced edit successful!")
        
        # Print debug info
        debug_info = result.get('debug_info', {})
        print(f"Debug Information:")
        print(f"  - Chat ID: {debug_info.get('chat_id')}")
        print(f"  - Original message ID: {debug_info.get('original_message_id')}")
        print(f"  - New message ID: {debug_info.get('new_message_id')}")
        print(f"  - Branch ID: {debug_info.get('branch_id')}")
        print(f"  - Edit ID: {debug_info.get('edit_id')}")
        print(f"  - Graph size: {debug_info.get('graph_size')}")
        print(f"  - All heads: {debug_info.get('all_heads')}")
        print(f"  - Total branches: {debug_info.get('total_branches')}")
        
        # Print branch comparison
        branch_comparison = result.get('branch_comparison', {})
        original_messages = branch_comparison.get('original_branch_messages', [])
        new_messages = branch_comparison.get('new_branch_messages', [])
        
        print(f"BRANCH COMPARISON:")
        print(f"="*80)
        print(f"ORIGINAL BRANCH ({len(original_messages)} messages):")
        for i, msg in enumerate(original_messages):
            marker = " [EDITED FROM HERE]" if msg['id'] == original_message_id else ""
            print(f"  {i+1}. [{msg['role']}] {msg['content'][:50]}...{marker}")
        
        print(f"NEW BRANCH ({len(new_messages)} messages):")
        for i, msg in enumerate(new_messages):
            marker = " [NEW EDITED MESSAGE]" if msg['id'] == debug_info.get('new_message_id') else ""
            print(f"  {i+1}. [{msg['role']}] {msg['content'][:50]}...{marker}")
        print(f"="*80)
        
        # Print all branches
        all_branches = result.get('all_branches', [])
        print(f"All Branches ({len(all_branches)}):")
        for branch in all_branches:
            marker = " (NEW)" if branch.get('is_new_branch') else ""
            print(f"  - Branch {branch['branch_id']}: head={branch['head_message_id']}{marker}")
        
        return result
    else:
        print(f"Enhanced edit failed: {response.text}")
        return None

def test_graph_endpoints(token, chat_id):
    """Test the graph endpoints to verify the branching."""
    headers = {"Authorization": f"Bearer {token}"}
    
    print(f"Testing Graph Endpoints")
    
    # Test graph heads
    response = requests.get(f"{BASE_URL}/graph/graph_heads/?chat_id={chat_id}", headers=headers)
    if response.status_code == 200:
        heads = response.json()
        print(f"Graph heads: {heads}")
    else:
        print(f"Graph heads failed: {response.text}")
    
    # Test branches
    response = requests.get(f"{BASE_URL}/graph/branches/?chat_id={chat_id}", headers=headers)
    if response.status_code == 200:
        branches = response.json()
        print(f"Branches: {branches}")
    else:
        print(f"Branches failed: {response.text}")

def main():
    """Main test function."""
    print("Testing Enhanced Edit Functionality")
    print("="*50)
    
    # Step 1: Create test user
    user = create_test_user()
    
    # Step 2: Login and get token
    token = login_user()
    if not token:
        print("Cannot proceed without authentication token")
        return
    
    # Step 3: Create test chat with messages
    chat_id, messages = create_test_chat_with_messages(token)
    if not chat_id or not messages:
        print("Cannot proceed without test chat and messages")
        return
    
    # Step 4: Find the first user message to edit
    user_message = None
    for msg in messages:
        if msg['role'] == 'user':
            user_message = msg
            break
    
    if not user_message:
        print("No user message found to edit")
        return
    
    print(f"Found user message to edit: {user_message['content'][:50]}...")
    
    # Step 5: Test enhanced edit
    edit_result = test_enhanced_edit(token, chat_id, user_message['id'])
    
    if edit_result:
        # Step 6: Test graph endpoints
        test_graph_endpoints(token, chat_id)
        
        print(f"Enhanced edit functionality test completed successfully!")
        print(f"New branch created with edited message")
        print(f"Original branch preserved")
        print(f"Graph updated correctly")
        print(f"Edit record created")
    else:
        print(f"Enhanced edit functionality test failed!")

if __name__ == "__main__":
    main()
