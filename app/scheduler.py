from sqlalchemy.orm import Session
from app import models, crud
from app.logger import log
from app.crud import get_queued_deployments

def scheduler(db: Session, cluster: models.Cluster):
    log.info(f"Running scheduler for cluster {cluster.id}")

    # Available resources (copy them to track allocation)
    available_cpu = cluster.cpu - cluster.cpu_allocated
    available_ram = cluster.ram - cluster.ram_allocated
    available_gpu = cluster.gpu - cluster.gpu_allocated

    log.info(f"Available resources: CPU={available_cpu}, RAM={available_ram}, GPU={available_gpu}")

    # Get all queued deployments for the cluster
    deployments = get_queued_deployments(db, cluster.id)

    # Sort deployments by priority (ascending = highest priority first)
    deployments.sort(key=lambda d: d.priority)

    any_scheduled = False
    for deployment in deployments:
        if (deployment.cpu <= available_cpu and
            deployment.ram <= available_ram and
            deployment.gpu <= available_gpu):

            # Allocate resources
            deployment.status = "running"
            available_cpu -= deployment.cpu
            available_ram -= deployment.ram
            available_gpu -= deployment.gpu

            # Update allocated usage on the cluster
            cluster.cpu_allocated += deployment.cpu
            cluster.ram_allocated += deployment.ram
            cluster.gpu_allocated += deployment.gpu
            db.add(deployment)
            db.add(cluster)
            db.commit()

            log.info(f"Scheduled deployment {deployment.id} (priority {deployment.priority})")
            any_scheduled = True
            break

    if not any_scheduled:
        log.info("No deployments could be scheduled due to insufficient resources.")