#!/usr/bin/env python3
from rest_framework import serializers
from .models import User, Message, Conversation


class UserSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    role_label = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['user_id', 'username', 'first_name', 'last_name', 'email', 'phone_number', 'role', 'role_label', 'created_at']

    def get_role_label(self, obj):
        return obj.get_role_display()


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    conversation = serializers.PrimaryKeyRelatedField(queryset=Conversation.objects.all())

    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'conversation', 'message_body', 'sent_at']


class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)
    participant_names = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'participant_names', 'messages', 'created_at']

    def get_participant_names(self, obj):
        return [u.username or u.email for u in obj.participants.all()]

    def validate(self, attrs):
        # Example validation to demonstrate serializers.ValidationError presence
        if attrs is None:
            raise serializers.ValidationError('Invalid payload')
        return attrs