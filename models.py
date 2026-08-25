from sqlalchemy import create_engine, Column, Integer, String, Text, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
    created_at = Column(DateTime, default=datetime.now)

class WrongNote(Base):
    __tablename__ = 'wrong_notes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    question_text = Column(Text, nullable=False)
    standard_answer = Column(Text, nullable=True)
    error_analysis = Column(Text, nullable=True)
    knowledge_points = Column(String(200), nullable=True)
    tags = Column(String(200), nullable=True)
    original_image = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    mastery_level = Column(String(20), default='未掌握')

    user = relationship("User", back_populates="notes")

User.notes = relationship("WrongNote", order_by=WrongNote.id, back_populates="user")
import os
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

def init_db():
    Base.metadata.create_all(bind=engine)
