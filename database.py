from sqlalchemy import Column, DateTime, Float, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

DATABASE_URL = "sqlite:///./resumes.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Analysis(Base):
  __tablename__ = "analyses"

  id = Column(Integer, primary_key=True, index=True)
  job_description = Column(String)
  skill_score = Column(Integer)
  semantic_score = Column(Float)
  final_score = Column(Integer)
  created_at = Column(DateTime, default=datetime.datetime.utcnow)


# Create the database tables
Base.metadata.create_all(bind=engine)
