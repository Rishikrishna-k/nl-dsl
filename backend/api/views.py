from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, viewsets
from rest_framework.decorators import api_view, action
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .models import UserProfile, Project, Chat, Message, UserSettings
from .serializers import (
    UserSerializer, UserProfileSerializer, ProjectSerializer, 
    ChatSerializer, MessageSerializer, ChatDetailSerializer,
    ProjectDetailSerializer, MessageDetailSerializer, UserSettingsSerializer,
    DashboardProjectSerializer, DashboardChatSerializer
)

# ---
# Custom Permission: Only allow owners to edit their own objects
# ---
class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    - SAFE_METHODS (GET, HEAD, OPTIONS) are always allowed.
    - For write operations (POST, PUT, PATCH, DELETE), only the owner can edit.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if hasattr(obj, 'owner'):
            return obj.owner == request.user
        elif hasattr(obj, 'user'):
            return obj.user == request.user
        elif hasattr(obj, 'chat') and hasattr(obj.chat, 'owner'):
            return obj.chat.owner == request.user
        return False

# ---
# User Profile ViewSet
# ---
class UserProfileViewSet(viewsets.ModelViewSet):
    """
    API endpoint for viewing and editing the current user's profile.
    - Each user has one profile (extra info: display name, avatar, bio, memory).
    - Only the user can view or edit their profile.
    """
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    
    def get_queryset(self):
        # Only allow users to see their own profile
        return UserProfile.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        # When creating, link the profile to the current user
        serializer.save(user=self.request.user)

# ---
# Project ViewSet
# ---
class ProjectViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing projects.
    - Projects group related chats together (like folders).
    - Each project belongs to a user.
    - Users can create, view, update, and delete their own projects.
    - Projects can have AI instructions for all chats inside.
    """
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    
    def get_queryset(self):
        # Only show projects owned by the current user
        return Project.objects.filter(owner=self.request.user)
    
    def get_serializer_class(self):
        # Use a detailed serializer for single project view, minimal for list
        if self.action == 'retrieve':
            return ProjectDetailSerializer
        elif self.action == 'list':
            return DashboardProjectSerializer
        return ProjectSerializer
    
    def perform_create(self, serializer):
        # Set the owner to the current user when creating
        serializer.save(owner=self.request.user)
    
    @action(detail=True, methods=['post'])
    def create_chat(self, request, pk=None):
        """
        Custom action to create a new chat inside a project.
        - POST to /api/projects/{project_id}/create_chat/
        - Only the project owner can add chats.
        """
        project = self.get_object()
        chat_data = {
            'name': request.data.get('name', 'New Chat'),
            'project': project.id,
            'description': request.data.get('description', ''),
            'ai_model': request.data.get('ai_model', ''),
        }
        serializer = ChatSerializer(data=chat_data, context={'request': request})
        if serializer.is_valid():
            serializer.save(owner=request.user, project=project)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['patch'])
    def rename(self, request, pk=None):
        """
        Custom action to rename a project.
        - PATCH to /api/projects/{project_id}/rename/
        - Only the project owner can rename.
        """
        project = self.get_object()
        new_name = request.data.get('name')
        if new_name:
            project.name = new_name
            project.save()
            serializer = self.get_serializer(project)
            return Response(serializer.data)
        return Response({'error': 'Name is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'])
    def chats(self, request, pk=None):
        """
        Custom action to get all chats in a project.
        - GET to /api/projects/{project_id}/chats/
        - Returns all chats belonging to this project.
        """
        project = self.get_object()
        chats = project.chats.all()
        serializer = ChatSerializer(chats, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['delete'])
    def delete_chat(self, request, pk=None):
        """
        Custom action to delete a specific chat in a project.
        - DELETE to /api/projects/{project_id}/delete_chat/
        - Requires chat_id in request data.
        - Only the project owner can delete chats in their project.
        """
        project = self.get_object()
        chat_id = request.data.get('chat_id')
        if chat_id:
            try:
                chat = project.chats.get(id=chat_id, owner=request.user)
                chat.delete()
                return Response({'message': 'Chat deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
            except Chat.DoesNotExist:
                return Response({'error': 'Chat not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'error': 'chat_id is required'}, status=status.HTTP_400_BAD_REQUEST)

# ---
# Chat ViewSet
# ---
class ChatViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing chats (conversations).
    - Each chat belongs to a user and (optionally) a project.
    - Users can create, view, update, and delete their own chats.
    - Each chat can have its own AI model and status (active, archived, deleted).
    - Messages are grouped under chats.
    """
    serializer_class = ChatSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    
    def get_queryset(self):
        # Only show chats owned by the current user
        return Chat.objects.filter(owner=self.request.user)
    
    def get_serializer_class(self):
        # Use a detailed serializer for single chat view, minimal for list
        if self.action == 'retrieve':
            return ChatDetailSerializer
        elif self.action == 'list':
            return DashboardChatSerializer
        return ChatSerializer
    
    def perform_create(self, serializer):
        # Set the owner to the current user when creating
        serializer.save(owner=self.request.user)
    
    @action(detail=True, methods=['post'])
    def add_message(self, request, pk=None):
        """
        Custom action to add a new message to a chat.
        - POST to /api/chats/{chat_id}/add_message/
        - Only the chat owner can add messages.
        """
        chat = self.get_object()
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(chat=chat)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        """
        Custom action to update the status of a chat (active, archived, deleted).
        - PATCH to /api/chats/{chat_id}/update_status/
        - Only the chat owner can update status.
        """
        chat = self.get_object()
        new_status = request.data.get('status')
        if new_status in [choice[0] for choice in Chat.Status.choices]:
            chat.status = new_status
            chat.save()
            serializer = self.get_serializer(chat)
            return Response(serializer.data)
        return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['patch'])
    def rename(self, request, pk=None):
        """
        Custom action to rename a chat.
        - PATCH to /api/chats/{chat_id}/rename/
        - Only the chat owner can rename.
        """
        chat = self.get_object()
        new_name = request.data.get('name')
        if new_name:
            chat.name = new_name
            chat.save()
            serializer = self.get_serializer(chat)
            return Response(serializer.data)
        return Response({'error': 'Name is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'])
    def messages(self, request, pk=None):
        """
        Custom action to get all messages in a chat.
        - GET to /api/chats/{chat_id}/messages/
        - Returns all messages belonging to this chat.
        """
        chat = self.get_object()
        messages = chat.messages.all()
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

