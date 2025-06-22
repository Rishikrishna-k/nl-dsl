from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, Project, Chat, Message, UserSettings

# Create your serializers here. 

class UserSerializer(serializers.ModelSerializer):
    """Basic user serializer for authentication and user info."""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined']
        read_only_fields = ['id', 'date_joined']

class UserProfileSerializer(serializers.ModelSerializer):
    """User profile serializer with nested user data."""
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'display_name', 'avatar_url', 'bio', 'user_memory', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class MessageSerializer(serializers.ModelSerializer):
    """Message serializer for individual messages."""
    class Meta:
        model = Message
        fields = ['id', 'chat', 'role', 'content', 'original_message', 'status', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class MessageDetailSerializer(serializers.ModelSerializer):
    """Detailed message serializer with edited versions."""
    edited_versions = MessageSerializer(many=True, read_only=True)
    
    class Meta:
        model = Message
        fields = ['id', 'chat', 'role', 'content', 'original_message', 'status', 'edited_versions', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class ChatSerializer(serializers.ModelSerializer):
    """Basic chat serializer for list views."""
    message_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Chat
        fields = ['id', 'owner', 'project', 'name', 'description', 'ai_model', 'status', 'message_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'owner', 'created_at', 'updated_at']
    
    def get_message_count(self, obj):
        return obj.messages.count()

class ChatDetailSerializer(serializers.ModelSerializer):
    """Detailed chat serializer with messages."""
    messages = MessageSerializer(many=True, read_only=True)
    message_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Chat
        fields = ['id', 'owner', 'project', 'name', 'description', 'ai_model', 'status', 'messages', 'message_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'owner', 'created_at', 'updated_at']
    
    def get_message_count(self, obj):
        return obj.messages.count()

class ProjectSerializer(serializers.ModelSerializer):
    """Basic project serializer for list views."""
    chat_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Project
        fields = ['id', 'owner', 'name', 'description', 'ai_instructions', 'chat_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'owner', 'created_at', 'updated_at']
    
    def get_chat_count(self, obj):
        return obj.chats.filter(status=Chat.Status.ACTIVE).count()

class ProjectDetailSerializer(serializers.ModelSerializer):
    """Detailed project serializer with chats."""
    chats = ChatSerializer(many=True, read_only=True)
    chat_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Project
        fields = ['id', 'owner', 'name', 'description', 'ai_instructions', 'chats', 'chat_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'owner', 'created_at', 'updated_at']
    
    def get_chat_count(self, obj):
        return obj.chats.filter(status=Chat.Status.ACTIVE).count()

class UserSettingsSerializer(serializers.ModelSerializer):
    """User settings serializer."""
    class Meta:
        model = UserSettings
        fields = ['id', 'user', 'settings', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

# Dashboard serializers for efficient data loading
class DashboardProjectSerializer(serializers.ModelSerializer):
    """Minimal project data for dashboard."""
    chat_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'chat_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_chat_count(self, obj):
        return obj.chats.filter(status=Chat.Status.ACTIVE).count()

class DashboardChatSerializer(serializers.ModelSerializer):
    """Minimal chat data for dashboard."""
    message_count = serializers.SerializerMethodField()
    project_name = serializers.CharField(source='project.name', read_only=True)
    
    class Meta:
        model = Chat
        fields = ['id', 'name', 'description', 'status', 'message_count', 'project_name', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_message_count(self, obj):
        return obj.messages.count() 