#!/usr/bin/env python3
from django.contrib import admin
from .models import Message

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('message_id', 'sender', 'sent_at')
    search_fields = ('sender__username', 'message_body')
    list_filter = ('sent_at',)