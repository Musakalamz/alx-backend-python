#!/usr/bin/env python3
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model


def delete_user(request, user_id):
    User = get_user_model()
    user = get_object_or_404(User, pk=user_id)
    user.delete()
    return JsonResponse({"status": "deleted", "user_id": user_id})

