
# Pinsphere Backend

---

## Table of Contents
- [Pinsphere Backend](#pinsphere-backend)
  - [Table of Contents](#table-of-contents)
  - [Aim](#aim)
  - [Features](#features)
  - [Usage](#usage)
  - [Infrastructure](#infrastructure)
  - [Architecture](#architecture)
  - [Installation](#installation)
  - [Structure](#structure)
  - [License](#license)
    - [Points Covered:](#points-covered)

---

## Aim

The primary goal of Pinsphere is to create a seamless and intuitive environment for users to interact with a digital collection of media. The platform enables users to upload, categorize, and share pins (images, videos, and media) within a scalable and secure ecosystem. Whether for personal use or collaborative teams, Pinsphere streamlines the way media is managed and shared.

---

## Features

- **Pin Storage:** Store various types of media like images, GIFs, and videos in a secure and organized environment.
- **Tagging & Categorization:** Classify and categorize your pins using tags for easy searching and browsing.
- **User Management:** Manage users and permissions to control who can upload, view, or modify pins.
- **Search Functionality:** Powerful search capabilities that allow you to quickly find pins based on tags, categories, or metadata.
- **Responsive UI:** A simple, responsive web interface for easy interaction with the platform.
- **REST API:** A fully featured API for developers to interact with the platform programmatically.

---

## Usage

1. **Start the Application:**

    You can either run the application locally or deploy it on a cloud service. To start the application locally, follow the installation instructions below.

2. **Upload Pins:**

    Use the web interface to upload images, GIFs, and videos. You can easily tag and categorize pins during the upload process.

3. **Organize Content:**

    Pins can be organized into categories and tagged for easier access. Use the search functionality to quickly find your desired content.

4. **Share Pins:**

    Pins can be shared with other users, or public links can be generated to distribute your media.

---

## Infrastructure & Tech Stack

PinSphere Backend is built with modern, asynchronous Python and distributed systems:

- **Web Framework & API:**
  - **FastAPI (Python 3.12)**: Asynchronous REST API server with dependency injection, Pydantic v2 validation, and auto-generated OpenAPI 3.1 documentation.
  - **Uvicorn / Starlette**: High-concurrency ASGI web server.
- **Data Persistence & Vector Search:**
  - **PostgreSQL 16**: Primary relational database for users, media metadata, comments, and engagement.
  - **pgvector**: Native PostgreSQL extension for high-performance vector similarity and cosine distance search.
  - **SQLAlchemy 2.0 (Async) + Alembic**: Declarative ORM supporting asynchronous connection pooling via `asyncpg` and schema migrations.
  - **JSONB**: Flexible schema storage for custom user preferences and image dimensions.
- **Asynchronous Processing & Caching:**
  - **Celery**: Distributed task queue for asynchronous background jobs (Blurhash generation, Ollama vision inference, embedding generation).
  - **Redis**: In-memory message broker for Celery and caching layer.
- **AI & Multimodal Vision:**
  - **Ollama (`gemma3:4b` vision)**: Multimodal LLM generating rich visual descriptions for uploaded media.
  - **Sentence-Transformers (`all-MiniLM-L6-v2`)**: Dense vector representations for semantic search.
- **Object Storage & Streaming:**
  - **AWS S3 / MinIO**: Object storage using direct-to-S3 pre-signed POST URLs for zero server I/O bottleneck.
- **Authentication & Security:**
  - Google OAuth 2.0 and local password authentication (salted bcrypt hashing) with standard JWT bearer tokens.
- **Observability & Code Quality:**
  - `structlog` & `python-json-logger` for structured logging.
  - `asgi-correlation-id` for end-to-end request tracing.
  - `Pyright` in strict mode and `Ruff` for linting and formatting.

---
## Architecture

### High Level Architecture Diagram

<img src="assets/high_level_architecture.png" alt="Architecture Diagram" />

---

## Installation & Setup

### 1. Prerequisites
- Python 3.12+
- Astral [`uv`](https://github.com/astral-sh/uv)
- Docker & Docker Compose (for PostgreSQL, Redis, MinIO)

### 2. Clone and Install Dependencies:
```bash
git clone https://github.com/saurabh254/PinSphere.git
cd PinSphere/server
uv sync --dev
```

### 3. Environment Configuration:
Create a `.env` file in `server/` with the required parameters:

```env
DATABASE_DSN=postgresql://postgres:postgres@localhost:5432/pin_sphere
REDIS_DSN=redis://localhost:6379/0
CELERY_QUEUE_URL=redis://localhost:6379/1
ALGORITHM=HS256
AUTH_SECRET=your-random-auth-secret-key
REFRESH_TOKEN_EXPIRATION_SECONDS=604800
AWS_STORAGE_BUCKET_NAME=pinsphere
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=minioadmin
AWS_SECRET_ACCESS_KEY=minioadmin123
AWS_SIGNATURE_VERSION=s3v4
AWS_ENDPOINT_URL=http://localhost:9000
ENVIRONMENT=dev
SBERT_MODEL_NAME=sentence-transformers/all-MiniLM-L6-v2
GOOGLE_OAUTH2_CLIENT_ID=your-google-client-id
GOOGLE_OAUTH2_CLIENT_SECRET=your-google-client-secret
GOOGLE_OAUTH2_REDIRECT_URI=http://localhost:5173/auth/google/callback
```

### 4. Start Infrastructure (Docker):
```bash
# Spins up PostgreSQL (pgvector), Redis, and MinIO
docker compose up minio minio-init postgres redis -d
```

### 5. Apply Database Migrations:
```bash
uv run alembic upgrade head
```

### 6. Start Celery Worker:
```bash
uv run celery -A celery_app.app worker --loglevel=INFO
```

### 7. Start FastAPI Application:
```bash
uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be running at `http://localhost:8000`.  
Interactive documentation is available at `http://localhost:8000/docs` (Swagger UI) and `http://localhost:8000/redoc`.

---

## Structure

```
server
├── alembic.ini
├── celery_app.py
├── config.py
├── conf.py
├── conftest.py
├── core
│   ├── authflow
│   │   ├── auth.py
│   │   ├── __init__.py
│   │   └── service.py
│   ├── boto3_client.py
│   ├── database
│   │   ├── base_model.py
│   │   ├── __init__.py
│   │   └── session_manager.py
│   ├── __init__.py
│   ├── models
│   │   ├── images.py
│   │   ├── __init__.py
│   │   └── user.py
│   ├── redis_utils.py
│   ├── storage.py
│   └── types.py
├── docker-compose.yml
├── Dockerfile
├── docs
│   └── conf.py
├── history.sqlite
├── ipython_config.py
├── log
├── logs
│   ├── app.log
│   ├── app.log.2025-02-03
│   ├── app.log.2025-02-04
│   ├── app.log.2025-02-05
│   ├── app.log.2025-02-06
│   ├── app.log.2025-02-08
│   ├── app.log.2025-02-09
│   ├── app.log.2025-02-10
│   ├── celery.log
│   ├── error.log
│   └── sqlalchemy.log
├── main.py
├── ok.png
├── pid
├── pin_sphere
│   ├── api.py
│   ├── auth
│   │   ├── endpoint.py
│   │   ├── exceptions.py
│   │   ├── __init__.py
│   │   ├── schemas.py
│   │   └── service.py
│   ├── base_exception.py
│   ├── exception_handling.py
│   ├── images
│   │   ├── endpoint.py
│   │   ├── exceptions.py
│   │   ├── __init__.py
│   │   ├── schemas.py
│   │   ├── service.py
│   │   ├── tasks.py
│   │   └── utils.py
│   ├── __init__.py
│   └── users
│       ├── endpoints.py
│       ├── __init__.py
│       ├── schemas.py
│       ├── service.py
│       └── tasks.py
├── pyproject.toml
├── pyrightconfig.json
├── README.md
├── scripts
│   └── migrations
│       ├── env.py
│       ├── README
│       ├── script.py.mako
│       └── versions
│           ├── 463fb820ea97_create_metadata_column_in_images_table.py
│           ├── 53c200918d00_create_users_table.py
│           ├── 81e7346f8f87_add_description_in_images_table.py
│           └── f2e1a69354d4_create_images_table.py
├── security
├── setup_logging.py
├── startup
│   ├── 00-imports.py
│   └── README
├── tests
│   ├── fixtures.py
│   ├── __init__.py
│   └── test_users
│       ├── fixtures.py
│       ├── __init__.py
│       └── test_api.py
├── uv.lock
└── what.txt

20 directories, 78 files

```
