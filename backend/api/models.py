import uuid
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class UserProfile(models.Model):
    """
    Extended user profile with additional fields for the chat application.
    Uses UUID for all operations and includes user memory for AI preferences.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    display_name = models.CharField(max_length=255, blank=True)
    avatar_url = models.URLField(max_length=500, blank=True)
    bio = models.TextField(blank=True)
    user_memory = models.TextField(blank=True, help_text="User preferences for AI responses")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_profiles'
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"{self.user.username} Profile ({self.id})"

class Project(models.Model):
    """
    Projects that group related chats together.
    Each project belongs to a user and contains multiple chats.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    ai_instructions = models.TextField(blank=True, help_text="Project-level instructions for AI")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'projects'
        indexes = [
            models.Index(fields=['owner']),
            models.Index(fields=['created_at']),
            models.Index(fields=['updated_at']),
        ]
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.name} ({self.id})"

class Chat(models.Model):
    """
    Chat conversations within projects or standalone.
    Each chat belongs to a user and optionally to a project.
    """
    class Status(models.TextChoices):
        ACTIVE = 'active', 'Active'
        ARCHIVED = 'archived', 'Archived'
        DELETED = 'deleted', 'Deleted'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chats')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='chats', null=True, blank=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    ai_model = models.CharField(max_length=100, blank=True, help_text="AI model to use for this chat")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'chats'
        indexes = [
            models.Index(fields=['owner']),
            models.Index(fields=['project']),
            models.Index(fields=['status']),
            models.Index(fields=['created_at']),
            models.Index(fields=['updated_at']),
        ]
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.name} ({self.id})"

class Message(models.Model):
    """
    Individual messages within chats.
    Supports message editing by keeping original and creating new edited versions.
    """
    class Role(models.TextChoices):
        USER = 'user', 'User'
        ASSISTANT = 'assistant', 'Assistant'
        SYSTEM = 'system', 'System'

    class Status(models.TextChoices):
        SENT = 'sent', 'Sent'
        DELIVERED = 'delivered', 'Delivered'
        FAILED = 'failed', 'Failed'
        EDITED = 'edited', 'Edited'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.USER)
    content = models.TextField()
    original_message = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, 
                                       related_name='edited_versions', help_text="Reference to original message if this is an edit")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.SENT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'messages'
        indexes = [
            models.Index(fields=['chat']),
            models.Index(fields=['role']),
            models.Index(fields=['status']),
            models.Index(fields=['created_at']),
            models.Index(fields=['original_message']),
        ]
        ordering = ['created_at']

    def __str__(self):
        return f"{self.role} message in {self.chat.name} ({self.id})"

class UserSettings(models.Model):
    """
    User settings for future extensibility.
    Uses JSON field for modular settings that can be easily extended.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='settings')
    settings = models.JSONField(default=dict, help_text="Modular user settings")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_settings'
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['updated_at']),
        ]

    def __str__(self):
        return f"Settings for {self.user.username} ({self.id})"
