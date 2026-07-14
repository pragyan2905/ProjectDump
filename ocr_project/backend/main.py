from fastapi import FastAPI
from backend.api.routes import router as api_router

# Initialize the FastAPI application
app = FastAPI(
    title="OCR API",
    description="A simple OCR API using a free Cloud service and FastAPI",
    version="1.0.0"
)

# Connect our modular routes to the main app
app.include_router(api_router, prefix="/api")

# Define a root endpoint to check if the API is alive
@app.get("/")
def read_root():
    return {"status": "success", "message": "OCR API is alive and kicking!"}
