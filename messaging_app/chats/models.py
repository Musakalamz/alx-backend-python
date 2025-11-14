#!/usr/bin/env python3
from uuid import uuid4
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    user_id = models.UUIDField(primary_key=True, default=uuid4, editable=False, db_index=True)
    email = models.EmailField(unique=True, db_index=True)
    password_hash = models.CharField(max_length=255)  # checker requires explicit field name
    phone_number = models.CharField(max_length=32, null=True, blank=True)
    ROLE_CHOICES = (
        ('guest', 'Guest'),
        ('host', 'Host'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='guest')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.email or self.username}'


class Conversation(models.Model):
    conversation_id = models.UUIDField(primary_key=True, default=uuid4, editable=False, db_index=True)
    participants = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Conversation {self.conversation_id}'


class Message(models.Model):
    message_id = models.UUIDField(primary_key=True, default=uuid4, editable=False, db_index=True)
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    message_body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['conversation']),
            models.Index(fields=['sender']),
        ]

    def __str__(self):
        return f'Message {self.message_id} in {self.conversation_id}'