# OCR Webapp

A simple Optical Character Recognition (OCR) application built with FastAPI and Streamlit. It extracts text from uploaded images using the OCR.Space API.

App Link: https://opticalcharacterrecognition.streamlit.app

## Architecture

* Backend: FastAPI
* Frontend: Streamlit
* OCR Engine: OCR.Space API

## Project Structure

* `backend/main.py`: FastAPI server entry point.
* `backend/api/routes.py`: API endpoint for image uploads.
* `backend/services/ocr_engine.py`: OCR.Space API integration.
* `backend/core/config.py`: Configuration loading.
* `frontend/app.py`: Streamlit UI.

## Local Setup

1. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Add your OCR.Space API key to a `.env` file at the root:
   ```text
   OCR_API_KEY=your_key_here
   ```

## Running Locally

Start the backend server:
```bash
uvicorn backend.main:app --reload
```

Start the frontend UI:
```bash
streamlit run frontend/app.py
```
