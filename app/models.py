# app/models.py

from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text
from sqlalchemy.orm import relationship

from .database import Base

# This class defines the 'trajectories' table in the database.
# SQLAlchemy uses this model to understand how to interact with the table.
class Trajectory(Base):
    __tablename__ = "trajectories"

    # The primary key for the table, with an index for fast lookups.
    id = Column(Integer, primary_key=True, index=True)
    
    
    wall_dimensions_json = Column(String(255))
    obstacles_json = Column(Text)
    path_json = Column(Text)