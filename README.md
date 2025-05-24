# MLOps Hypervisor Backend Service

## Overview

This backend service is designed to manage user authentication, organization membership, cluster resource allocation, deployment creation, and scheduling for an MLOps platform. It optimizes deployment scheduling based on priority and resource availability.

---

## Features

- User Registration & Authentication with JWT
- Organization Membership via Invite Codes
- Cluster Management (Create, Track Resources)
- Deployment Management (Create, List)
- Priority-based Deployment Scheduling with Resource Preemption
- API documented with OpenAPI / Swagger UI

---

## Tech Stack

- **Python 3.10+**
- **FastAPI** for REST API
- **SQLAlchemy** ORM
- **SQLite** as the default database (can be switched to PostgreSQL)
- **Uvicorn** ASGI server
- **Redis** (optional) for queue management (if implemented)
- **JWT** for secure authentication

---

## Prerequisites

- Python 3.10 or later installed
- Git installed (optional, for cloning repo)
- (Optional) Redis server if you want to enable queueing

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-repo/mlops_hypervisor.git
cd mlops_hypervisor
```

### 2. Create and Activate Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Initialize the Database

#### For SQLite (default):

```bash
python -c "from app.database import Base, engine; Base.metadata.create_all(bind=engine)"
```

#### If you use migrations with Alembic:
```bash
alembic upgrade head
```

### 5. Run the application

```bash
uvicorn app.main:app --reload
```

## The API will be available at: http://127.0.0.1:8000



