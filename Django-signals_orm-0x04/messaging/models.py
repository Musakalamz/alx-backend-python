#!/usr/bin/env python3
from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_messages")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)
    parent_message = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="replies")
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message(from={self.sender}, to={self.receiver})"


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name="notifications")
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification(user={self.user}, message_id={self.message_id})"
class MessageHistory(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name="histories")
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)


class MessageQuerySet(models.QuerySet):
    def with_relations(self):
        return self.select_related("sender", "receiver", "parent_message").prefetch_related("replies")


class MessageManager(models.Manager):
    def get_queryset(self):
        return MessageQuerySet(self.model, using=self._db)

    def thread(self, root_id):
        nodes = {}
        order = []
        root = self.get_queryset().with_relations().filter(pk=root_id).first()
        if not root:
            return []
        stack = [root]
        while stack:
            node = stack.pop()
            nodes[node.pk] = {
                "id": node.pk,
                "sender_id": node.sender_id,
                "receiver_id": node.receiver_id,
                "content": node.content,
                "timestamp": node.timestamp,
                "edited": node.edited,
                "children": []
            }
            for child in list(node.replies.all()):
                stack.append(child)
                order.append((node.pk, child.pk))
        for parent_id, child_id in order:
            nodes[parent_id]["children"].append(nodes[child_id])
        return [nodes[root.pk]]


Message.add_to_class("objects", MessageManager())


class UnreadMessagesManager(models.Manager):
    def for_user(self, user):
        return self.get_queryset().filter(receiver=user, read=False).only("id", "content", "timestamp", "sender_id", "receiver_id", "parent_message_id")


Message.add_to_class("unread", UnreadMessagesManager())
