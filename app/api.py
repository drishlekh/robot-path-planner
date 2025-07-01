# app/api.py

import time
import json 
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from . import crud, schemas, path_planner, models
from .database import get_db

router = APIRouter()

# --- Logging Dependency ---
async def log_request_timing(response_time_ms: float = 0):
    start_time = time.time()
    yield
    process_time = (time.time() - start_time) * 1000
    print(f"--- Request Handled: Processed in {process_time:.2f}ms ---")

# --- API Endpoints ---
@router.post("/trajectories/", response_model=schemas.Trajectory, status_code=201, dependencies=[Depends(log_request_timing)])
def create_new_trajectory(
    trajectory_in: schemas.TrajectoryCreate,
    tool_width: float = 0.1, 
    db: Session = Depends(get_db),
):
    
    print("--- Received POST request to create trajectory ---")
    print(f"Input: Wall({trajectory_in.wall_dimensions.width}x{trajectory_in.wall_dimensions.height}), ToolWidth({tool_width})")
    
    # 1. Calculating the path
    calculated_path = path_planner.generate_path(
        wall_dimensions=trajectory_in.wall_dimensions,
        obstacles=trajectory_in.obstacles,
        tool_width=tool_width
    )

    # 2. Calling the CRUD function to save to the database
    db_trajectory = crud.create_trajectory(
        db=db, 
        trajectory_data=trajectory_in,
        path=calculated_path,
        tool_width=tool_width
    )
    
    
    return schemas.Trajectory(
        id=db_trajectory.id,
        wall_dimensions=json.loads(db_trajectory.wall_dimensions_json),
        obstacles=[schemas.ObstacleBase(**obs) for obs in json.loads(db_trajectory.obstacles_json)],
        path=[schemas.Point(**p) for p in json.loads(db_trajectory.path_json)]
    )


@router.get("/trajectories/{trajectory_id}", response_model=schemas.Trajectory, dependencies=[Depends(log_request_timing)])
def read_trajectory(
    trajectory_id: int, 
    db: Session = Depends(get_db)
):
    
    print(f"--- Received GET request for trajectory ID: {trajectory_id} ---")
    db_trajectory = crud.get_trajectory(db, trajectory_id=trajectory_id)
    
    if db_trajectory is None:
        raise HTTPException(status_code=404, detail="Trajectory not found")
        
    # Reconstruct the object for the response model, same as in the POST endpoint
    return schemas.Trajectory(
        id=db_trajectory.id,
        wall_dimensions=json.loads(db_trajectory.wall_dimensions_json),
        obstacles=[schemas.ObstacleBase(**obs) for obs in json.loads(db_trajectory.obstacles_json)],
        path=[schemas.Point(**p) for p in json.loads(db_trajectory.path_json)]
    )