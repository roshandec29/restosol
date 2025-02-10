import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    EMAIL_HOST = os.getenv("EMAIL_HOST")
    EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))
    EMAIL_USERNAME = os.getenv("EMAIL_USERNAME")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

config = Config()
print(config.EMAIL_USERNAME)