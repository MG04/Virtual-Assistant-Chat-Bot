import os
from pathlib import Path

# Load .env if python-dotenv is installed
try:
    from dotenv import load_dotenv
    # Look for .env in current working directory and project root
    env_path = Path(__file__).resolve().parent.parent / '.env'
    if env_path.exists():
        load_dotenv(dotenv_path=env_path)
    else:
        load_dotenv()
except ImportError:
    pass

# Assistant Persona
USERNAME = os.getenv("ASSISTANT_USERNAME", "User")
BOT_NAME = os.getenv("ASSISTANT_BOT_NAME", "Assistant")

# UI Theme Configuration
BG_GRAY = "#ABB2B9"
BG_COLOR = "#17202A"
TEXT_COLOR = "#EAECEE"
ENTRY_BG = "#2C3E50"
FONT = ("Helvetica", 14)
FONT_BOLD = ("Helvetica", 13, "bold")

# API Keys and External Credentials
NEWS_API_KEY = os.getenv("NEWS_API_KEY", "")
OPENWEATHER_APP_ID = os.getenv("OPENWEATHER_APP_ID", "")
NEWS_COUNTRY = os.getenv("NEWS_COUNTRY", "us")

# Email (SMTP) Configuration
EMAIL_ADDRESS = os.getenv("GMAIL_ADDRESS", os.getenv("EMAIL_ADDRESS", ""))
EMAIL_PASSWORD = os.getenv("GMAIL_APP_PASSWORD", os.getenv("EMAIL_PASSWORD", ""))
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))


def has_email_credentials() -> bool:
    return bool(EMAIL_ADDRESS and EMAIL_PASSWORD)


def has_weather_credentials() -> bool:
    return bool(OPENWEATHER_APP_ID)


def has_news_credentials() -> bool:
    return bool(NEWS_API_KEY)
