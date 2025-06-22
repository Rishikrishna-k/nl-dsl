from django.contrib import admin
from .models import UserProfile, Project, Chat, Message, UserSettings

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'display_name', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'display_name', 'bio')
    readonly_fields = ('id', 'created_at', 'updated_at')

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('name', 'description', 'owner__username')
    readonly_fields = ('id', 'created_at', 'updated_at')

@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'project', 'status', 'created_at')
    list_filter = ('status', 'created_at', 'project')
    search_fields = ('name', 'description', 'owner__username', 'project__name')
    readonly_fields = ('id', 'created_at', 'updated_at')

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('role', 'chat', 'status', 'created_at')
    list_filter = ('role', 'status', 'created_at')
    search_fields = ('content', 'chat__name')
    readonly_fields = ('id', 'created_at', 'updated_at')

@admin.register(UserSettings)
class UserSettingsAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'updated_at')
    search_fields = ('user__username',)
    readonly_fields = ('id', 'created_at', 'updated_at')
