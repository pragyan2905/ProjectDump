import requests
from backend.core.config import OCR_API_KEY

# We use the public free test key 'helloworld' for OCR.Space
OCR_API_URL = "https://api.ocr.space/parse/image"

def extract_text_from_image(image_bytes: bytes, filename: str, content_type: str) -> str:
    """
    Sends the image bytes to OCR.Space API and returns the extracted text.
    """
    # The API requires our key and the language we expect to read
    payload = {
        'apikey': OCR_API_KEY,
        'language': 'eng',
    }
    # We bundle the raw bytes into a file-like object using the real filename and type!
    files = {
        'file': (filename, image_bytes, content_type)
    }
    
    # Make the HTTP POST request to the cloud API
    response = requests.post(OCR_API_URL, data=payload, files=files)
    result = response.json()
    
    # Navigate the JSON response to grab just the text
    if not result.get("IsErroredOnProcessing"):
        parsed_results = result.get("ParsedResults", [])
        if parsed_results:
            text = parsed_results[0].get("ParsedText", "")
            if text:
                return text.strip()
            
    # If we get here, something failed. Let's return the raw JSON so we can debug!
    return f"Debug Info - Raw API Response: {result}"
