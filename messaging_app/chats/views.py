#!/usr/bin/env python3
from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .permissions import IsParticipantOfConversation
from django.shortcuts import get_object_or_404

from .models import User, Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all().order_by('-created_at')
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['participants__username', 'participants__email']
    ordering_fields = ['created_at']

    def get_queryset(self):
        return Conversation.objects.filter(participants=self.request.user).order_by('-created_at')

    def create(self, request, *args, **kwargs):
        participant_ids = request.data.get('participants', [])
        if not isinstance(participant_ids, list) or len(participant_ids) == 0:
            return Response({'detail': 'participants list is required'}, status=status.HTTP_400_BAD_REQUEST)
        if str(request.user.pk) not in [str(pid) for pid in participant_ids]:
            participant_ids.append(str(request.user.pk))
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
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['sender__username', 'message_body']
    ordering_fields = ['sent_at']

    def get_queryset(self):
        return Message.objects.select_related('sender', 'conversation').filter(conversation__participants=self.request.user).order_by('-sent_at')

    def create(self, request, *args, **kwargs):
        sender_id = request.data.get('sender')
        conversation_id = request.data.get('conversation')
        message_body = request.data.get('message_body')
        if not sender_id or not conversation_id or not message_body:
            return Response({'detail': 'sender, conversation, and message_body are required'}, status=status.HTTP_400_BAD_REQUEST)
        if str(sender_id) != str(request.user.pk):
            return Response({'detail': 'sender must be the authenticated user'}, status=status.HTTP_403_FORBIDDEN)
        conversation = get_object_or_404(Conversation, conversation_id=conversation_id)
        if not conversation.participants.filter(pk=request.user.pk).exists():
            return Response({'detail': 'user is not a participant of the conversation'}, status=status.HTTP_403_FORBIDDEN)
        msg = Message.objects.create(sender=request.user, conversation=conversation, message_body=message_body)
        serializer = self.get_serializer(msg)
        return Response(serializer.data, status=status.HTTP_201_CREATED)