from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime, timezone

SQLALCHEMY_DATABASE_URL = "sqlite:///./evaluations.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Log(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    user_query = Column(String)
    bot_response = Column(String)
    accuracy = Column(Integer)
    tone = Column(Integer)
    verdict = Column(String)
    errors = Column(String)
    average_score = Column(Float)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()