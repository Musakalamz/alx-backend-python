#!/usr/bin/env python3
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

from .models import Message


@cache_page(60)
def list_messages(request):
    qs = Message.objects.filter(receiver=request.user).only("id", "content", "timestamp", "sender_id", "receiver_id", "parent_message_id").select_related("sender", "receiver")
    data = [
        {
            "id": m.id,
            "content": m.content,
            "timestamp": m.timestamp,
            "sender_id": m.sender_id,
            "receiver_id": m.receiver_id,
        }
        for m in qs
    ]
    return JsonResponse({"messages": data})


def unread_inbox(request):
    qs = Message.unread.unread_for_user(request.user)
    data = [
        {
            "id": m.id,
            "content": m.content,
            "timestamp": m.timestamp,
            "sender_id": m.sender_id,
            "receiver_id": m.receiver_id,
        }
        for m in qs
    ]
    return JsonResponse({"unread": data})


def send_message(request):
    User = get_user_model()
    receiver_id = request.POST.get("receiver")
    content = request.POST.get("content")
    receiver = get_object_or_404(User, pk=receiver_id)
    msg = Message.objects.create(sender=request.user, receiver=receiver, content=content)
    return JsonResponse({"id": msg.id})


def edit_message(request, message_id):
    msg = get_object_or_404(Message, pk=message_id)
    new_content = request.POST.get("content")
    msg.content = new_content
    msg.edited_by = request.user
    msg.save()
    history = [
        {"old_content": h.old_content, "edited_at": h.edited_at}
        for h in msg.histories.all()
    ]
    return JsonResponse({"id": msg.id, "edited": msg.edited, "history": history})


def threaded_view(request, root_id):
    root = Message.objects.filter(pk=root_id).select_related("sender", "receiver", "parent_message").first()
    if not root:
        return JsonResponse({"thread": []})

    def build(node):
        children = list(node.replies.all().select_related("sender", "receiver"))
        return {
            "id": node.id,
            "content": node.content,
            "sender_id": node.sender_id,
            "receiver_id": node.receiver_id,
            "timestamp": node.timestamp,
            "children": [build(c) for c in children],
        }

    return JsonResponse({"thread": build(root)})


def delete_user(request, user_id):
    User = get_user_model()
    user = get_object_or_404(User, pk=user_id)
    user.delete()
    return JsonResponse({"status": "deleted", "user_id": user_id})
