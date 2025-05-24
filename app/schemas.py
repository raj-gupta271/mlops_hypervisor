from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum

class UserCreate(BaseModel):
    username: str
    password: str

class OrgCreate(BaseModel):
    name: str

class ClusterCreate(BaseModel):
    name: str
    cpu: int
    ram: int
    gpu: int

class DeploymentStatus(str, Enum):
    queued = "queued"
    running = "running"
    completed = "completed"
    failed = "failed"
    preempted = "preempted"

class DeploymentCreate(BaseModel):
    docker_image: str
    cpu: int = Field(gt=0)
    ram: int = Field(gt=0)
    gpu: int = Field(ge=0)
    priority: int = 0
    cluster_id: int

class Deployment(BaseModel):
    id: int
    docker_image: str
    cpu: int
    ram: int
    gpu: int
    priority: int
    status: DeploymentStatus
    cluster_id: int
    user_id: int

    class Config:
        orm_mode = True