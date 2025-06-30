# app/crud.py

from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
import json

from . import database, schemas

# --- SQLAlchemy Database Models ---
# These classes define the structure of our database tables.
# This is where we use the 'Base' we created in database.py.

class TrajectoryModel(database.Base):
    __tablename__ = "trajectories"

    id = Column(Integer, primary_key=True, index=True)
    
    # We store complex data like dimensions and path as JSON strings in the database.
    # This is a simple approach for SQLite.
    wall_dimensions_json = Column(String, name="wall_dimensions")
    path_json = Column(String, name="path")

    # This creates a 'one-to-many' relationship. One trajectory can have many obstacles.
    obstacles = relationship("ObstacleModel", back_populates="trajectory")

    @property
    def wall_dimensions(self):
        return json.loads(self.wall_dimensions_json)

    @property
    def path(self):
        return json.loads(self.path_json)

class ObstacleModel(database.Base):
    __tablename__ = "obstacles"

    id = Column(Integer, primary_key=True, index=True)
    bottom_left_x = Column(Float)
    bottom_left_y = Column(Float)
    width = Column(Float)
    height = Column(Float)
    
    trajectory_id = Column(Integer, ForeignKey("trajectories.id"))
    trajectory = relationship("TrajectoryModel", back_populates="obstacles")

    # This is not the most elegant way, but it bridges the gap between our
    # database model and our Pydantic schema.
    @property
    def bottom_left(self):
        return {"x": self.bottom_left_x, "y": self.bottom_left_y}

    @property
    def dimensions(self):
        return {"width": self.width, "height": self.height}


# --- CRUD Functions ---

def get_trajectory(db: Session, trajectory_id: int):
    """
    Reads a single trajectory from the database by its ID.
    """
    # .first() returns the first result or None if not found.
    return db.query(TrajectoryModel).filter(TrajectoryModel.id == trajectory_id).first()


def create_trajectory(db: Session, trajectory_data: schemas.TrajectoryCreate, path: list):
    """
    Creates a new trajectory record in the database.
    
    Args:
        db: The database session.
        trajectory_data: The input data from the user (wall dimensions, obstacles).
        path: The calculated path from the path_planner.
    """
    # Convert complex objects to JSON strings for storage
    wall_dimensions_str = json.dumps(trajectory_data.wall_dimensions.dict())
    path_str = json.dumps([p.dict() for p in path])

    # Create the main trajectory database object
    db_trajectory = TrajectoryModel(
        wall_dimensions_json=wall_dimensions_str,
        path_json=path_str
    )
    
    # Add it to the session (staging area)
    db.add(db_trajectory)
    # Commit the session to write the trajectory to the database and get its ID
    db.commit()
    # Refresh the object to get the ID that the database assigned
    db.refresh(db_trajectory)

    # Now, create the associated obstacle objects
    for obs_data in trajectory_data.obstacles:
        db_obstacle = ObstacleModel(
            bottom_left_x=obs_data.bottom_left.x,
            bottom_left_y=obs_data.bottom_left.y,
            width=obs_data.dimensions.width,
            height=obs_data.dimensions.height,
            trajectory_id=db_trajectory.id # Link it to the trajectory we just created
        )
        db.add(db_obstacle)

    # Commit again to save the obstacles
    db.commit()
    db.refresh(db_trajectory)
    
    return db_trajectory