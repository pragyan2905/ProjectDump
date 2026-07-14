from fastapi import APIRouter, UploadFile, File
from backend.services.ocr_engine import extract_text_from_image

# APIRouter allows us to split our API into multiple files (modularity!)
router = APIRouter()

@router.post("/extract-text")
async def extract_text(file: UploadFile = File(...)):
    """
    Endpoint that accepts an image file upload and returns the extracted text.
    """
    # 1. Read the uploaded image into memory as raw bytes
    image_bytes = await file.read()
    
    # 2. Pass the bytes, filename, and type to our OCR engine logic
    text = extract_text_from_image(image_bytes, file.filename, file.content_type)
    
    # 3. Return the final text to the user
    return {
        "filename": file.filename,
        "extracted_text": text
    }
