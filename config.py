import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get OpenRouter API key from environment variables
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
if not OPENROUTER_API_KEY:
    raise ValueError("Please set OPENROUTER_API_KEY in .env file")

# URL references for OpenRouter
REFERER_URL = os.getenv("REFERER_URL", "http://localhost")
SITE_NAME = os.getenv("SITE_NAME", "Markdown Conversion Test")