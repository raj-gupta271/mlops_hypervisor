
from fastapi import FastAPI
from app.routers import user, organization, cluster, deployment

app = FastAPI()

app.include_router(user.router)
app.include_router(organization.router)
app.include_router(cluster.router)
app.include_router(deployment.router)
