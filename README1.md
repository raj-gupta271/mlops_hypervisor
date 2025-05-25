
# 🧠 MLOps Hypervisor Backend

A backend service that manages user authentication, organizations, clusters, and deployment scheduling for MLOps workflows. Built with **FastAPI**, **SQLAlchemy**, **Redis**, **RQ**, and **RQ-Scheduler**.

---

## 🚀 Features

- ✅ **User Authentication** with JWT
- 🏢 **Organization & User Management**
- 📦 **Cluster Management**
- ⚙️ **Deployment Lifecycle** (Create, Queue, Start, Fail)
- 🧠 **Priority-Based Scheduling** with Preemption
- 🧵 **Background Job Scheduling** using RQ & RQ-Scheduler
- 🔒 **Role-Based Access Control**
- 🐳 Dockerized setup (optional)

---

## 🛠️ Tech Stack

- **FastAPI** — API framework
- **SQLAlchemy** — ORM
- **PostgreSQL / SQLite** — Database
- **Redis** — In-memory job broker
- **RQ / RQ-Scheduler** — Background job & scheduling
- **JWT** — Auth
- **Docker** — Containerization (optional)

---

## 📦 Setup Instructions

### 1. Clone the Repo

```bash
git clone https://github.com/your-org/mlops-hypervisor.git
cd mlops-hypervisor
```

### 2. Create and Activate Virtual Environment

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Start Redis Server

```bash
redis-server
```

### 5. Start RQ Worker & Scheduler

```bash
# In one terminal
rq worker

# In another terminal
rqscheduler
```

### 6. Start the FastAPI Server

```bash
uvicorn app.main:app --reload
```

---

## 📚 API Endpoints

### 🔐 Auth

- `POST /register` — Register a new user
- `POST /login` — Get JWT access token

### 🏢 Organization & User

- `POST /organization/` — Create organization
- `POST /organization/join/{invite_code}` — Add user to org

### 🖥️ Cluster

- `POST /cluster` — Create a cluster
- `GET /clusters` — List all clusters

### 🚀 Deployments

- `POST /deployment` — Create deployment (goes into `QUEUED`)
- `GET /deployments` — List deployments
- Automatic scheduling every 30s based on cluster

### Access interactive API docs:

  - Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)  
  - ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 📅 Scheduling Logic

- Scheduler jobs are created:
  - **On cluster creation** (post-hook)
  - **Once for each cluster**, running every 30 seconds
- Uses RQ-scheduler to enqueue `scheduler_job(cluster_id)`
- Scheduling respects:
  - Deployment priority
  - Cluster resource availability
  - Preemption of lower-priority jobs if needed

---

## 🐳 Docker (Optional)

 - DockerFile

---

## 🧪 Tests

- Unit tests cover key components like authentication, cluster management, deployment creation, and scheduling.
- Run tests using:

```bash
python -m pytest tests
```

---

## 📂 Project Structure

```
app/
├── main.py                # FastAPI entrypoint
├── models.py              # SQLAlchemy models
├── schemas.py             # Pydantic schemas
├── crud.py                # DB operations
├── database.py            # DB session & base
├── routers/               # All API routes
├── tasks.py               # Background jobs (scheduler_job)
├── scheduler.py           # RQ-scheduler config
├── security.py            # JWT Token generation
```

---

## 📌 Requirements

See [`requirements.txt`](./requirements.txt) for details.

---

## 👨‍💻 Author

Abhijeet Raj  
_Contact for any suggestions, issues, or contributions._

### Contact

For questions or support, contact: Your Name - abhijeet.raj271@gmail.com

---
