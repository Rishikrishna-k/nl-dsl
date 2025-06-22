from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    UserProfileViewSet, ProjectViewSet, ChatViewSet, MessageViewSet, 
    UserSettingsViewSet, DashboardView, HealthCheckView, AllProjectsView, ProjectChatsView, ChatMessagesView
)

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'profiles', UserProfileViewSet, basename='profile')
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'chats', ChatViewSet, basename='chat')
router.register(r'messages', MessageViewSet, basename='message')
router.register(r'settings', UserSettingsViewSet, basename='settings')

urlpatterns = [
    # Include the router URLs
    path('', include(router.urls)),
    
    # JWT Authentication endpoints
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Dashboard and utility endpoints
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('health/', HealthCheckView.as_view(), name='health_check'),
    
    # Additional separate data retrieval endpoints
    path('all-projects/', AllProjectsView.as_view(), name='all-projects'),
    path('project-chats/<uuid:project_id>/', ProjectChatsView.as_view(), name='project-chats'),
    path('chat-messages/<uuid:chat_id>/', ChatMessagesView.as_view(), name='chat-messages'),
] 