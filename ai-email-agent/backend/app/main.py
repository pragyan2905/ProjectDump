from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.parser_routes import router as parser_router
from app.api.campaign_routes import router as campaign_router
from app.core.database import engine, Base
import app.models.campaign as campaign_models

# Tell SQLAlchemy to physically create tables in the database if they don't exist
Base.metadata.create_all(bind=engine)

# Initialize the FastAPI app
app = FastAPI(
    title="AI Bulk Email Agent API",
    description="Backend API for managing AI-driven bulk email campaigns.",
    version="1.0.0"
)

# Configure CORS (Cross-Origin Resource Sharing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register modular routes
app.include_router(parser_router)
app.include_router(campaign_router)

# Root Endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the AI Email Agent Backend"}

# Health check endpoint
@app.get("/api/health")
def health_check():
    return {"status": "healthy", "service": "AI Email Agent"}
