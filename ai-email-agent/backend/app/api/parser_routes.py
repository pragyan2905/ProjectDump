from fastapi import APIRouter, File, UploadFile
from app.services.file_parser import parse_uploaded_file

router = APIRouter(prefix="/api", tags=["File Parser"])

@router.post("/parse-file")
async def parse_file(file: UploadFile = File(...)):
    """
    Endpoint to upload a CSV or XLSX file.
    Uses pandas via our file_parser service to read in-memory byte streams and return structured JSON.
    """
    parsed_data = parse_uploaded_file(file)
    return {
        "status": "success",
        "filename": parsed_data["filename"],
        "total_rows": parsed_data["total_rows"],
        "columns": parsed_data["columns"],
        "preview": parsed_data["data_preview"],
        "records": parsed_data["records"]
    }
