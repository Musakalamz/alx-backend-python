#!/usr/bin/env python3
from django_filters import rest_framework as filters
from .models import Message

class MessageFilter(filters.FilterSet):
    sender = filters.UUIDFilter(field_name='sender__user_id')
    conversation = filters.UUIDFilter(field_name='conversation__conversation_id')
    participant = filters.UUIDFilter(method='filter_participant')
    sent_after = filters.DateTimeFilter(field_name='sent_at', lookup_expr='gte')
    sent_before = filters.DateTimeFilter(field_name='sent_at', lookup_expr='lte')
    message_body = filters.CharFilter(field_name='message_body', lookup_expr='icontains')

    def filter_participant(self, queryset, name, value):
        return queryset.filter(conversation__participants__user_id=value)

    class Meta:
        model = Message
        fields = ['sender', 'conversation', 'participant', 'sent_after', 'sent_before', 'message_body']