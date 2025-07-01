# tests/test_api.py

import pytest
from fastapi.testclient import TestClient
import os
import sys

# This is a common trick to make sure Python can find your 'app' module.
# It adds the parent directory (your project root) to the system path.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.main import app
from app.database import Base, get_db, engine

# --- Test Setup ---

# Create a TestClient. This is like a 'requests' library that can call
# your FastAPI application directly without needing a running server. It's fast.
client = TestClient(app)

# --- Test Fixture for a Clean Database ---

@pytest.fixture(scope="module", autouse=True)
def session_override():
    """
    This is a pytest fixture that runs once for this entire test file.
    It does three things:
    1. Deletes the old test database file if it exists.
    2. Creates all the new tables based on your models.
    3. 'yield's to let the tests run.
    4. Deletes the test database file after all tests are finished.
    This ensures every test run starts with a clean, empty database.
    """
    # Define the path for our temporary test database
    TEST_DB_PATH = "./test_trajectories.db"
    
    # Delete the old test DB if it exists
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)
    
    # Create the tables in the new test DB
    Base.metadata.create_all(bind=engine)
    
    yield # This is where the tests will run
    
    # Teardown: clean up the database file after tests
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)


# --- The Actual Tests ---

def test_create_and_read_trajectory():
    """
    This is an integration test for the basic CRUD operations:
    1. CREATE a new trajectory via a POST request.
    2. READ the same trajectory back via a GET request.
    3. Validate the data and response times at each step.
    """
    # 1. ARRANGE: Define the data we will send to the API.
    test_payload = {
        "wall_dimensions": {"width": 10, "height": 8},
        "obstacles": [{
            "bottom_left": {"x": 3, "y": 3},
            "dimensions": {"width": 1, "height": 2}
        }]
    }
    tool_width = 0.2

    # 2. ACT (CREATE): Send the POST request to the creation endpoint.
    response_create = client.post(f"/api/v1/trajectories/?tool_width={tool_width}", json=test_payload)

    # 3. ASSERT (CREATE): Check that the creation was successful.
    assert response_create.status_code == 201, "Status code for creation should be 201 Created."
    
    # Validate a simple response time sanity check.
    # This checks if the request took less than 1 second.
    assert response_create.elapsed.total_seconds() < 1, "Creation response time should be under 1 second."
    
    # Check the contents of the response.
    data_create = response_create.json()
    assert "id" in data_create, "Response must contain a trajectory ID."
    assert data_create["wall_dimensions"]["width"] == 10
    assert len(data_create["path"]) > 1, "A valid path with multiple points should be generated."

    # --- Now test the READ part of CRUD ---

    # 4. ARRANGE (READ): Get the ID from the previous step.
    trajectory_id = data_create["id"]

    # 5. ACT (READ): Send a GET request to the retrieval endpoint for that ID.
    response_read = client.get(f"/api/v1/trajectories/{trajectory_id}")

    # 6. ASSERT (READ): Check that the retrieval was successful.
    assert response_read.status_code == 200, "Status code for retrieval should be 200 OK."
    assert response_read.elapsed.total_seconds() < 0.5, "Retrieval response time should be under 0.5 seconds."
    
    # Check that the data we got back is the same as what we created.
    data_read = response_read.json()
    assert data_read["id"] == trajectory_id
    assert data_read["obstacles"][0]["dimensions"]["height"] == 2


def test_get_nonexistent_trajectory():
    """
    Test the failure case: requesting a trajectory that doesn't exist.
    The API should correctly return a 404 Not Found error.
    """
    # ACT: Request an ID that is highly unlikely to exist.
    response = client.get("/api/v1/trajectories/99999")

    # ASSERT: Check for the 404 error and the correct detail message.
    assert response.status_code == 404, "Status code for a non-existent ID should be 404."
    assert response.json() == {"detail": "Trajectory not found"}