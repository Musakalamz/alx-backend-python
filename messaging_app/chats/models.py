#!/usr/bin/env python3
from django.db import models

class Message(models.Model):
    sender = models.CharField(max_length=64)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sender}: {self.content[:20]}'