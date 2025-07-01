
# app/crud.py

from sqlalchemy.orm import Session
import json


from . import models, schemas

# --- Read Operation ---
def get_trajectory(db: Session, trajectory_id: int):
    """
    Reads a single trajectory from the database by its ID.
    """
    
    return db.query(models.Trajectory).filter(models.Trajectory.id == trajectory_id).first()

# --- Create Operation ---
def create_trajectory(db: Session, trajectory_data: schemas.TrajectoryCreate, path: list, tool_width: float):
    """
    Creates a new trajectory record in the database.
    """
    
    wall_dimensions_str = json.dumps(trajectory_data.wall_dimensions.dict())
    obstacles_str = json.dumps([obs.dict() for obs in trajectory_data.obstacles])
    path_str = json.dumps([p.dict() for p in path])

    
    db_trajectory = models.Trajectory(
        wall_dimensions_json=wall_dimensions_str,
        obstacles_json=obstacles_str,
        path_json=path_str
    )
    
    db.add(db_trajectory)
    db.commit()
    db.refresh(db_trajectory)
    
    return db_trajectory