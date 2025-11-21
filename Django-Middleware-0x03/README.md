# Django Middleware — 0x03

A practical Django project focused on designing, integrating, and testing custom middleware in a messaging-style backend. This repository is a copy of the Messaging App backend scaffold and serves as the foundation for middleware-focused tasks: request/response logging, access control, IP blocking, payload validation, and clean middleware organization.

## Overview

- Target stack: Django, Django REST Framework (DRF), django-filter, optional JWT
- Base apps: `messaging_app` (project), `chats` (app)
- Goal: Implement production-ready middleware aligned with Django’s request/response lifecycle

## Objectives

- Understand middleware order and lifecycle in Django
- Create focused custom middleware (logging, permissions, rate limiting, validation)
- Intercept and modify requests/responses
- Configure `MIDDLEWARE` properly in `settings.py`
- Test behavior with Postman and Django’s test client

## Project Structure

```
Django-Middleware-0x03/
  manage.py
  messaging_app/
    settings.py
    urls.py
    wsgi.py
    asgi.py
  chats/
    models.py
    views.py
    serializers.py
    urls.py
```

Planned middleware location for clarity and modularity:

```
apps/core/middleware/
  request_logger.py
  auth_enforcer.py
  ip_blocklist.py
  json_validator.py
```

## Setup

- Python 3.11+
- Create and activate a virtualenv
- Install dependencies:

```bash
pip install django djangorestframework django-filter djangorestframework-simplejwt
```

- Initial migrations and run:

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

## Middleware Integration

- Declare custom middleware in `messaging_app/settings.py` under `MIDDLEWARE`
- Keep middleware small and single-responsibility
- Always call `get_response(request)` unless short-circuiting
- Use `request.user`, `request.path`, `request.method` for clean conditions
- Avoid DB-heavy operations; prefer caches and settings toggles

Example entry (to be added in later tasks):

```
MIDDLEWARE += [
  'apps.core.middleware.request_logger.RequestLoggerMiddleware',
  'apps.core.middleware.auth_enforcer.AuthEnforcerMiddleware',
]
```

## Testing

- Postman collections under `post_man-Collections`
- Django test client for unit tests of accept/reject/modify flows
- Verify:
  - Logs written for inbound/outbound traffic
  - Access control for authenticated/role-based users
  - Blocklisted IPs rejected early
  - Invalid JSON payloads rejected with clear errors

## Development Guidelines

- Follow PEP8 and Django conventions already present in the project
- Keep configuration via environment variables where applicable
- Document each middleware with a short header: purpose, inputs, outputs
- Order in `MIDDLEWARE` matters; place enforcement before logging if desired

## Git Workflow

- Commit after each task with clear messages, e.g.:

```bash
git add .
git commit -m "Task 0: project setup and middleware-focused README"
git push origin main
```

## License

Educational use for ALX Backend Python curriculum.
