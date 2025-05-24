
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
import uuid

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

@router.post("/organization")
def create_organization(org: schemas.OrgCreate, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user = get_current_user(db, token)
    invite_code = str(uuid.uuid4())
    db_org = models.Organization(name=org.name, invite_code=invite_code)
    db.add(db_org)
    db.commit()
    db.refresh(db_org)
    user.organization_id = db_org.id
    db.commit()
    return {"org_id": db_org.id, "invite_code": db_org.invite_code}

@router.post("/join/{invite_code}")
def join_organization(invite_code: str, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user = get_current_user(db, token)
    org = db.query(models.Organization).filter(models.Organization.invite_code == invite_code).first()
    if not org:
        raise HTTPException(status_code=404, detail="Invite code not found")
    user.organization_id = org.id
    db.commit()
    return {"msg": f"User joined organization '{org.name}'"}
