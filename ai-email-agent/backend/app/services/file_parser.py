import io
import pandas as pd
from fastapi import HTTPException, UploadFile

def parse_uploaded_file(file: UploadFile) -> dict:
    """
    Reads an uploaded CSV or XLSX file and converts it into structured JSON-compatible data.
    
    Technical Details:
    - BytesIO is used to read file streams in-memory without saving temporary files to disk.
    - pandas parses CSV/Excel data into a DataFrame.
    """
    filename = file.filename.lower()
    content = file.file.read()

    try:
        # Load in-memory bytes into io.BytesIO stream
        file_stream = io.BytesIO(content)

        if filename.endswith(".csv"):
            df = pd.read_csv(file_stream)
        elif filename.endswith((".xlsx", ".xls")):
            df = pd.read_excel(file_stream)
        else:
            raise HTTPException(
                status_code=400,
                detail="Unsupported file format. Please upload a .csv or .xlsx file."
            )

        # Sanitize column names (strip whitespace, convert to lower/clean strings)
        df.columns = [str(col).strip() for col in df.columns]

        # Replace NaN/null values with empty string for JSON serialization
        df = df.fillna("")

        # Extract recipient data
        records = df.to_dict(orient="records")
        columns = list(df.columns)

        return {
            "filename": file.filename,
            "total_rows": len(df),
            "columns": columns,
            "data_preview": records[:5],  # First 5 rows preview
            "records": records          # Full dataset
        }

    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=500,
            detail=f"Failed to parse file '{file.filename}': {str(e)}"
        )
