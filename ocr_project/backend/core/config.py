import os
from dotenv import load_dotenv

# This function automatically finds your .env file and loads the variables into the OS environment
load_dotenv()

# Securely grab the key from the environment. 
# If the .env file is missing or the key isn't there, we fallback to 'helloworld'.
OCR_API_KEY = os.getenv("OCR_API_KEY", "helloworld")
