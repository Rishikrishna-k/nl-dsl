from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import UserProfile, Project, Chat, Message
import uuid


class BaseTestCase(APITestCase):
    """
    Base test case with common setup for all API tests.
    Provides authenticated user and common test data.
    """
    
    def setUp(self):
        """Set up test data and authenticated client."""
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # Create user profile
        self.user_profile = UserProfile.objects.create(
            user=self.user,
            display_name='Test User',
            bio='Test bio'
        )
        
        # Create test project
        self.project = Project.objects.create(
            owner=self.user,
            name='Test Project',
            description='Test project description'
        )
        
        # Create test chat
        self.chat = Chat.objects.create(
            owner=self.user,
            name='Test Chat',
            description='Test chat description',
            project=self.project
        )
        
        # Create test messages
        self.user_message = Message.objects.create(
            chat=self.chat,
            role=Message.Role.USER,
            content='Hello, this is a user message',
            status=Message.Status.SENT
        )
        
        self.ai_message = Message.objects.create(
            chat=self.chat,
            role=Message.Role.ASSISTANT,
            content='Hello! This is an AI response.',
            status=Message.Status.SENT
        )
        
        # Set up authenticated client
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        
        # Create another user for permission tests
        self.other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='otherpass123'
        )
        self.other_user_profile = UserProfile.objects.create(
            user=self.other_user,
            display_name='Other User'
        )


