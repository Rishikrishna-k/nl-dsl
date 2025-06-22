#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import time

# API base URL
BASE_URL = "http://localhost:8000/api"

def test_enhanced_edit_workflow():
    """Test the enhanced edit workflow with comprehensive debugging and branch comparison"""
    
    print("=== Testing Enhanced Edit Workflow (Comprehensive) ===")
    
    # Test user credentials
    test_user = {
        "username": "testuser_enhanced",
        "email": "testuser_enhanced@example.com",
        "password": "testpass123"
    }
    
    # Step 1: Register user
    print("\n1. Registering test user...")
    register_response = requests.post(f"{BASE_URL}/auth/register/", json=test_user)
    print(f"Register response: {register_response.status_code}")
    
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
    print(f"Login response: {login_response.status_code}")
    
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
    chat_data = {"name": "Test Chat for Enhanced Edit Workflow"}
    chat_response = requests.post(f"{BASE_URL}/chats/", json=chat_data, headers=headers)
    print(f"Chat creation response: {chat_response.status_code}")
    
    if chat_response.status_code == 201:
        print("✓ Chat created successfully")
        chat = chat_response.json()
        chat_id = chat['id']
        print(f"   Chat ID: {chat_id}")
    else:
        print(f"✗ Chat creation failed: {chat_response.status_code}")
        print(chat_response.text)
        return
    
    # Step 4: Add initial messages to create a conversation
    print("\n4. Adding initial messages...")
    messages = [
        {"content": "Hello, I want to learn about Python programming", "role": "user"},
        {"content": "Great! Python is a versatile programming language. What specific aspect would you like to explore?", "role": "assistant"},
        {"content": "I want to learn about web development with Django", "role": "user"}
    ]
    message_ids = []
    
    for i, msg in enumerate(messages):
        print(f"\n--- Adding message {i+1} ---")
        print(f"Content: {msg['content'][:50]}...")
        
        msg_response = requests.post(
            f"{BASE_URL}/chats/{chat_id}/add_message/", 
            json=msg, 
            headers=headers
        )
        
        if msg_response.status_code == 201:
            message_data = msg_response.json()
            if 'user_message' in message_data and 'id' in message_data['user_message']:
                message_ids.append(message_data['user_message']['id'])
                print(f"✓ User message added: {message_data['user_message']['content'][:30]}...")
            if 'ai_message' in message_data and 'id' in message_data['ai_message']:
                message_ids.append(message_data['ai_message']['id'])
                print(f"✓ AI message added: {message_data['ai_message']['content'][:30]}...")
        else:
            print(f"✗ Failed to add message {i+1}: {msg_response.status_code}")
            return
    
    print(f"\n✓ All messages added. Message IDs: {message_ids}")
    
    # Step 5: Get initial branch info
    print("\n5. Getting initial branch info...")
    branch_response = requests.get(f"{BASE_URL}/chats/{chat_id}/branches/", headers=headers)
    if branch_response.status_code == 200:
        branches = branch_response.json()
        print(f"✓ Found {len(branches)} initial branches")
        for branch in branches:
            print(f"   Branch {branch['id']}: head={branch['head_message_id']}")
    else:
        print(f"✗ Failed to get initial branches: {branch_response.status_code}")
    
    # Step 6: Test enhanced edit workflow
    print("\n6. Testing enhanced edit workflow...")
    message_to_edit = message_ids[0]  # Edit the first user message
    
    edit_data = {
        "chat_id": chat_id,
        "original_message_id": message_to_edit,
        "new_content": "Hello, I want to learn about Python programming and machine learning"
    }
    
    print(f"Editing message: {message_to_edit}")
    print(f"New content: {edit_data['new_content']}")
    
    edit_response = requests.post(
        f"{BASE_URL}/edit/enhanced_edit_with_branch/",
        json=edit_data,
        headers=headers
    )
    
    if edit_response.status_code == 201:
        print("✓ Enhanced edit workflow successful!")
        edit_result = edit_response.json()
        
        # Display comprehensive debug information
        print("\n" + "="*80)
        print("ENHANCED EDIT WORKFLOW RESULTS")
        print("="*80)
        
        # Debug info
        debug_info = edit_result.get('debug_info', {})
        print(f"\n📊 DEBUG INFO:")
        print(f"   Chat ID: {debug_info.get('chat_id')}")
        print(f"   Original message ID: {debug_info.get('original_message_id')}")
        print(f"   New message ID: {debug_info.get('new_message_id')}")
        print(f"   New branch ID: {debug_info.get('new_branch_id')}")
        print(f"   Edit ID: {debug_info.get('edit_id')}")
        print(f"   Graph size: {debug_info.get('graph_size')}")
        print(f"   Total branches: {debug_info.get('total_branches')}")
        
        # Steps completed
        steps = debug_info.get('steps_completed', [])
        print(f"\n✅ STEPS COMPLETED ({len(steps)}):")
        for i, step in enumerate(steps, 1):
            print(f"   {i}. {step}")
        
        # New branch info
        new_branch = edit_result.get('new_branch', {})
        print(f"\n🌿 NEW BRANCH:")
        print(f"   Branch ID: {new_branch.get('branch_id')}")
        print(f"   Head message ID: {new_branch.get('head_message_id')}")
        
        # New message info
        new_message = edit_result.get('new_message', {})
        print(f"\n💬 NEW MESSAGE:")
        print(f"   Message ID: {new_message.get('id')}")
        print(f"   Content: {new_message.get('content')}")
        print(f"   Role: {new_message.get('role')}")
        print(f"   Status: {new_message.get('status')}")
        print(f"   Original message ID: {new_message.get('original_message_id')}")
        
        # Edit record
        edit_record = edit_result.get('edit_record', {})
        print(f"\n📝 EDIT RECORD:")
        print(f"   Edit ID: {edit_record.get('edit_id')}")
        print(f"   Previous message ID: {edit_record.get('prev_message_id')}")
        print(f"   New message ID: {edit_record.get('new_message_id')}")
        print(f"   New head ID: {edit_record.get('new_head_id')}")
        
        # Branch comparison
        branch_comparison = edit_result.get('branch_comparison', {})
        print(f"\n🔄 BRANCH COMPARISON:")
        
        original_branch = branch_comparison.get('original_branch', {})
        print(f"\n   📍 ORIGINAL BRANCH:")
        print(f"      Head message ID: {original_branch.get('head_message_id')}")
        print(f"      Message count: {original_branch.get('message_count')}")
        print(f"      Messages:")
        for i, msg in enumerate(original_branch.get('messages', []), 1):
            print(f"        {i}. [{msg['role']}] {msg['content'][:50]}...")
        
        new_branch_info = branch_comparison.get('new_branch', {})
        print(f"\n   🌱 NEW BRANCH:")
        print(f"      Head message ID: {new_branch_info.get('head_message_id')}")
        print(f"      Message count: {new_branch_info.get('message_count')}")
        print(f"      Messages:")
        for i, msg in enumerate(new_branch_info.get('messages', []), 1):
            print(f"        {i}. [{msg['role']}] {msg['content'][:50]}...")
        
        # Differences
        differences = branch_comparison.get('differences', {})
        print(f"\n   🔍 DIFFERENCES:")
        print(f"      Changed message ID: {differences.get('changed_message_id')}")
        print(f"      Original content: {differences.get('original_content')}")
        print(f"      New content: {differences.get('new_content')}")
        
        # All branches
        all_branches = edit_result.get('all_branches', [])
        print(f"\n🌳 ALL BRANCHES ({len(all_branches)}):")
        for branch in all_branches:
            marker = " (NEW)" if branch.get('is_new_branch') else ""
            print(f"   Branch {branch['branch_id']}: head={branch['head_message_id']}{marker}")
        
        # Graph info
        updated_graph = edit_result.get('updated_graph', {})
        print(f"\n🗺️  UPDATED GRAPH:")
        print(f"   Total nodes: {len(updated_graph)}")
        print(f"   Graph structure:")
        for node_id, node_data in updated_graph.items():
            parent = node_data.get('parent', 'None')
            children = node_data.get('children', [])
            print(f"     {node_id} -> parent: {parent}, children: {children}")
        
        print("\n" + "="*80)
        print("✅ ENHANCED EDIT WORKFLOW TEST COMPLETED SUCCESSFULLY!")
        print("="*80)
        
    else:
        print(f"✗ Enhanced edit workflow failed: {edit_response.status_code}")
        print(edit_response.text)
        return
    
    # Step 7: Verify the edit by fetching branch messages
    print("\n7. Verifying edit by fetching branch messages...")
    
    # Get all branches again
    branch_response = requests.get(f"{BASE_URL}/chats/{chat_id}/branches/", headers=headers)
    if branch_response.status_code == 200:
        branches = branch_response.json()
        print(f"✓ Now have {len(branches)} branches")
        
        # Test fetching messages for each branch
        for branch in branches:
            print(f"\n--- Testing branch {branch['id']} ---")
            
            # Get messages for this branch
            branch_messages_response = requests.get(
                f"{BASE_URL}/edit/get_branch_messages/?chat_id={chat_id}&head_id={branch['head_message_id']}",
                headers=headers
            )
            
            if branch_messages_response.status_code == 200:
                branch_data = branch_messages_response.json()
                messages = branch_data.get('messages', [])
                print(f"✓ Branch {branch['id']} has {len(messages)} messages:")
                for i, msg in enumerate(messages, 1):
                    print(f"  {i}. [{msg['role']}] {msg['content'][:50]}...")
            else:
                print(f"✗ Failed to get messages for branch {branch['id']}: {branch_messages_response.status_code}")
    
    print("\n=== Enhanced Edit Workflow Test Completed Successfully! ===")

if __name__ == "__main__":
    test_enhanced_edit_workflow() 