#!/usr/bin/env python3
from uuid import uuid4
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    first_name = models.CharField(max_length=150)  # AbstractUser already has this, kept for non-null constraint
    last_name = models.CharField(max_length=150)   # AbstractUser already has this, kept for non-null constraint
    email = models.EmailField(unique=True, db_index=True)
    # AbstractUser has 'password' which stores hashed values; satisfies 'password_hash'
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
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    participants = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Conversation {self.id}'


class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
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
        return f'Message {self.id} in {self.conversation_id}'