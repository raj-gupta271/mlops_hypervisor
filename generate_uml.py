from sqlalchemy.orm import declarative_base
from graphviz import Digraph
from app.models import User, Organization, Cluster, Deployment

Base = declarative_base()

dot = Digraph(comment='Database UML Diagram')
tables = [User, Organization, Cluster, Deployment]

for table in tables:
    fields = [f"{col.name}: {col.type.__class__.__name__}" for col in table.__table__.columns]
    label = f"{table.__tablename__}|" + "\\l".join(fields) + "\\l"
    dot.node(table.__tablename__, label=label, shape='record')

dot.edge('users', 'organizations', label='organization_id')
dot.edge('clusters', 'organizations', label='organization_id')
dot.edge('deployments', 'clusters', label='cluster_id')
dot.edge('deployments', 'users', label='user_id')

dot.render('database_uml_diagram', format='png', cleanup=True)
