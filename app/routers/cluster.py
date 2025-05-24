
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer

from app import models, schemas, crud
from app.database import SessionLocal

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(db: Session, token: str):
    user = crud.get_user(db, token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user

@router.post("/cluster")
def create_cluster(cluster: schemas.ClusterCreate, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user = get_current_user(db, token)
    if not user.organization_id:
        raise HTTPException(status_code=400, detail="User must belong to an organization to create a cluster")
    return crud.create_cluster(db, cluster, user.organization_id)

@router.get("/clusters")
def list_clusters(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user = get_current_user(db, token)
    if not user.organization_id:
        raise HTTPException(status_code=400, detail="User must belong to an organization")
    return crud.get_clusters_by_org(db, user.organization_id)
