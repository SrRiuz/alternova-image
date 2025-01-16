# Libs
from sqlalchemy import create_engine
from core.db.utils import get_db_uri

DATABASE_URI = get_db_uri()
engine = None

if DATABASE_URI:
    engine = create_engine(DATABASE_URI)
