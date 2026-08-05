import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

class SMTPSender:
    def __init__(self):
        self.server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.port = int(os.getenv("SMTP_PORT", 587))
        self.username = os.getenv("SMTP_USERNAME")
        self.password = os.getenv("SMTP_PASSWORD")

    def send_email(self, to_email: str, subject: str, body_text: str):
        if not self.username or not self.password:
            raise ValueError("SMTP credentials are not configured in .env file")
            
        msg = EmailMessage()
        msg.set_content(body_text)
        msg['Subject'] = subject
        msg['From'] = self.username
        msg['To'] = to_email

        # Connect to the SMTP server and send
        try:
            with smtplib.SMTP(self.server, self.port) as server:
                server.starttls() # Secure the connection
                server.login(self.username, self.password)
                server.send_message(msg)
            return True
        except Exception as e:
            print(f"Failed to send email to {to_email}: {e}")
            raise e
