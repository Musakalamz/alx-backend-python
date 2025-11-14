#!/usr/bin/env python3
from django.contrib import admin
from .models import Message

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'created_at')
    search_fields = ('sender', 'content')
    list_filter = ('created_at',)