#!/usr/bin/env python3
from django.test import TestCase
from django.apps import apps
from django.contrib.auth import get_user_model


class MessagingAppTests(TestCase):
    def test_app_config_loaded(self):
        self.assertTrue(apps.is_installed("messaging"))

    def test_message_model_exists(self):
        Message = apps.get_model("messaging", "Message")
        self.assertIsNotNone(Message)


class MessageSignalTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.sender = User.objects.create_user(username="sender", email="sender@example.com", password="pass")
        self.receiver = User.objects.create_user(username="receiver", email="receiver@example.com", password="pass")

    def test_notification_created_on_message_post_save(self):
        Message = apps.get_model("messaging", "Message")
        Notification = apps.get_model("messaging", "Notification")

        msg = Message.objects.create(sender=self.sender, receiver=self.receiver, content="Hello!")

        self.assertEqual(Notification.objects.filter(user=self.receiver, message=msg).count(), 1)