# ---
# Message ViewSet
# ---
class MessageViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing messages inside chats.
    - Each message belongs to a chat.
    - Users can only access messages in their own chats.
    - Supports message editing: keeps the original and creates a new edited version.
    - Only user messages can be edited (not AI messages).
    """
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    
    def get_queryset(self):
        # Only show messages in chats owned by the current user
        return Message.objects.filter(chat__owner=self.request.user)
    
    def get_serializer_class(self):
        # Use a detailed serializer for single message view
        if self.action == 'retrieve':
            return MessageDetailSerializer
        return MessageSerializer
    
    def perform_create(self, serializer):
        serializer.save()
    
    @action(detail=True, methods=['post'])
    def edit_message(self, request, pk=None):
        """
        Custom action to create an edited version of a message.
        - POST to /api/messages/{message_id}/edit_message/
        - Only user messages can be edited (not AI messages).
        - Keeps the original message, creates a new one referencing the original.
        """
        original_message = self.get_object()
        
        # Check if the message is from a user (not AI)
        if original_message.role != Message.Role.USER:
            return Response(
                {'error': 'Only user messages can be edited'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        edited_data = {
            'chat': original_message.chat.id,
            'role': original_message.role,
            'content': request.data.get('content'),
            'original_message': original_message.id,
            'status': Message.Status.EDITED
        }
        serializer = MessageSerializer(data=edited_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ---
# User Settings ViewSet
# ---
class UserSettingsViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing user settings (future extensibility).
    - Each user can have a settings object (JSON field for modular settings).
    - Only the user can view or edit their settings.
    """
    serializer_class = UserSettingsSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    
    def get_queryset(self):
        return UserSettings.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# ---
# Dashboard View
# ---
class DashboardView(APIView):
    """
    API endpoint for dashboard summary data for the authenticated user.
    - Returns user info, profile, projects, and standalone chats (not in projects).
    - Used to quickly load the main dashboard in the frontend.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        user = request.user
        projects = Project.objects.filter(owner=user)
        chats = Chat.objects.filter(owner=user)
        projects_data = DashboardProjectSerializer(projects, many=True).data
        standalone_chats = chats.filter(project__isnull=True)
        standalone_chats_data = DashboardChatSerializer(standalone_chats, many=True).data
        profile, created = UserProfile.objects.get_or_create(user=user)
        profile_data = UserProfileSerializer(profile).data
        return Response({
            'user': UserSerializer(user).data,
            'profile': profile_data,
            'projects': projects_data,
            'standalone_chats': standalone_chats_data,
            'total_projects': projects.count(),
            'total_chats': chats.count(),
        })

# ---
# Additional API Views for Separate Data Retrieval
# ---
class AllProjectsView(APIView):
    """
    API endpoint to get all projects for the authenticated user.
    - GET to /api/all-projects/
    - Returns all projects with detailed information.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        projects = Project.objects.filter(owner=request.user)
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

