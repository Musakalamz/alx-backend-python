#!/usr/bin/env python3
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Message
from .serializers import MessageSerializer

class MessageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Message.objects.all().order_by('-created_at')
    serializer_class = MessageSerializer

@api_view(['GET'])
def ping(_request):
    return Response({'status': 'ok', 'service': 'messaging_app'})