from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.campaign import Campaign, EmailRecord
from app.schemas.campaign import CampaignCreate, CampaignResponse, EmailRecordResponse, EmailRecordUpdate
from app.worker import process_campaign
from typing import List

router = APIRouter(prefix="/api/campaign", tags=["Campaign"])

@router.post("/start", response_model=CampaignResponse)
def create_campaign(payload: CampaignCreate, db: Session = Depends(get_db)):
    """
    Receives parsed CSV data and a prompt, saves it to the database, 
    and (in the future) triggers the background Celery worker.
    """
    # 1. Create the parent Campaign record
    new_campaign = Campaign(
        name=payload.name,
        prompt_template=payload.prompt_template,
        status="processing"
    )
    db.add(new_campaign)
    db.commit()
    db.refresh(new_campaign) # Get the generated auto-increment ID

    # 2. Create the child EmailRecord entries for each recipient
    email_records = []
    for rec in payload.recipients:
        # Convert keys to lowercase for flexible matching
        lowercase_rec = {k.lower(): v for k, v in rec.items()}
        
        # Try to find email
        email_val = lowercase_rec.get("email") or lowercase_rec.get("email address") or ""
        
        # Try to find name
        name_val = lowercase_rec.get("name") or lowercase_rec.get("first name") or ""
        
        record = EmailRecord(
            campaign_id=new_campaign.id,
            recipient_email=str(email_val),
            recipient_name=str(name_val),
            status="pending"
        )
        email_records.append(record)
    
    # Bulk insert for performance
    db.add_all(email_records)
    db.commit()

    # 3. Trigger the Celery worker to process this in the background!
    # The .delay() method pushes the job to Redis without making the user wait.
    process_campaign.delay(new_campaign.id)

    return {
        "id": new_campaign.id,
        "name": new_campaign.name,
        "status": new_campaign.status,
        "total_recipients": len(email_records),
        "message": "Campaign saved to database and background worker started!"
    }

@router.get("/{campaign_id}/emails", response_model=List[EmailRecordResponse])
def get_campaign_emails(campaign_id: int, db: Session = Depends(get_db)):
    """Fetch all email drafts for a specific campaign"""
    emails = db.query(EmailRecord).filter(EmailRecord.campaign_id == campaign_id).all()
    return emails

@router.put("/emails/{email_id}", response_model=EmailRecordResponse)
def update_email_record(email_id: int, payload: EmailRecordUpdate, db: Session = Depends(get_db)):
    """Update the generated content and/or status of an email draft"""
    email_record = db.query(EmailRecord).filter(EmailRecord.id == email_id).first()
    if not email_record:
        raise HTTPException(status_code=404, detail="Email record not found")
    
    if payload.generated_content is not None:
        email_record.generated_content = payload.generated_content
    if payload.status is not None:
        email_record.status = payload.status
        
    db.commit()
    db.refresh(email_record)
    
    return email_record

from app.services.email_sender import SMTPSender

@router.post("/emails/{email_id}/send")
def send_individual_email(email_id: int, db: Session = Depends(get_db)):
    """Send an approved email draft via SMTP"""
    email_record = db.query(EmailRecord).filter(EmailRecord.id == email_id).first()
    if not email_record:
        raise HTTPException(status_code=404, detail="Email record not found")
        
    if email_record.status != "approved":
        raise HTTPException(status_code=400, detail="Only approved emails can be sent")
        
    try:
        sender = SMTPSender()
        subject = f"Connecting with {email_record.recipient_name}"
        
        # We need to extract the subject from the generated content if possible.
        # But for now, we'll use a generic subject if it's not clearly defined.
        content = email_record.generated_content
        if "subject:" in content.lower():
            # Try to parse out the subject
            lines = content.split('\n')
            for line in lines:
                if line.lower().startswith('subject:'):
                    subject = line[8:].strip()
                    break
                    
        sender.send_email(
            to_email=email_record.recipient_email,
            subject=subject,
            body_text=content
        )
        
        email_record.status = "sent"
        db.commit()
        
        return {"message": "Email sent successfully", "status": "sent"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
