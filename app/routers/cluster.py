
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from app.auth import get_db, get_current_user
from app import schemas, crud

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

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
