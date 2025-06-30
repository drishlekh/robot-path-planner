# tests/test_api.py

from fastapi.testclient import TestClient
import pytest
import os

# We need to adjust the python path to import from the 'app' directory
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.main import app

# --- Test Setup ---

# Create a TestClient instance. This acts like a 'requests' library
# but calls your FastAPI application directly, making it very fast.
client = TestClient(app)

# Define the database file path for testing
TEST_DB = "test_robot_trajectories.db"


@pytest.fixture(scope="module", autouse=True)
def setup_and_teardown():
    """
    A pytest fixture to set up a clean environment for our tests.
    It runs once per test module.
    """
    # Make sure we're using a separate test database
    os.environ["DATABASE_URL"] = f"sqlite:///./{TEST_DB}"
    
    # Run the tests
    yield
    
    # Teardown: Clean up the test database file after tests are complete
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)

# --- Test Cases ---

def test_create_and_get_trajectory():
    """
    A complete test case that simulates the full user flow:
    1. Create a trajectory.
    2. Validate the creation response.
    3. Retrieve the same trajectory by its ID.
    4. Validate the retrieved data.
    """
    # 1. Define the payload for the POST request
    test_payload = {
        "wall_dimensions": {"width": 10, "height": 8},
        "obstacles": [
            {
                "bottom_left": {"x": 2, "y": 2},
                "dimensions": {"width": 1, "height": 1}
            }
        ]
    }

    # 2. Send the POST request to the /api/v1/trajectories/ endpoint
    response_create = client.post("/api/v1/trajectories/", json=test_payload)

    # 3. Assertions for the CREATE request
    assert response_create.status_code == 201  # Check for "201 Created"
    data_create = response_create.json()
    assert "id" in data_create
    assert data_create["wall_dimensions"]["width"] == 10
    assert len(data_create["path"]) > 0  # Make sure a path was actually generated
    
    trajectory_id = data_create["id"]

    # 4. Send a GET request to retrieve the trajectory we just created
    response_get = client.get(f"/api/v1/trajectories/{trajectory_id}")

    # 5. Assertions for the GET request
    assert response_get.status_code == 200
    data_get = response_get.json()
    assert data_get["id"] == trajectory_id
    assert data_get["wall_dimensions"]["width"] == 10
    assert len(data_get["obstacles"]) == 1
    assert data_get["obstacles"][0]["dimensions"]["width"] == 1

def test_get_nonexistent_trajectory():
    """
    Test that the API correctly returns a 404 Not Found error
    when requesting a trajectory ID that doesn't exist.
    """
    response = client.get("/api/v1/trajectories/99999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Trajectory not found"}