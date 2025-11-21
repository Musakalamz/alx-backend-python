#!/usr/bin/env python3
from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import Conversation, Message

class IsParticipantOfConversation(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Conversation):
            return obj.participants.filter(pk=request.user.pk).exists()
        if isinstance(obj, Message):
            if obj.sender_id == request.user.pk:
                return True
            return obj.conversation.participants.filter(pk=request.user.pk).exists()
        return False