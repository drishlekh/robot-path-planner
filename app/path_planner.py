# app/path_planner.py

from typing import List
from .schemas import Dimensions, ObstacleBase, Point

# --- Helper function for a standard vertical "lawnmower" pattern ---
def generate_vertical_path(path: List[Point], start_x, end_x, wall_height, tool_width):
    current_x = start_x
    # Determine direction based on the last point's y-coordinate
    direction = 1 if path[-1].y == 0.0 else -1

    while current_x <= end_x:
        target_y = wall_height if direction == 1 else 0.0
        path.append(Point(x=current_x, y=target_y))
        
        current_x += tool_width
        if current_x <= end_x:
            path.append(Point(x=current_x, y=target_y))
        
        direction *= -1

# --- Helper function for a horizontal pattern (for above/below obstacle) ---
def generate_horizontal_path(path: List[Point], start_y, end_y, start_x, end_x, tool_width):
    current_y = start_y
    # Determine direction based on the last point's x-coordinate
    direction = 1 if path[-1].x == start_x else -1

    while current_y <= end_y:
        target_x = end_x if direction == 1 else start_x
        path.append(Point(x=target_x, y=current_y))
        
        current_y += tool_width
        if current_y <= end_y:
            path.append(Point(x=target_x, y=current_y))

        direction *= -1

# --- The Main Path Planner ---
def generate_path(
    wall_dimensions: Dimensions,
    obstacles: List[ObstacleBase],
    tool_width: float
) -> List[Point]:
    """
    Generates a full coverage path by dividing the wall into zones around the obstacle.
    """
    path = [Point(x=0.0, y=0.0)]
    
    # For this assignment, we focus on a single, primary obstacle.
    if not obstacles:
        # No obstacles, just do a simple vertical path over the whole wall
        generate_vertical_path(path, 0.0, wall_dimensions.width, wall_dimensions.height, tool_width)
        return path

    obs = obstacles[0]
    obs_x_min = obs.bottom_left.x
    obs_x_max = obs.bottom_left.x + obs.dimensions.width
    obs_y_min = obs.bottom_left.y
    obs_y_max = obs.bottom_left.y + obs.dimensions.height

    # --- ZONE 1: Left of the Obstacle ---
    generate_vertical_path(path, 0.0, obs_x_min, wall_dimensions.height, tool_width)

    # --- ZONE 2: Above and Below the Obstacle ---
    # The robot is now at (obs_x_min, y). We need to paint the regions
    # above and below the obstacle using a horizontal pattern.
    
    # Path for the area BELOW the obstacle
    path.append(Point(x=obs_x_min, y=0.0)) # Move to the start corner
    generate_horizontal_path(path, 0.0, obs_y_min, obs_x_min, obs_x_max, tool_width)

    # Path for the area ABOVE the obstacle
    # Jump the robot to the starting corner of the area above the obstacle
    path.append(Point(x=path[-1].x, y=obs_y_max))
    generate_horizontal_path(path, obs_y_max, wall_dimensions.height, obs_x_min, obs_x_max, tool_width)
    
    # --- ZONE 3: Right of the Obstacle ---
    # Move the robot to the starting position for the final zone
    path.append(Point(x=obs_x_max, y=path[-1].y))
    generate_vertical_path(path, obs_x_max, wall_dimensions.width, wall_dimensions.height, tool_width)

    return path