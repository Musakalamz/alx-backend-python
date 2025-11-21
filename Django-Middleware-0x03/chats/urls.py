#!/usr/bin/env python3
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from .views import ConversationViewSet, MessageViewSet

router = DefaultRouter()  # routers.DefaultRouter()
router.register('conversations', ConversationViewSet, basename='conversation')
router.register('messages', MessageViewSet, basename='message')

nested_router = routers.NestedDefaultRouter(router, 'conversations', lookup='conversation')  # NestedDefaultRouter
nested_router.register('messages', MessageViewSet, basename='conversation-messages')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(nested_router.urls)),
]