
# app/schemas.py

from pydantic import BaseModel
from typing import List, Optional

# --- Base Schemas ---
class Point(BaseModel):
    x: float
    y: float

class Dimensions(BaseModel):
    width: float
    height: float

class ObstacleBase(BaseModel):
    bottom_left: Point
    dimensions: Dimensions

# --- Schema for API Input ---

class TrajectoryCreate(BaseModel):
    wall_dimensions: Dimensions
    obstacles: List[ObstacleBase]

# --- Schema for API Output ---
# This is the full object to return from the database.
class Trajectory(BaseModel):
    id: int
    wall_dimensions: Dimensions
    obstacles: List[ObstacleBase]
    path: List[Point]

    
    class Config:
        
        from_attributes = True