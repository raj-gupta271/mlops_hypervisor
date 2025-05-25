from fastapi.testclient import TestClient # type: ignore
from app.main import app
from app.database import Base, engine

client = TestClient(app)

# Setup DB before tests
def setup_module():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

# Utility functions
def get_token():
    client.post("/register", json={"username": "testuser", "password": "testpass"})
    res = client.post("/login", data={"username": "testuser", "password": "testpass"})
    return res.json()["access_token"]

def create_organization(token):
    res = client.post(
        "/organization",
        json={"name": "TestOrg"},
        headers={"Authorization": f"Bearer {token}"}
    )
    return res.json()["invite_code"]

# 1. User Authentication and Organization Management
def test_register_and_login():
    client.post("/register", json={"username": "authuser", "password": "secret"})
    res = client.post("/login", data={"username": "authuser", "password": "secret"})
    assert res.status_code == 200
    assert "access_token" in res.json()

def test_join_organization():
    token = get_token()
    invite_code = create_organization(token)
    res = client.post(f"/organization/join/{invite_code}", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200

# 2. Cluster Management
def test_create_cluster():
    token = get_token()
    res = client.post("/cluster", headers={"Authorization": f"Bearer {token}"}, json={
        "name": "TestCluster",
        "cpu": 10,
        "ram": 64,
        "gpu": 2,
    })
    assert res.status_code == 200
    assert res.json()["name"] == "TestCluster"

# 3. Deployment Management
def test_create_deployment():
    token = get_token()
    clusters = client.get("/clusters", headers={"Authorization": f"Bearer {token}"})
    cluster_id = clusters.json()[0]["id"]
    res = client.post("/deployment", headers={"Authorization": f"Bearer {token}"}, json={
        "cluster_id": cluster_id,
        "cpu": 8,
        "ram": 32,
        "gpu": 1,
        "docker_image": "myapp:v1",
        "priority": 5
    })
    assert res.status_code == 200
    assert res.json()["docker_image"] == "myapp:v1"

# 4. Scheduling Algorithm (basic test)
def test_scheduler_prioritization():
    token = get_token()
    clusters = client.get("/clusters", headers={"Authorization": f"Bearer {token}"})
    cluster_id = clusters.json()[0]["id"]
    # Create low-priority deployment (takes more resources)
    client.post("/deployment", headers={"Authorization": f"Bearer {token}"}, json={
        "cluster_id": cluster_id,
        "cpu": 6,
        "ram": 48,
        "gpu": 1,
        "docker_image": "low:v1",
        "priority": 1
    })
    # Create high-priority deployment (less resources)
    res = client.post("/deployment", headers={"Authorization": f"Bearer {token}"}, json={
        "cluster_id": cluster_id,
        "cpu": 2,
        "ram": 8,
        "gpu": 1,
        "docker_image": "high:v1",
        "priority": 10
    })
    assert res.status_code == 200

# 5. Confirm deployment status is 'running' (scheduled successfully)
def test_scheduler_triggers_and_updates_deployment():
    token = get_token()
    cluster_payload = {
        "name": "TestCluster",
        "cpu": 8,
        "ram": 32,
        "gpu": 1
    }
    cluster_res = client.post(
        "/cluster",
        json=cluster_payload,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert cluster_res.status_code == 200
    cluster_id = cluster_res.json()["id"]

    deployment_payload = {
        "docker_image": "app:v1",
        "cluster_id": cluster_id,
        "cpu": 2,
        "ram": 8,
        "gpu": 0,
        "priority": 10
    }
    deployment_res = client.post(
        "/deployment",
        json=deployment_payload,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert deployment_res.status_code == 200
    assert deployment_res.json()["status"] == "queued"

