import os
from celery import Celery
from app.core.database import SessionLocal
from app.models.campaign import Campaign, EmailRecord
from app.agent.email_graph import email_agent

# Initialize Celery using Redis as the message broker
broker_url = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
celery_app = Celery("email_worker", broker=broker_url, backend=broker_url)

@celery_app.task(name="process_campaign")
def process_campaign(campaign_id: int, groq_api_key: str):
    """
    Background worker task. 
    It reads pending records from the DB, runs the LangGraph AI to generate the email,
    and updates the database with the result.
    """
    db = SessionLocal()
    try:
        # Fetch the campaign details
        campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
        if not campaign:
            print(f"Campaign {campaign_id} not found!")
            return
            
        # Get all 'pending' email records for this campaign
        records = db.query(EmailRecord).filter(
            EmailRecord.campaign_id == campaign_id, 
            EmailRecord.status == "pending"
        ).all()
        
        print(f"Worker started processing {len(records)} emails for Campaign {campaign_id}...")
        
        for record in records:
            # 1. Update status
            record.status = "processing"
            db.commit()
            
            try:
                # 2. Feed the data into our LangGraph AI Agent!
                initial_state = {
                    "recipient_name": record.recipient_name,
                    "recipient_email": record.recipient_email,
                    "recipient_company": "Unknown", 
                    "recipient_role": "Unknown",
                    "custom_prompt": campaign.prompt_template,
                    "groq_api_key": groq_api_key,
                    "generated_draft": "",
                    "quality_approved": False
                }
                
                # Execute the StateGraph
                final_state = email_agent.invoke(initial_state)
                
                # Save the AI-generated draft
                record.generated_content = final_state.get("generated_draft", "Failed to generate.")
                record.status = "generated"
                print(f"Successfully generated email for {record.recipient_name}")
                
                # (Future Step: Add SMTP logic right here to actually send the email)
                
            except Exception as e:
                record.status = "failed"
                record.generated_content = f"Error: {str(e)}"
                print(f"Failed generating email for {record.recipient_name}: {e}")
            
            db.commit()
            
        # Mark campaign as finished
        campaign.status = "completed"
        db.commit()
        print(f"Campaign {campaign_id} processing complete!")
        
    finally:
        db.close()
