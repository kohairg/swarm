from sqlalchemy import create_engine, Column, Integer, String, JSON, DateTime, Text, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

# Create SQLAlchemy base class
Base = declarative_base()

class Document(Base):
    __tablename__ = 'documents'

    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    doc_metadata = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    embedding = Column(JSON, nullable=True)  # Store embeddings if needed later
    url = Column(String, nullable=True)
    title = Column(String, nullable=True)
    description = Column(Text, nullable=True)

def get_db_session():
    """Create a database session"""
    DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://docgen:docgen@localhost:5432/docgen')
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session() 