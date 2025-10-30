from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router
from app.config import settings

app = FastAPI(
    title="Clinical Video Gait API",
    description="API for gait analysis using clinical video processing",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=settings.CORS_METHODS,
    allow_headers=settings.CORS_HEADERS,
    expose_headers=["Content-Type"]
)

app.include_router(router)

@app.get("/")
async def root():
    return {"message": "Clinical Gait API is running!"}