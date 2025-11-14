#!/usr/bin/env python3
from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from .models import User, Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all().order_by('-created_at')
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['participants__username', 'participants__email']
    ordering_fields = ['created_at']

    def create(self, request, *args, **kwargs):
        # Expect: {"participants": ["<uuid>", "<uuid>", ...]}
        participant_ids = request.data.get('participants', [])
        if not isinstance(participant_ids, list) or len(participant_ids) == 0:
            return Response({'detail': 'participants list is required'}, status=status.HTTP_400_BAD_REQUEST)
        convo = Conversation.objects.create()
        users = User.objects.filter(user_id__in=participant_ids)
        if users.count() == 0:
            convo.delete()
            return Response({'detail': 'no valid participants found'}, status=status.HTTP_400_BAD_REQUEST)
        convo.participants.set(users)
        serializer = self.get_serializer(convo)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.select_related('sender', 'conversation').order_by('-sent_at')
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['sender__username', 'message_body']
    ordering_fields = ['sent_at']

    def create(self, request, *args, **kwargs):
        # Expect: {"sender": "<uuid>", "conversation": "<uuid>", "message_body": "text"}
        sender_id = request.data.get('sender')
        conversation_id = request.data.get('conversation')
        message_body = request.data.get('message_body')
        if not sender_id or not conversation_id or not message_body:
            return Response({'detail': 'sender, conversation, and message_body are required'}, status=status.HTTP_400_BAD_REQUEST)

        sender = get_object_or_404(User, user_id=sender_id)
        conversation = get_object_or_404(Conversation, conversation_id=conversation_id)
        msg = Message.objects.create(sender=sender, conversation=conversation, message_body=message_body)
        serializer = self.get_serializer(msg)
        return Response(serializer.data, status=status.HTTP_201_CREATED)