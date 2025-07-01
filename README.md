# Autonomous Wall Finishing Robot - Control System

This project is a complete full-stack control system for a conceptual autonomous wall-finishing robot. It features a robust FastAPI backend for intelligent path planning and a sleek, modern frontend for user interaction and live visualization. The system is designed to calculate an optimal path for a robot to cover a rectangular wall while intelligently navigating around user-defined obstacles.



---

## Overview

The core of this application is a "database-driven control system." A user can define the dimensions of a wall, the size and position of an obstacle (like a window), and the robot's tool width. The system then:

1.  **Calculates** an optimal, full-coverage trajectory using a "Zoned Painting" algorithm.
2.  **Stores** this trajectory in an SQLite database for persistence and retrieval.
3.  **Visualizes** the robot's path in real-time on a clean, intuitive web interface.

This project fulfills all requirements for a server-intensive, database-driven control system assignment, demonstrating proficiency in backend development, API design, frontend integration, and automated testing.

---

## Features

-   **Intelligent Path Planning:** Implements a "Zoned Painting" algorithm that divides the wall into logical sections around obstacles to ensure 100% coverage of all reachable areas.
-   **Dynamic Configuration:** Users can fully customize the dimensions of the wall, obstacle, and the robot's tool width through the UI.
-   **Full-Stack Architecture:** A clear separation of concerns with a FastAPI backend and a Vanilla JavaScript frontend.
-   **Database Persistence:** All generated trajectories are saved to an SQLite database, complete with a unique ID.
-   **RESTful API:** A well-defined API for creating and retrieving trajectory data.
    -   `POST /api/v1/trajectories/`: Creates and stores a new path.
    -   `GET /api/v1/trajectories/{id}`: Retrieves a previously stored path.
-   **Live Visualization:** A real-time "painting" animation on an HTML Canvas provides clear visual feedback of the robot's path.
-   **Automated API Testing:** Includes a suite of tests written with `pytest` to ensure API reliability and correctness.

---

## Tech Stack

-   **Backend:** Python, FastAPI, Uvicorn
-   **Database:** SQLite
-   **ORM:** SQLAlchemy
-   **Data Validation:** Pydantic
-   **Frontend:** HTML5, CSS3, Vanilla JavaScript (ES6+)
-   **Testing:** Pytest, FastAPI TestClient

---

## ⚙️ How to Use

To run this project on your local machine, follow these steps.

### Prerequisites

-   Python 3.10+
-   A virtual environment tool (like `venv`)

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```
### 2. Set Up the Python Virtual Environment

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate

On Windows:
python -m venv venv
.\venv\Scripts\activate
```
### 3. Install Dependencies
Install all the required Python packages from the requirements.txt file.
```bash
pip install -r requirements.txt
```

### 4. Run the Application
Start the FastAPI server using Uvicorn. The --reload flag enables hot-reloading for development.
```bash
uvicorn app.main:app --reload
```

### 5. Access the Web Interface
Open your web browser and navigate to:
```bash
http://127.0.0.1:8000
```

### 6. Run the Tests (Optional)
To verify that the API is working correctly, you can run the automated tests. Open a new terminal, activate the virtual environment, and run:
```bash
pytest
```


##Future Advancements:
- Multiple Obstacle Support: Upgrade the path planning algorithm to handle a list of multiple, potentially overlapping obstacles.
- Advanced Input Validation: Implement more robust validation (e.g., using Pydantic custom validators) to handle edge cases, such as an obstacle being larger than or outside the wall.
- Containerization: Create a Dockerfile to containerize the application with Docker, making it completely portable and easy to deploy.
- Database Migrations: Integrate a tool like Alembic to manage database schema changes gracefully without needing to delete the database.
- Asynchronous Operations: For even more complex path planning, the calculation could be moved to a background worker (like Celery) to prevent blocking the API for long-running tasks.
