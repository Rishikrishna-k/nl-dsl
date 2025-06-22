#!/usr/bin/env python
import os
import sys
import django

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from api.models import Chat, Message, Branch
from django.contrib.auth.models import User

def create_test_data():
    # Create a test user if it doesn't exist
    user, created = User.objects.get_or_create(
        username='testuser',
        defaults={'email': 'test@example.com'}
    )
    if created:
        user.set_password('testpass123')
        user.save()
        print(f"Created test user: {user.username}")
    
    # Create a test chat
    chat, created = Chat.objects.get_or_create(
        name='Test Chat for Debug',
        owner=user
    )
    if created:
        print(f"Created test chat: {chat.name} (ID: {chat.id})")
    
    # Clear existing messages for this chat
    Message.objects.filter(chat=chat).delete()
    Branch.objects.filter(chat=chat).delete()
    
    # Create test messages
    messages = []
    
    # User message 1
    msg1 = Message.objects.create(
        chat=chat,
        content="Hello, can you help me with Python?",
        role="user"
    )
    messages.append(msg1)
    print(f"Created message 1: {msg1.content[:30]}... (ID: {msg1.id})")
    
    # Assistant response 1
    msg2 = Message.objects.create(
        chat=chat,
        content="Sure! I'd be happy to help you with Python. What specific question do you have?",
        role="assistant"
    )
    messages.append(msg2)
    print(f"Created message 2: {msg2.content[:30]}... (ID: {msg2.id})")
    
    # User message 2
    msg3 = Message.objects.create(
        chat=chat,
        content="How do I create a list comprehension?",
        role="user"
    )
    messages.append(msg3)
    print(f"Created message 3: {msg3.content[:30]}... (ID: {msg3.id})")
    
    # Assistant response 2
    msg4 = Message.objects.create(
        chat=chat,
        content="List comprehensions in Python are a concise way to create lists. The basic syntax is: [expression for item in iterable]. For example: [x**2 for x in range(5)] creates [0, 1, 4, 9, 16].",
        role="assistant"
    )
    messages.append(msg4)
    print(f"Created message 4: {msg4.content[:30]}... (ID: {msg4.id})")
    
    # Create message graph connections
    message_graph = {}
    for i in range(len(messages)):
        message_id = str(messages[i].id)
        if i == 0:
            # First message has no parent
            message_graph[message_id] = {"parent": None, "children": [str(messages[i+1].id)] if i+1 < len(messages) else []}
        elif i == len(messages) - 1:
            # Last message has no children
            message_graph[message_id] = {"parent": str(messages[i-1].id), "children": []}
        else:
            # Middle messages have both parent and children
            message_graph[message_id] = {"parent": str(messages[i-1].id), "children": [str(messages[i+1].id)]}
        print(f"Added to graph: {message_id} -> parent: {message_graph[message_id]['parent']}, children: {message_graph[message_id]['children']}")
    
    # Update the chat's message graph
    chat.message_graph = message_graph
    chat.save()
    print(f"Updated chat message graph with {len(message_graph)} nodes")
    
    # Create a branch pointing to the last message
    branch = Branch.objects.create(
        chat=chat,
        head_message_id=messages[-1].id
    )
    print(f"Created branch with head: {branch.head_message_id}")
    
    print(f"\nTest data created successfully!")
    print(f"Chat ID: {chat.id}")
    print(f"Total messages: {len(messages)}")
    print(f"Last message ID (should be head): {messages[-1].id}")
    print(f"Last message content: {messages[-1].content[:50]}...")
    print(f"Branch head message ID: {branch.head_message_id}")

if __name__ == '__main__':
    create_test_data() 