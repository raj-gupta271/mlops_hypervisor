
from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.database import Base
import enum

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=True)

class Organization(Base):
    __tablename__ = 'organizations'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    invite_code = Column(String, unique=True)
    users = relationship("User", backref="organization")

class Cluster(Base):
    __tablename__ = 'clusters'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    cpu = Column(Integer)
    ram = Column(Integer)
    gpu = Column(Integer)
    cpu_allocated = Column(Integer, default=0)  # currently allocated CPU
    ram_allocated = Column(Integer, default=0)  # currently allocated RAM
    gpu_allocated = Column(Integer, default=0)  # currently allocated GPU
    organization_id = Column(Integer, ForeignKey("organizations.id"))

class DeploymentStatus(str, enum.Enum):
    queued = "queued"
    running = "running"
    completed = "completed"
    failed = "failed"
    preempted = "preempted"

class Deployment(Base):
    __tablename__ = 'deployments'
    id = Column(Integer, primary_key=True, index=True)
    docker_image = Column(String)
    cpu = Column(Integer)
    ram = Column(Integer)
    gpu = Column(Integer)
    priority = Column(Integer, default=0)
    status = Column(Enum(DeploymentStatus), default=DeploymentStatus.queued)
    cluster_id = Column(Integer, ForeignKey("clusters.id"))
    user_id = Column(Integer, ForeignKey("users.id"))

    cluster = relationship("Cluster", backref="deployments")
    user = relationship("User", backref="deployments")

