# app/main.py

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from . import api, database

# Create the database and tables if they don't exist
database.create_database_and_tables()

# Create the main FastAPI application instance
app = FastAPI(
    title="Autonomous Wall-Finishing Robot API",
    description="API for planning and storing robot trajectories.",
    version="2.0.0", # Bump version for new features!
)

# --- CORS Middleware (still important) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Include API Routers ---
# All our API logic lives behind this prefix
app.include_router(api.router, prefix="/api/v1", tags=["Trajectories"])

# --- Mount Static Files (The Frontend) ---
# This is the new, important part. It tells FastAPI to serve the 'frontend'
# directory at the root URL. The 'html=True' part makes it serve index.html
# for requests to '/'.
# THIS MUST BE THE LAST 'app.mount' or 'app.include_router' CALL
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")