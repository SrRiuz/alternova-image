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

# Pagination config
PAGINATION = {"PAGE_LIMIT": 12}

SHORT_ID_SIZE = 8

# Cors
ALLOWER_CORS_ORIGINS = (
    "http://localhost",
    "http://localhost:8000",
)
