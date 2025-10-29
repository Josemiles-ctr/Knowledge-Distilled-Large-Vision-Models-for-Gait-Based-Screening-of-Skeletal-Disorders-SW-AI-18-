from fastapi import FastAPI
from app.routes import predict

app = FastAPI(title="GAITLAB Multimodal Gait Classifier")

# Include prediction routes
app.include_router(predict.router)
