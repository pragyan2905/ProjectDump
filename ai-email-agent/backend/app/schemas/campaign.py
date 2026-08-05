from pydantic import BaseModel, EmailStr
from typing import List, Optional

class RecipientInput(BaseModel):
    name: str
    email: EmailStr
    # We can capture any extra columns dynamically if we want, 
    # but for now we'll stick to a strict schema for simplicity.

class CampaignCreate(BaseModel):
    name: str
    prompt_template: str
    recipients: List[dict] # Accepting a list of dicts from the parsed CSV
    groq_api_key: str

class EmailSendRequest(BaseModel):
    smtp_email: str
    smtp_password: str

class CampaignResponse(BaseModel):
    id: int
    name: str
    status: str
    total_recipients: int
    message: str

class EmailRecordResponse(BaseModel):
    id: int
    campaign_id: int
    recipient_email: str
    recipient_name: str
    generated_content: Optional[str] = None
    status: str

    class Config:
        from_attributes = True

class EmailRecordUpdate(BaseModel):
    generated_content: Optional[str] = None
    status: Optional[str] = None
