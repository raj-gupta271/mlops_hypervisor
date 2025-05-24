
# MLOps Hypervisor Backend Service

## Overview

This backend service provides user authentication, organization and cluster management, deployment creation, and scheduling for an MLOps platform. The service schedules containerized deployments to clusters based on resource availability and priority.

---

## Features

- User registration and JWT-based authentication
- Organization membership via invite codes
- Cluster management with fixed resource tracking (CPU, RAM, GPU)
- Deployment creation with resource requirements
- Priority-based scheduling with resource optimization and preemption
- REST API with OpenAPI docs via Swagger and ReDoc

---

## Setup and Run Instructions

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/mlops_hypervisor.git
cd mlops_hypervisor
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate    # On Windows use: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Initialize the database

For SQLite (default):

```bash
python -c "from app.database import Base, engine; Base.metadata.create_all(bind=engine)"
```

If you use migrations with Alembic:

```bash
alembic upgrade head
```

### 5. Run the application

```bash
uvicorn app.main:app --reload
```

The API will be available at: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## Usage

- Access interactive API docs:

  - Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)  
  - ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

- Key API endpoints:

  - `POST /register` — Register a new user
  - `POST /token` — Obtain JWT access tokens
  - `POST /organizations/join/{invite_code}` — Join an organization
  - `/clusters` — Create, list, and manage clusters
  - `/deployments` — Create and manage deployments

---

## Environment Variables (Optional)

| Variable      | Description                 | Default                  |
| ------------- | ---------------------------| ------------------------ |
| `DATABASE_URL`| Database connection string | `sqlite:///./app.db`     |
| `SECRET_KEY`  | JWT signing secret         | `your-secret-key`        |

---

## Architecture Overview

- **FastAPI**: Web framework for REST APIs
- **SQLAlchemy**: ORM for database interaction
- **SQLite/PostgreSQL**: Database backend
- **JWT**: Token-based authentication
- **Scheduling Algorithm**: Priority-based deployment scheduling with resource preemption

---

## Scheduling Algorithm Details

The scheduler:

1. Sorts queued deployments by priority (highest first).
2. Checks available resources on the target cluster.
3. Allocates resources if available and starts the deployment.
4. Uses a preemption strategy to evict lower-priority deployments if necessary to accommodate higher-priority ones.
5. Raises an error if no deployments can be scheduled due to resource constraints.

---

## Testing

- Unit tests cover key components like authentication, cluster management, deployment creation, and scheduling.
- Run tests using:

```bash
pytest
```

---

## License

Specify your project license here.

---

## Contact

For questions or support, contact: Your Name - abhijeet.raj271@gmail.com
