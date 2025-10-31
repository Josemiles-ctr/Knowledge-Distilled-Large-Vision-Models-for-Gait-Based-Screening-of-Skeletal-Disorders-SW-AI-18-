"""
GaitLab FastAPI Application
Clinical video gait analysis server with model inference and clinical embeddings.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router

app = FastAPI(
    title="GaitLab - Clinical Gait Analysis API",
    description="FastAPI server for video-based gait analysis using deep learning models",
    version="1.0.0",
    docs_url="/docs",
    openapi_url="/openapi.json"
)

# Configure CORS for broader compatibility
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Include API routes (health, ready, predict, conditions)
app.include_router(router)

@app.get("/")
async def root():
    """Root endpoint returning API information."""
    return {
        "message": "GaitLab API is running!",
        "docs": "/docs",
        "version": "1.0.0"
    }