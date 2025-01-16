# Libs
from sqlalchemy.orm import sessionmaker
from core.db.connection import engine


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()
