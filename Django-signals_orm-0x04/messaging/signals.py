#!/usr/bin/env python3
from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver

from .models import Message, Notification, MessageHistory
from django.contrib.auth import get_user_model


@receiver(post_save, sender=Message)
def create_notification_on_message(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(user=instance.receiver, message=instance)


@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    if instance.pk:
        try:
            prev = Message.objects.get(pk=instance.pk)
        except Message.DoesNotExist:
            return
        if prev.content != instance.content:
            MessageHistory.objects.create(message=prev, old_content=prev.content)
            instance.edited = True


@receiver(post_delete, sender=get_user_model())
def cleanup_user_related(sender, instance, **kwargs):
    try:
        Message.objects.filter(sender=instance).delete()
        Message.objects.filter(receiver=instance).delete()
        Notification.objects.filter(user=instance).delete()
        MessageHistory.objects.filter(message__sender=instance).delete()
        MessageHistory.objects.filter(message__receiver=instance).delete()
    except Exception:
        pass

