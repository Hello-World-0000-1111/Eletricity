import datetime
from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime, MetaData, Table
from sqlalchemy.orm import declarative_base, sessionmaker

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# PostgreSQL Connection settings
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "electricity_db")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

try:
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()
except Exception as e:
    engine = None
    SessionLocal = None
    Base = None
    print(f"Failed to connect to database: {e}")

class PredictionHistory(Base if Base else object):
    __tablename__ = "prediction_history"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    city = Column(Integer)
    temperature_c = Column(Float)
    humidity_percent = Column(Float)
    household_size = Column(Integer)
    income_level = Column(Integer)
    power_outage_hours = Column(Float)
    predicted_electricity_kwh = Column(Float)
    model_used = Column(String(50))

def init_db():
    if engine and Base:
        try:
            Base.metadata.create_all(bind=engine)
        except Exception as e:
            print(f"Warning: Database initialization encountered an error (this is often safe to ignore if tables already exist): {e}")


def get_db_session():
    if not SessionLocal:
        return None
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()

def log_prediction(data_dict, prediction, model_name="XGBoost"):
    if not SessionLocal:
        return False
    db = SessionLocal()
    try:
        record = PredictionHistory(
            city=data_dict.get("city", 0),
            temperature_c=data_dict.get("temperature_c", 0.0),
            humidity_percent=data_dict.get("humidity_percent", 0.0),
            household_size=data_dict.get("household_size", 0),
            income_level=data_dict.get("income_level", 0),
            power_outage_hours=data_dict.get("power_outage_hours", 0.0),
            predicted_electricity_kwh=prediction,
            model_used=model_name
        )
        db.add(record)
        db.commit()
        return True
    except Exception as e:
        print(f"Error logging prediction: {e}")
        return False
    finally:
        db.close()

def get_prediction_history(limit=100):
    if not SessionLocal:
        return []
    db = SessionLocal()
    try:
        records = db.query(PredictionHistory).order_by(PredictionHistory.timestamp.desc()).limit(limit).all()
        return records
    except Exception as e:
        print(f"Error fetching history: {e}")
        return []
    finally:
        db.close()
