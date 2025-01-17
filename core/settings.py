# Python
import os

DEBUG = os.environ["DEBUG"]
SECRET_KEY = "..."

# Database configuration
USE_DATABASE = os.environ["USE_DATABASE"]

DATABASE = (
    {
        "ENGINE": "postgresql",  # postgresql or sqlite
        "NAME": os.environ["DATABASE_NAME"],
        # Only for postgresql database
        "USER": os.environ["DATABASE_USER"],
        "PASSWORD": os.environ["DATABASE_PASSWORD"],
        "HOST": os.environ["DATABASE_HOST"],
        "PORT": os.environ["DATABASE_PORT"],
    }
    if USE_DATABASE
    else {}
)

# Storage
LOCAL_STORAGE_DIR = "storage"

# Pagination config
PAGINATION = {"PAGE_LIMIT": 12}

SHORT_ID_SIZE = 8

# Media
MEDIA_PATH = "v1/images/media"
BASE_MEDIA_BACKEND_URL = "http://localhost:9090"
MEDIA_URL = f"{BASE_MEDIA_BACKEND_URL}/{MEDIA_PATH}"

# Cors
ALLOWER_CORS_ORIGINS = (
    "http://localhost",
    "http://localhost:8000",
)
