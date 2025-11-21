from datetime import datetime, timedelta
import os
from collections import deque, defaultdict
from django.conf import settings
from django.http import HttpResponseForbidden, JsonResponse
from django.utils import timezone

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.file_path = os.path.join(settings.BASE_DIR, 'requests.log')

    def __call__(self, request):
        user = getattr(request, 'user', None)
        if user and getattr(user, 'is_authenticated', False):
            user_repr = getattr(user, 'username', None) or getattr(user, 'email', 'authenticated')
        else:
            user_repr = 'anonymous'
        line = f"{datetime.now()} - User: {user_repr} - Path: {request.path}\n"
        with open(self.file_path, 'a', encoding='utf-8') as f:
            f.write(line)
        return self.get_response(request)

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        now = timezone.localtime()
        hour = now.hour
        if hour >= 21 or hour < 6:
            return HttpResponseForbidden('Access restricted between 9PM and 6AM')
        return self.get_response(request)

class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.window_seconds = 60
        self.limit = 5
        self.store = defaultdict(deque)

    def __call__(self, request):
        if request.method == 'POST' and '/messages' in request.path:
            now = timezone.now()
            ip = self._client_ip(request)
            dq = self.store[ip]
            cutoff = now - timedelta(seconds=self.window_seconds)
            while dq and dq[0] < cutoff:
                dq.popleft()
            if len(dq) >= self.limit:
                return JsonResponse({'detail': 'Rate limit exceeded: 5 messages per minute'}, status=429)
            dq.append(now)
        return self.get_response(request)

    def _client_ip(self, request):
        xff = request.META.get('HTTP_X_FORWARDED_FOR')
        if xff:
            return xff.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR') or 'unknown'

class RolepermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.write_methods = {'POST', 'PUT', 'PATCH', 'DELETE'}
        self.allowed_roles = {'admin', 'moderator'}

    def __call__(self, request):
        if request.method in self.write_methods:
            user = getattr(request, 'user', None)
            if not user or not getattr(user, 'is_authenticated', False):
                return HttpResponseForbidden('Forbidden')
            role = getattr(user, 'role', None)
            if role not in self.allowed_roles:
                return HttpResponseForbidden('Forbidden')
        return self.get_response(request)