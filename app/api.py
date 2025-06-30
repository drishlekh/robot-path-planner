# app/api.py

import time
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from . import crud, schemas, path_planner
from .database import get_db

router = APIRouter()

async def log_request(request_id: str = None):
    start_time = time.time()
    print(f"--- Request Start ---")
    yield
    process_time = (time.time() - start_time) * 1000
    formatted_process_time = '{0:.2f}'.format(process_time)
    print(f"--- Request End: Processed in {formatted_process_time}ms ---")

@router.post("/trajectories/", response_model=schemas.Trajectory, status_code=201)
def create_new_trajectory(
    trajectory_in: schemas.TrajectoryCreate,
    # Accept tool_width as a query parameter (e.g., /trajectories/?tool_width=0.1)
    tool_width: float = 0.1, 
    db: Session = Depends(get_db),
    log: None = Depends(log_request)
):
    """
    Create a new trajectory.
    This endpoint receives wall and obstacle data, calculates the path,
    stores it in the database, and returns the complete trajectory object.
    """
    print(f"Received request with tool_width: {tool_width}")
    
    # Pass the tool_width to the path planner
    calculated_path = path_planner.generate_path(
        wall_dimensions=trajectory_in.wall_dimensions,
        obstacles=trajectory_in.obstacles,
        tool_width=tool_width
    )

    db_trajectory = crud.create_trajectory(
        db=db, 
        trajectory_data=trajectory_in,
        path=calculated_path
    )
    
    print(f"Successfully created and stored trajectory with ID: {db_trajectory.id}")
    return db_trajectory


@router.get("/trajectories/{trajectory_id}", response_model=schemas.Trajectory)
def read_trajectory(
    trajectory_id: int, 
    db: Session = Depends(get_db),
    log: None = Depends(log_request)
):
    print(f"Received request to retrieve trajectory with ID: {trajectory_id}")
    db_trajectory = crud.get_trajectory(db, trajectory_id=trajectory_id)
    
    if db_trajectory is None:
        raise HTTPException(status_code=404, detail="Trajectory not found")
        
    print(f"Found trajectory ID: {trajectory_id}. Returning data.")
    return db_trajectory