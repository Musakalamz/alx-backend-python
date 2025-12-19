# 📘 Messaging App — Backend API (Django & DRF)

### _Designed and documented with over 30 years of backend engineering experience_

---

## 🔰 Overview

The **Messaging App Backend** is a structured, scalable RESTful API built with **Django** and **Django REST Framework (DRF)**.  
It forms part of the **ProDev Backend: Milestone 2 — Building Robust APIs** curriculum and guides learners through building production-ready API services.

This project emphasizes:

- Enterprise-level system organization
- Robust database modeling
- Clean REST architecture
- Scalable project structure
- Professional documentation and workflow

---

## 🎯 Project Objectives

By the end of this project, learners will be able to:

- Scaffold Django projects using industry-standard structures
- Design scalable models using Django ORM
- Implement one-to-many, many-to-many, and one-to-one model relationships
- Create clean, modular Django apps
- Configure URL routing with `path()` and `include()`
- Follow Django’s best practices in code structure and documentation
- Build API layers using Django REST Framework
- Validate API functionality with Postman, Swagger, or CLI tools

---

## 📚 Learning Outcomes

Learners will:

- Understand Django’s project/app architecture
- Design relational schemas from feature requirements
- Use Django models and migrations effectively
- Build RESTful API endpoints
- Organize views, serializers, and URLs professionally
- Develop maintainable, modular applications
- Improve readability, scalability, and team collaboration

---

## 🏗️ Key Implementation Phases

### **1. Project Setup & Environment Configuration**

- Create virtual environment
- Install Django
- Scaffold project using `django-admin startproject messaging_app`
- Install and configure Django REST Framework
- Create `chats` app with `python manage.py startapp chats`
- Update `settings.py` (INSTALLED_APPS, middleware, DRF config)

---

### **2. Defining Data Models**

#### **User (Extended from AbstractUser)**

- `user_id` (UUID primary key)
- `first_name`, `last_name`
- `email` (unique)
- `password_hash`
- `phone_number`
- `role` (`guest`, `host`, `admin`)
- `created_at` timestamp

#### **Conversation**

- `conversation_id` (UUID primary key)
- `participants` (Many-to-Many → User)
- `created_at` timestamp

#### **Message**

- `message_id` (UUID primary key)
- `sender` (FK → User)
- `conversation` (FK → Conversation)
- `message_body`
- `sent_at` timestamp

#### Constraints & Indexes

- Primary keys indexed by default
- Unique email constraints
- Proper foreign key relationships
- Indexes on user email, conversation_id, message_id

**File:** `messaging_app/chats/models.py`

---

### **3. Serializers**

Create serializers for:

- **UserSerializer**
- **ConversationSerializer**
- **MessageSerializer**

Requirements:

- Properly handle nested relationships
- Allow conversation to include messages

**File:** `messaging_app/chats/serializers.py`

---

### **4. API Endpoints & Views**

Implement DRF ViewSets:

- **ConversationViewSet**

  - List conversations
  - Create conversations

- **MessageViewSet**
  - List messages
  - Send a message

**File:** `messaging_app/chats/views.py`

---

### **5. URL Routing**

Use DRF `DefaultRouter` to auto-generate routes:

- Register ConversationViewSet
- Register MessageViewSet
- Include API routes under `/api/`

Files:

- `messaging_app/chats/urls.py`
- `messaging_app/urls.py`

---

### **6. Running & Testing**

Run the full application:

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

---

## 🔧 CI/CD: Jenkins and GitHub Actions

### Jenkins Pipeline

- Pipeline file: `messaging_app/Jenkinsfile`
- Stages: checkout, install dependencies, run pytest, archive HTML report, build Docker image, push to Docker Hub.
- Start Jenkins:
  - `docker run -d --name jenkins -p 8080:8080 -p 50000:50000 -v jenkins_home:/var/jenkins_home jenkins/jenkins:lts`
- Configure plugins: Git, Pipeline, ShiningPanda.
- Set Docker Hub credentials in Jenkins with ID `dockerhub`.

### GitHub Actions

- Workflow file: `messaging_app/.github/workflows/ci.yml`
- Triggers: push and pull_request.
- Steps: checkout, setup Python 3.10, install dependencies, run flake8, run pytest with coverage, MySQL service for tests.

### Docker

- Dockerfile: `messaging_app/Dockerfile`
- Build: `docker build -t messaging-app:latest -f messaging_app/Dockerfile .`
- Run: `docker run -p 8000:8000 messaging-app:latest`

### Kubernetes (Optional)

- Manifest: `messaging_app/deployment.yaml`
- Apply: `kubectl apply -f messaging_app/deployment.yaml`

### Manual QA

- Trigger Jenkins “Build Now” and verify stages.
- Check GitHub Actions workflow results on pushes and PRs.
