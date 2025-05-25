from app.scheduler import scheduler
from app.models import Cluster
from app.database import SessionLocal
from app.logger import log

def scheduler_job(cluster_id: int):
    db = SessionLocal()
    try:
        cluster = db.query(Cluster).filter(Cluster.id == cluster_id).first()
        if cluster:
            log.info(f"Running periodic scheduler for cluster {cluster.id}")
            scheduler(db, cluster)
        else:
            log.warning(f"Cluster {cluster_id} not found for scheduler.")
    except Exception as e:
        log.error(f"Scheduler job failed for cluster {cluster_id}: {str(e)}")
    finally:
        db.close()