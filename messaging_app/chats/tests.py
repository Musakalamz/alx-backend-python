#!/usr/bin/env python3
from django.test import TestCase
from django.apps import apps

class ChatsAppTests(TestCase):
    def test_app_config_loaded(self):
        self.assertTrue(apps.is_installed('chats'))

    def test_message_model_exists(self):
        Message = apps.get_model('chats', 'Message')
        self.assertIsNotNone(Message)