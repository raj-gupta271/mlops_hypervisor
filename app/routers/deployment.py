from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import schemas, models, crud
from fastapi.security import OAuth2PasswordBearer
from app.auth import get_db, get_current_user

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

@router.post("/deployment", response_model=schemas.Deployment)
def create_deployment(
    deployment_in: schemas.DeploymentCreate,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    current_user = get_current_user(db, token)
    # Check cluster exists
    cluster = db.query(models.Cluster).filter(models.Cluster.id == deployment_in.cluster_id).first()
    if not cluster:
        raise HTTPException(status_code=404, detail="Cluster not found")

    # Create deployment with queued status
    deployment = crud.create_deployment(db, deployment_in, current_user.id)
    return deployment

@router.get("/deployments", response_model=List[schemas.Deployment])
def list_deployments(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    current_user = get_current_user(db, token)
    # List deployments for clusters that belong to user's organization
    user_org_id = current_user.organization_id
    clusters = db.query(models.Cluster).filter(models.Cluster.organization_id == user_org_id).all()
    deployments = []
    for cluster in clusters:
        deployments.extend(crud.get_deployments_by_cluster(db, cluster.id))
    return deployments
