from fastapi import FastAPI
from api import routes  # API endpoints

app = FastAPI(title="Clinical Video Gait API")

# Include API router
app.include_router(routes.router)

@app.get("/")
async def root():
    return {"message": "Clinical Gait API is running!"}
