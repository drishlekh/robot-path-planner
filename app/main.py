

# app/main.py

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from . import api, models
from .database import engine


models.Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Autonomous Wall-Finishing Robot API",
    description="API for planning and storing robot trajectories.",
    version="3.0.0",
)

# --- CORS Middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Including API Routers ---
app.include_router(api.router, prefix="/api/v1", tags=["Trajectories"])

# The Frontend
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")