#!/usr/bin/env python3
from django.db import models


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


class UnreadMessagesManager(models.Manager):
    def unread_for_user(self, user):
        return self.get_queryset().filter(receiver=user, read=False).only("id", "content", "timestamp", "sender_id", "receiver_id", "parent_message_id").select_related("sender", "receiver")

