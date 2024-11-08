from sqlalchemy import create_engine, Column, Integer, String, DateTime, JSON, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://nextjsgen:nextjsgen@localhost:5432/nextjsgen')

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(Text)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    project_path = Column(String)
    config = Column(JSON)  # Stores project configuration
    components = Column(JSON)  # Stores component metadata
    pages = Column(JSON)  # Stores page structure
    dependencies = Column(JSON)  # Stores project dependencies

def get_db_session():
    return SessionLocal()

def init_db():
    Base.metadata.create_all(bind=engine) 