# app/schemas.py

from pydantic import BaseModel
from typing import List, Optional

# --- Base Schemas ---
# These define the common attributes.



class Point(BaseModel):
    """A simple 2D point."""
    x: float
    y: float

class Dimensions(BaseModel):
    """Represents the width and height of an object."""
    width: float
    height: float

class ObstacleBase(BaseModel):
    """The basic properties of an obstacle."""
    bottom_left: Point
    dimensions: Dimensions

# --- Schemas for API requests (Input) ---

class TrajectoryCreate(BaseModel):
    """
    This is the blueprint for the data the user MUST send to create a trajectory.
    It defines the expected input format for our API.
    """
    wall_dimensions: Dimensions
    obstacles: List[ObstacleBase]

# --- Schemas for API responses (Output) ---

class Obstacle(ObstacleBase):
    """The obstacle data we will return from our API."""
    id: int

    class Config:
        orm_mode = True # Tells Pydantic to read the data from an ORM model

class Trajectory(BaseModel):
    """

    This is the full blueprint for a trajectory object as it will be returned
    from our API. It includes the ID and the calculated path.
    """
    id: int
    wall_dimensions: Dimensions
    # Note: We are returning a slightly different Obstacle schema that includes an ID
    obstacles: List[Obstacle]
    path: List[Point] # The calculated series of points

    class Config:
        orm_mode = True # This is key! It allows this Pydantic model to be created directly from a SQLAlchemy database object.