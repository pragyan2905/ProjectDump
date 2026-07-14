# OCR Webapp

This project is a modular, full-stack Optical Character Recognition (OCR) application built with FastAPI and Streamlit. It extracts text from uploaded images using a cloud OCR engine.

Streamlit App Link: [Insert Link Here]

## Architecture

* Backend: FastAPI (Python)
* Frontend: Streamlit (Python)
* OCR Engine: OCR.Space API

## Project Structure

* backend/main.py: Entry point for the FastAPI server.
* backend/api/routes.py: API endpoints for handling image uploads.
* backend/services/ocr_engine.py: Logic for communicating with the external OCR API.
* backend/core/config.py: Environment variable configuration and security.
* frontend/app.py: Streamlit user interface.

## Local Setup

1. Create a virtual environment and activate it:
   python3 -m venv venv
   source venv/bin/activate

2. Install dependencies:
   pip install -r requirements.txt

3. Add your OCR.Space API key to a .env file at the root:
   OCR_API_KEY=your_key_here

## Running the Application

Start the backend server (Terminal 1):
uvicorn backend.main:app --reload

Start the frontend UI (Terminal 2):
streamlit run frontend/app.py
