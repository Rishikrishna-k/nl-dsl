# Backend API

## Test Coverage Summary

The automated tests in `api/tests.py` cover the following features:

### Project Operations
- Renaming a project (success, missing name, unauthorized)
- Deleting a chat from a project (success, missing chat_id, not found)
- Getting all chats in a project

### Chat Operations
- Renaming a chat (success, missing name, unauthorized)
- Getting all messages in a chat

### Message Operations
- Editing a user message (success, missing content, forbidden for AI messages)

### Separate Data Retrieval Endpoints
- Getting all projects for a user
- Getting all chats in a specific project (success, project not found)
- Getting all messages in a specific chat (success, chat not found)

### Dashboard View
- Retrieving dashboard data (success, unauthorized)

### Permissions
- Ensuring users cannot access or modify other users' projects, chats, or messages

### Health Check
- Health check endpoint returns status, database connection, and timestamp

Each test class in `api/tests.py` is organized by feature for easy maintenance. All tests are run automatically in Docker using Django's test runner. 