class ProjectChatsView(APIView):
    """
    API endpoint to get all chats in a specific project.
    - GET to /api/project-chats/{project_id}/
    - Returns all chats belonging to the specified project.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, project_id):
        try:
            project = Project.objects.get(id=project_id, owner=request.user)
            chats = project.chats.all()
            serializer = ChatSerializer(chats, many=True)
            return Response(serializer.data)
        except Project.DoesNotExist:
            return Response({'error': 'Project not found'}, status=status.HTTP_404_NOT_FOUND)

class ChatMessagesView(APIView):
    """
    API endpoint to get all messages in a specific chat.
    - GET to /api/chat-messages/{chat_id}/
    - Returns all messages belonging to the specified chat.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, chat_id):
        try:
            chat = Chat.objects.get(id=chat_id, owner=request.user)
            messages = chat.messages.all()
            serializer = MessageSerializer(messages, many=True)
            return Response(serializer.data)
        except Chat.DoesNotExist:
            return Response({'error': 'Chat not found'}, status=status.HTTP_404_NOT_FOUND)

# ---
# Health Check View
# ---
class HealthCheckView(APIView):
    """
    API endpoint for health checks (used for monitoring and uptime checks).
    - Returns status and database connection info.
    """
    permission_classes = []
    
    def get(self, request):
        from django.db import connection
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
            db_status = "connected"
        except Exception:
            db_status = "disconnected"
        return Response({
            'status': 'healthy',
            'database': db_status,
            'timestamp': '2025-06-22T04:16:00Z'
        })

# ---
# User Registration View
# ---
class UserRegistrationView(APIView):
    """
    API endpoint for user registration.
    - Creates a new user account with username, email, and password.
    - Automatically creates a UserProfile for the new user.
    - Returns JWT tokens upon successful registration.
    - Includes comprehensive validation for username, email, and password.
    """
    permission_classes = []
    
    def post(self, request):
        """
        Register a new user with the provided credentials.
        - Validates username, email, and password.
        - Creates user and profile.
        - Returns JWT tokens for immediate login.
        """
        from django.contrib.auth.models import User
        from django.contrib.auth.password_validation import validate_password
        from django.core.exceptions import ValidationError
        from rest_framework_simplejwt.tokens import RefreshToken
        
        # Extract data from request
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        display_name = request.data.get('display_name', '')
        
        # Validate required fields
        if not username or not email or not password:
            return Response({
                'error': 'Username, email, and password are required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if username already exists
        if User.objects.filter(username=username).exists():
            return Response({
                'error': 'Username already exists'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if email already exists
        if User.objects.filter(email=email).exists():
            return Response({
                'error': 'Email already exists'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Validate password strength
        try:
            validate_password(password)
        except ValidationError as e:
            return Response({
                'error': 'Password validation failed',
                'details': list(e.messages)
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Validate email format
        from django.core.validators import validate_email
        try:
            validate_email(email)
        except ValidationError:
            return Response({
                'error': 'Invalid email format'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Validate username format (alphanumeric and underscore only)
        import re
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            return Response({
                'error': 'Username can only contain letters, numbers, and underscores'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Validate username length
        if len(username) < 3 or len(username) > 30:
            return Response({
                'error': 'Username must be between 3 and 30 characters'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Create the user
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            
            # Create user profile
            profile = UserProfile.objects.create(
                user=user,
                display_name=display_name or username
            )
            
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'message': 'User registered successfully',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'date_joined': user.date_joined
                },
                'profile': {
                    'id': profile.id,
                    'display_name': profile.display_name,
                    'bio': profile.bio,
                    'avatar_url': profile.avatar_url
                },
                'tokens': {
                    'access': str(refresh.access_token),
                    'refresh': str(refresh)
                }
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            # If anything goes wrong, clean up
            if user:
                user.delete()
            return Response({
                'error': 'Registration failed. Please try again.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# ---
# User Deletion View
# ---
class UserDeletionView(APIView):
    """
    API endpoint for user deletion.
    - Deletes a user account and all associated data.
    - Requires authentication and user can only delete their own account.
    - Cascades to delete all related data (projects, chats, messages, profiles).
    - Returns confirmation of deletion.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def delete(self, request):
        """
        Delete the authenticated user's account and all associated data.
        - Deletes user profile, projects, chats, messages, and settings.
        - Requires password confirmation for security.
        - Returns confirmation message.
        """
        from django.contrib.auth.models import User
        
        # Get password confirmation from request
        password = request.data.get('password')
        if not password:
            return Response({
                'error': 'Password confirmation is required for account deletion'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Verify password
        if not request.user.check_password(password):
            return Response({
                'error': 'Incorrect password'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = request.user
            username = user.username
            
            # Store user info for response
            user_info = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'date_joined': user.date_joined
            }
            
            # Delete user (this will cascade to related data due to CASCADE relationships)
            user.delete()
            
            return Response({
                'message': 'User account deleted successfully',
                'deleted_user': user_info,
                'note': 'All associated data (projects, chats, messages, profile) has been deleted'
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'error': 'Failed to delete user account. Please try again.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
