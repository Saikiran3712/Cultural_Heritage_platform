import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # API Configuration
    API_BASE_URL = os.getenv("API_BASE_URL", "https://api.corpus.swecha.org")
    API_KEY = os.getenv("SWECHA_API_KEY")
    
    # App Configuration
    APP_NAME = os.getenv("APP_NAME", "మన ఆటలు - Mana Aatalu")
    APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    
    # File Upload Configuration
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif', 'mp4', 'mov', 'avi', 'mp3', 'wav', 'pdf']
    
    # Pagination
    DEFAULT_PAGE_SIZE = 20
    MAX_PAGE_SIZE = 100
    
    # Regional Configuration
    INDIAN_STATES = [
        "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh",
        "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand", "Karnataka",
        "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya", "Mizoram",
        "Nagaland", "Odisha", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu",
        "Telangana", "Tripura", "Uttar Pradesh", "Uttarakhand", "West Bengal"
    ]
    
    # Game Categories
    GAME_CATEGORIES = [
        "Outdoor Games", "Indoor Games", "Group Games", "Solo Games",
        "Water Games", "Festival Games", "Seasonal Games", "Board Games",
        "Running Games", "Strategy Games", "Traditional Sports"
    ]
    
    # Age Groups
    AGE_GROUPS = ["3-6 years", "7-12 years", "13-18 years", "18+ years", "All ages"]

settings = Settings()