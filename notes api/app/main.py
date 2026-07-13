from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os

# Import our database, models, and routers
from .database import engine
from . import models
from .routers import notes, auth

# Create all tables in the database.
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Notes API with Auth",
    description="A simple, modular API for managing notes, designed for learning FastAPI.",
    version="1.0.0"
)

# Include routers
app.include_router(auth.router)
app.include_router(notes.router)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse(
        request=request, name="index.html"
    )
