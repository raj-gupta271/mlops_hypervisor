
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app import models, schemas, auth

def get_user(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_cluster(db: Session, cluster: schemas.ClusterCreate, org_id: int):
    db_cluster = models.Cluster(
        name=cluster.name,
        cpu=cluster.cpu,
        ram=cluster.ram,
        gpu=cluster.gpu,
        organization_id=org_id
    )
    db.add(db_cluster)
    db.commit()
    db.refresh(db_cluster)
    return db_cluster

def get_clusters_by_org(db: Session, org_id: int):
    return db.query(models.Cluster).filter(models.Cluster.organization_id == org_id).all()


def create_deployment(db: Session, deployment: schemas.DeploymentCreate, user_id: int):
    db_deployment = models.Deployment(
        docker_image=deployment.docker_image,
        cpu=deployment.cpu,
        ram=deployment.ram,
        gpu=deployment.gpu,
        priority=deployment.priority,
        cluster_id=deployment.cluster_id,
        user_id=user_id,
        status=models.DeploymentStatus.queued
    )
    db.add(db_deployment)
    db.commit()
    db.refresh(db_deployment)
    return db_deployment

def get_deployments_by_cluster(db: Session, cluster_id: int):
    return db.query(models.Deployment).filter(models.Deployment.cluster_id == cluster_id).all()

def get_deployments_by_status(db: Session, cluster_id: int, status: models.DeploymentStatus):
    return db.query(models.Deployment).filter(
        and_(
            models.Deployment.cluster_id == cluster_id,
            models.Deployment.status == status
        )
    ).all()

def update_deployment_status(db: Session, deployment: models.Deployment, status: models.DeploymentStatus):
    deployment.status = status
    db.commit()
    db.refresh(deployment)
    return deployment

def get_queued_deployments(db: Session, cluster_id: int):
    return db.query(models.Deployment)\
        .filter(models.Deployment.cluster_id == cluster_id)\
        .filter(models.Deployment.status == "queued")\
        .order_by(models.Deployment.priority.asc())\
        .all()

