# Django REST Framework Scalable API Core

A production-ready, highly scalable boilerplate and template for Django REST Framework (DRF) applications. This project demonstrates best practices in API architecture, JWT authentication, asynchronous task execution, caching, automated testing, containerization, and reverse-proxy deployment.

---

## 🌟 Key Features

- **Framework & API:** Django 5.2 & Django REST Framework (DRF).
- **Authentication & Authorization:** Secure JWT token management via `djangorestframework-simplejwt` and custom object-level permissions.
- **Asynchronous Tasks & Scheduling:** Celery integrated with Redis for handling background tasks and periodic scheduled jobs.
- **API Documentation:** Interactive Swagger UI and ReDoc OpenAPI documentation powered by `drf-yasg`.
- **Database & Caching:** PostgreSQL support for staging/production and Redis for caching/task queueing (`django-redis`).
- **Containerization & Deployment:**
  - Multi-stage Docker Compose setups (`docker-compose.yml`, `docker-compose-stage.yml`, `docker-compose-production.yml`).
  - Nginx pre-configured as a reverse proxy for static/media file serving and load handling.
  - Web server deployment ready with Gunicorn WSGI HTTP Server.
- **Development & Testing:**
  - `pytest` and `pytest-django` integration with `faker` for seed data.
  - `smtp4dev` integration for capturing and inspecting emails locally during development.
  - `locust` load-testing scripts pre-configured for API performance benchmarking.
  - Code formatting and standard compliance checks with `black` and `flake8`.

---

## 🏗️ Architecture & Service Layout
```text
.
├── core/                         # Main Django Project Root
│   ├── account/                  # User Management & Authentication App
│   ├── blog/                     # Blog & Content Management App
│   ├── core/                     # Project Settings & Configuration
│   ├── locust/                   # Locust Load Testing Scripts
│   └── manage.py                 # Django Management Utility
├── nginx/
│   └── default.conf              # Nginx Configuration File
├── docker-compose.yml            # Development Environment Setup
├── docker-compose-stage.yml      # Staging Setup
├── docker-compose-production.yml # Production Service Base
├── Dockerfile                    # Containerization Build File
├── pytest.ini                    # Pytest Settings
└── requirements.txt              # Project Dependencies
```
## 🚀 Quick Start Guide

### Prerequisites

- [Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/) installed on your machine.
- *Alternatively for local development:* Python 3.13+ and Redis installed locally.

---

### 🐳 Running with Docker (Recommended)

#### 1. Development Mode

The default Docker Compose environment runs the backend with auto-reloading enabled, Celery worker, Redis server, `smtp4dev` mail server, and Locust load testing UI.
> **Note:** Before running in Development Mode with SQLite, make sure to comment out the PostgreSQL database configuration and uncomment the SQLite configuration in `core/core/settings.py`.
```bash
# 1. Clone the repository
git clone [https://github.com/your-username/your-repo.name.git](https://github.com/your-username/your-repo.name.git)
cd your-repo-name

# 2. Setup your environment file
cp .env.example .env   # Configure your environment variables

# 3. Build and launch services
docker compose up --build
```

Access services at:
- Backend API: http://localhost:8000/

- Swagger Documentation: http://localhost:8000/swagger/

- smtp4dev Web UI: http://localhost:5000/

- Locust Performance Dashboard: http://localhost:8089/

#### 2. Staging / Production Simulation Mode
To test with PostgreSQL database, Gunicorn WSGI server, and Nginx reverse proxy serving static/media files:

```bash
docker compose -f docker-compose-stage.yml up --build
```
Access the Nginx-routed application at http://localhost/.

### 💻 Local Setup (Without Docker)
#### 1. Create and Activate Virtual Environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
#### 2. Install Dependencies:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```
#### 3. Apply Database Migrations:
```bash
python core/manage.py migrate
```
#### 4. Run the Development Server:
```bash
python core/manage.py runserver 0.0.0.0:8000
```
#### 5. Start Celery Worker (In a separate terminal):
```bash
cd core
celery -A core worker --loglevel=info
```

### 📑 API Endpoints Summary
Below is an overview of the primary REST endpoints available in the application:

| **Group** | **Endpoint**                           | **Description**    |
| --- |----------------------------------------|--------------------|
| `Auth` | `account/api/v1/registration/`         | 	Register a new user |
| `Auth` | `account/api/v1/token/login/`          | 	Obtain auth token  |
| `Auth` | `account/api/v1/token/logout/`         | Revoke auth token  |
| `Auth` | `account/api/v1/jwt/create/`           | 	Obtain JWT pair    |
| `Auth` | `account/api/v1/jwt/refresh/`          | 	Refresh JWT        |
| `Auth` | `account/api/v1/jwt/verify/`           | Verify JWT         |
| `Auth` | `account/api/v1/change-password/`      | 		Change password    |
| `Auth` | `account/api/v1/activation/confirm/<token>/` | Activate account via email link  |
| `Auth` | `account/api/v1/activation/resend/`    | 		Resend activation email    |
| `Profile` | `account/api/v1/profile/`              | 	Get / update profile        |
| `Blog` | `blog/api/v1/posts/`              | List / create posts         |
| `Blog` | `blog/api/v1/posts/<id>/`              | Retrieve / update / delete post         |
| `Blog` | `blog/api/v1/categories/`                    | List / create categories         |
| `Blog` | `blog/api/v1/categories/<id>/`                    | Retrieve / update / delete category         |
| `Docs` | `/swagger/`              | 	Swagger UI         |
| `Docs` | `/redoc/`                    | ReDoc UI         |
| `Docs` | `/swagger/output.json/`                    | OpenAPI schema         |

- Authentication schemes supported: Basic, Session, Token, JWT.

### 🧪 Testing & Code Quality
#### Running Unit Tests
Execute unit and integration tests using pytest:
```bash
# Run tests inside Docker container
docker compose exec backend pytest

# Or locally from project root
pytest core/
```
#### Code Formatting & Linting
Ensure code adheres to PEP 8 standards:
```bash
# Check code style with Flake8
flake8 core/

# Format code automatically using Black
black core/
```
#### Load & Stress Testing
Start the Locust service via docker-compose.yml and navigate to http://localhost:8089/.
Specify total users, spawn rate, and host http://backend:8000 to simulate traffic and analyze performance metrics under load.

### 🔧 Environment Variables Config (.env)
Create a .env file in the root directory based on the following template:
```text
# Django Settings
SECRET_KEY=your-custom-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,backend

# PostgreSQL Database Settings
POSTGRES_DB=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=db
POSTGRES_PORT=5432

# Redis & Celery Settings
CELERY_BROKER_URL=redis://redis:6379/0
REDIS_CACHE_URL=redis://redis:6379/1

# Email Settings
EMAIL_HOST=smtp4dev
EMAIL_PORT=25
```

### 📄 License
This project is open-source software licensed under the [MIT License](https://www.google.com/search?q=LICENSE).