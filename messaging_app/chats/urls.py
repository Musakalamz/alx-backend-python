#!/usr/bin/env python3
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import MessageViewSet, ping

router = DefaultRouter()
router.register('messages', MessageViewSet, basename='message')

urlpatterns = [
    path('ping/', ping),
]
urlpatterns += router.urls