import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

class SMTPSender:
    def __init__(self, smtp_user: str, smtp_password: str):
        self.server = "smtp.gmail.com"
        self.port = 587
        self.username = smtp_user
        self.password = smtp_password

    def send_email(self, to_email: str, subject: str, body_text: str):
        if not self.username or not self.password:
            raise ValueError("SMTP credentials were not provided")
            
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
