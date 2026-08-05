#!/bin/bash

# Navigate to backend directory
cd backend

# 1. Start Celery worker in the background
echo "Starting Celery worker..."
celery -A app.worker.celery_app worker --loglevel=info &

# 2. Start FastAPI backend in the background on port 8000
echo "Starting FastAPI backend..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 &

# Wait a few seconds to ensure backend is up
sleep 3

# Navigate to frontend directory
cd ../frontend

# 3. Start Streamlit frontend in the foreground on Render's provided $PORT
echo "Starting Streamlit frontend..."
streamlit run app.py --server.port $PORT --server.address 0.0.0.0
