"""
GaitLab FastAPI Application
Clinical video gait analysis server with model inference and clinical embeddings.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router
from app.config import CORS_ORIGINS, CORS_METHODS, CORS_HEADERS

app = FastAPI(
    title="GaitLab - Clinical Gait Analysis API",
    description="FastAPI server for video-based gait analysis using deep learning models",
    version="1.0.0",
    docs_url="/docs",
    openapi_url="/openapi.json"
)

# Configure CORS using environment variables
# Read from CORS_ORIGINS env var (comma-separated) or defaults to localhost:5173 and localhost:3000
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=CORS_METHODS,
    allow_headers=CORS_HEADERS,
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