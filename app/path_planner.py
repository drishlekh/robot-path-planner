# app/path_planner.py

from typing import List
from .schemas import Dimensions, ObstacleBase, Point

# --- Helper for a standard Vertical Lawnmower Pattern ---
def _generate_vertical_path(path: List[Point], start_x: float, end_x: float, wall_height: float, tool_width: float):
    current_x = start_x
    # Determine sweep direction based on the last point's y-coordinate
    direction = 1 if path[-1].y < wall_height / 2 else -1

    while current_x < end_x:
        target_y = wall_height if direction == 1 else 0.0
        path.append(Point(x=current_x, y=target_y))
        
        current_x += tool_width
        path.append(Point(x=current_x, y=target_y))
        
        direction *= -1
    
    # Ensure the final point is exactly at the end_x boundary
    path.append(Point(x=end_x, y=path[-1].y))


# --- Helper for a standard Horizontal Lawnmower Pattern ---
def _generate_horizontal_path(path: List[Point], start_y: float, end_y: float, x_min: float, x_max: float, tool_width: float):
    current_y = start_y
    # Determine sweep direction based on the last point's x-coordinate
    direction = 1 if path[-1].x < (x_min + x_max) / 2 else -1

    while current_y < end_y:
        target_x = x_max if direction == 1 else x_min
        path.append(Point(x=target_x, y=current_y))
        
        current_y += tool_width
        path.append(Point(x=target_x, y=current_y))
        
        direction *= -1

    # Ensuring the final point is exactly at the end_y boundary
    path.append(Point(x=path[-1].x, y=end_y))

# --- The Main Path Generation Logic ---
def generate_path(
    wall_dimensions: Dimensions,
    obstacles: List[ObstacleBase],
    tool_width: float
) -> List[Point]:
    """
    Generates a full coverage path by dividing the wall into zones around the obstacle.
    """
    path = [Point(x=0.0, y=0.0)]
    
    # If there are no obstacles, it does a simple run over the whole wall.
    if not obstacles:
        _generate_vertical_path(path, 0.0, wall_dimensions.width, wall_dimensions.height, tool_width)
        return path

    obs = obstacles[0]
    obs_x_min = obs.bottom_left.x
    obs_x_max = obs.bottom_left.x + obs.dimensions.width
    obs_y_min = obs.bottom_left.y
    obs_y_max = obs.bottom_left.y + obs.dimensions.height

    # --- ZONE 1: Paint area to the LEFT of the obstacle ---
    if obs_x_min > 0:
        _generate_vertical_path(path, 0.0, obs_x_min, wall_dimensions.height, tool_width)

    # --- ZONE 2: Paint areas ABOVE and BELOW the obstacle ---
    # Move to the starting corner for the area BELOW the obstacle
    path.append(Point(x=obs_x_min, y=0.0))
    if obs_y_min > 0:
        _generate_horizontal_path(path, 0.0, obs_y_min, obs_x_min, obs_x_max, tool_width)

    # Move to the starting corner for the area ABOVE the obstacle
    path.append(Point(x=path[-1].x, y=obs_y_max))
    if obs_y_max < wall_dimensions.height:
        _generate_horizontal_path(path, obs_y_max, wall_dimensions.height, obs_x_min, obs_x_max, tool_width)
    
    # --- ZONE 3: Paint area to the RIGHT of the obstacle ---
    # Move to the starting position for the final zone
    path.append(Point(x=obs_x_max, y=path[-1].y))
    if obs_x_max < wall_dimensions.width:
        _generate_vertical_path(path, obs_x_max, wall_dimensions.width, wall_dimensions.height, tool_width)

    return path