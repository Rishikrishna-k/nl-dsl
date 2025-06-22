import sys
import os
sys.path.insert(0, '/app')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
import django
django.setup()

from django.contrib.auth.models import User
from api.models import UserProfile, Project, Chat, Message, Branch, Edit
import uuid
from datetime import datetime

# --- Create or get user ---
user, _ = User.objects.get_or_create(username='mockuser', defaults={
    'email': 'mockuser@example.com',
    'password': 'mockpass123'
})
profile, _ = UserProfile.objects.get_or_create(user=user, defaults={'display_name': 'Mock User'})

# --- Create or get project ---
project, _ = Project.objects.get_or_create(owner=user, name='Mock Project', defaults={'description': 'A project for mock data'})

# --- Create or get chat ---
chat, _ = Chat.objects.get_or_create(owner=user, name='Mock Chat', project=project, defaults={'description': 'A chat for mock data'})

# --- Create messages ---
msg1 = Message.objects.create(chat=chat, role=Message.Role.USER, content='Hello, this is the first message', status=Message.Status.SENT)
msg2 = Message.objects.create(chat=chat, role=Message.Role.ASSISTANT, content='Hi! This is the AI response.', status=Message.Status.SENT)
msg3 = Message.objects.create(chat=chat, role=Message.Role.USER, content='Let me edit my first message.', status=Message.Status.SENT)

# --- Create message graph ---
message_graph = {
    str(msg1.id): {"parent": None, "children": [str(msg2.id), str(msg3.id)]},
    str(msg2.id): {"parent": str(msg1.id), "children": []},
    str(msg3.id): {"parent": str(msg1.id), "children": []}
}
chat.message_graph = message_graph
chat.save()

# --- Create branch for original flow ---
branch1 = Branch.objects.create(chat=chat, head_message_id=msg2.id)
# --- Create branch for edited flow ---
branch2 = Branch.objects.create(chat=chat, head_message_id=msg3.id)

# --- Create edit event ---
edit = Edit.objects.create(
    chat=chat,
    branch=branch2,
    prev_message_id=msg1.id,
    new_message_id=msg3.id,
    new_head_id=msg3.id
)

print('--- MOCK DATA CREATED ---')
print(f'User: {user.username} (id={user.id})')
print(f'Project: {project.name} (id={project.id})')
print(f'Chat: {chat.name} (id={chat.id})')
print(f'Messages:')
for m in [msg1, msg2, msg3]:
    print(f'  {m.id}: {m.role} - {m.content}')
print(f'Branches:')
for b in [branch1, branch2]:
    print(f'  {b.branch_id}: head={b.head_message_id}')
print(f'Edit: {edit.edit_id} (prev={edit.prev_message_id}, new={edit.new_message_id}, branch={edit.branch.branch_id})')
print(f'Message Graph: {chat.message_graph}')

# --- Retrieve messages for each branch ---
def get_branch_messages(branch):
    graph = chat.message_graph or {}
    head_id = str(branch.head_message_id)
    message_ids = []
    current = head_id
    while current:
        message_ids.append(current)
        parent = graph.get(current, {}).get('parent')
        if parent:
            current = parent
        else:
            break
    message_ids.reverse()
    messages = Message.objects.filter(id__in=message_ids)
    messages = sorted(messages, key=lambda m: message_ids.index(str(m.id)))
    return messages

print('\n--- Branch 1 Messages (Original) ---')
for m in get_branch_messages(branch1):
    print(f'  {m.id}: {m.role} - {m.content}')

print('\n--- Branch 2 Messages (Edited) ---')
for m in get_branch_messages(branch2):
    print(f'  {m.id}: {m.role} - {m.content}') 