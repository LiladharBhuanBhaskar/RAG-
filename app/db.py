from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from app.models import Base

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///data/rag.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {})
SessionLocal = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_session():
    return SessionLocal()

# for main startup
def init_db_if_needed():
    init_db()