class ProjectOperationsTests(BaseTestCase):
    """Test project operations: rename, delete chat in project."""
    
    def test_rename_project_success(self):
        """Test successfully renaming a project."""
        url = reverse('project-rename', kwargs={'pk': self.project.id})
        data = {'name': 'Renamed Project'}
        
        response = self.client.patch(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Renamed Project')
        
        # Verify database was updated
        self.project.refresh_from_db()
        self.assertEqual(self.project.name, 'Renamed Project')
    
    def test_rename_project_missing_name(self):
        """Test renaming project without providing name."""
        url = reverse('project-rename', kwargs={'pk': self.project.id})
        data = {}
        
        response = self.client.patch(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
    
    def test_rename_project_unauthorized(self):
        """Test renaming project owned by another user."""
        other_project = Project.objects.create(
            owner=self.other_user,
            name='Other Project'
        )
        url = reverse('project-rename', kwargs={'pk': other_project.id})
        data = {'name': 'Hacked Project'}
        
        response = self.client.patch(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_get_project_chats(self):
        """Test getting all chats in a project."""
        # Create another chat in the same project
        Chat.objects.create(
            owner=self.user,
            name='Another Chat',
            project=self.project
        )
        
        url = reverse('project-chats', kwargs={'pk': self.project.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Two chats in project
    
    def test_delete_chat_in_project_success(self):
        """Test successfully deleting a chat from a project."""
        url = reverse('project-delete-chat', kwargs={'pk': self.project.id})
        data = {'chat_id': self.chat.id}
        
        response = self.client.delete(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Verify chat was deleted
        self.assertFalse(Chat.objects.filter(id=self.chat.id).exists())
    
    def test_delete_chat_in_project_missing_chat_id(self):
        """Test deleting chat without providing chat_id."""
        url = reverse('project-delete-chat', kwargs={'pk': self.project.id})
        data = {}
        
        response = self.client.delete(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
    
    def test_delete_chat_in_project_not_found(self):
        """Test deleting a chat that doesn't exist in the project."""
        url = reverse('project-delete-chat', kwargs={'pk': self.project.id})
        data = {'chat_id': uuid.uuid4()}
        
        response = self.client.delete(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class ChatOperationsTests(BaseTestCase):
    """Test chat operations: rename, get messages."""
    
    def test_rename_chat_success(self):
        """Test successfully renaming a chat."""
        url = reverse('chat-rename', kwargs={'pk': self.chat.id})
        data = {'name': 'Renamed Chat'}
        
        response = self.client.patch(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Renamed Chat')
        
        # Verify database was updated
        self.chat.refresh_from_db()
        self.assertEqual(self.chat.name, 'Renamed Chat')
    
    def test_rename_chat_missing_name(self):
        """Test renaming chat without providing name."""
        url = reverse('chat-rename', kwargs={'pk': self.chat.id})
        data = {}
        
        response = self.client.patch(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
    
    def test_rename_chat_unauthorized(self):
        """Test renaming chat owned by another user."""
        other_chat = Chat.objects.create(
            owner=self.other_user,
            name='Other Chat'
        )
        url = reverse('chat-rename', kwargs={'pk': other_chat.id})
        data = {'name': 'Hacked Chat'}
        
        response = self.client.patch(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_get_chat_messages(self):
        """Test getting all messages in a chat."""
        url = reverse('chat-messages', kwargs={'pk': self.chat.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Two messages in chat
        
        # Verify message content
        message_contents = [msg['content'] for msg in response.data]
        self.assertIn('Hello, this is a user message', message_contents)
        self.assertIn('Hello! This is an AI response.', message_contents)


class MessageOperationsTests(BaseTestCase):
    """Test message operations: edit user message."""
    
    def test_edit_user_message_success(self):
        """Test successfully editing a user message."""
        url = reverse('message-edit-message', kwargs={'pk': self.user_message.id})
        data = {'content': 'This is my edited message'}
        
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['content'], 'This is my edited message')
        self.assertEqual(response.data['original_message'], self.user_message.id)
        self.assertEqual(response.data['status'], 'edited')
        
        # Verify original message still exists
        self.user_message.refresh_from_db()
        self.assertEqual(self.user_message.content, 'Hello, this is a user message')
        
        # Verify new edited message was created
        edited_message = Message.objects.get(id=response.data['id'])
        self.assertEqual(edited_message.original_message, self.user_message)
    
    def test_edit_ai_message_forbidden(self):
        """Test that AI messages cannot be edited."""
        url = reverse('message-edit-message', kwargs={'pk': self.ai_message.id})
        data = {'content': 'This should not work'}
        
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        self.assertIn('Only user messages can be edited', response.data['error'])
    
    def test_edit_message_missing_content(self):
        """Test editing message without providing content."""
        url = reverse('message-edit-message', kwargs={'pk': self.user_message.id})
        data = {}
        
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class SeparateDataRetrievalTests(BaseTestCase):
    """Test separate data retrieval endpoints."""
    
    def test_get_all_projects(self):
        """Test getting all projects for the user."""
        # Create another project
        Project.objects.create(
            owner=self.user,
            name='Another Project'
        )
        
        url = reverse('all-projects')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Two projects
        
        project_names = [project['name'] for project in response.data]
        self.assertIn('Test Project', project_names)
        self.assertIn('Another Project', project_names)
    
    def test_get_project_chats_endpoint(self):
        """Test getting all chats in a specific project."""
        # Create another chat in the same project
        Chat.objects.create(
            owner=self.user,
            name='Another Chat',
            project=self.project
        )
        
        url = reverse('project-chats', kwargs={'project_id': self.project.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Two chats in project
    
    def test_get_project_chats_project_not_found(self):
        """Test getting chats for a non-existent project."""
        url = reverse('project-chats', kwargs={'project_id': uuid.uuid4()})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('error', response.data)
    
    def test_get_chat_messages_endpoint(self):
        """Test getting all messages in a specific chat."""
        url = reverse('chat-messages', kwargs={'chat_id': self.chat.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Two messages in chat
    
    def test_get_chat_messages_chat_not_found(self):
        """Test getting messages for a non-existent chat."""
        url = reverse('chat-messages', kwargs={'chat_id': uuid.uuid4()})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('error', response.data)


class DashboardViewTests(BaseTestCase):
    """Test the dashboard view functionality."""
    
    def test_dashboard_view_success(self):
        """Test successful dashboard data retrieval."""
        url = reverse('dashboard')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check required fields
        self.assertIn('user', response.data)
        self.assertIn('profile', response.data)
        self.assertIn('projects', response.data)
        self.assertIn('standalone_chats', response.data)
        self.assertIn('total_projects', response.data)
        self.assertIn('total_chats', response.data)
        
        # Verify counts
        self.assertEqual(response.data['total_projects'], 1)
        self.assertEqual(response.data['total_chats'], 1)
    
    def test_dashboard_view_unauthorized(self):
        """Test dashboard access without authentication."""
        self.client.force_authenticate(user=None)
        url = reverse('dashboard')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PermissionTests(BaseTestCase):
    """Test permission and authorization scenarios."""
    
    def test_access_other_user_project(self):
        """Test that users cannot access other users' projects."""
        other_project = Project.objects.create(
            owner=self.other_user,
            name='Other Project'
        )
        
        url = reverse('project-detail', kwargs={'pk': other_project.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_access_other_user_chat(self):
        """Test that users cannot access other users' chats."""
        other_chat = Chat.objects.create(
            owner=self.other_user,
            name='Other Chat'
        )
        
        url = reverse('chat-detail', kwargs={'pk': other_chat.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_access_other_user_message(self):
        """Test that users cannot access other users' messages."""
        other_chat = Chat.objects.create(
            owner=self.other_user,
            name='Other Chat'
        )
        other_message = Message.objects.create(
            chat=other_chat,
            role=Message.Role.USER,
            content='Other user message'
        )
        
        url = reverse('message-detail', kwargs={'pk': other_message.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class HealthCheckTests(APITestCase):
    """Test health check endpoint."""
    
    def test_health_check_success(self):
        """Test successful health check."""
        url = reverse('health_check')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('status', response.data)
        self.assertIn('database', response.data)
        self.assertIn('timestamp', response.data)
        self.assertEqual(response.data['status'], 'healthy') 