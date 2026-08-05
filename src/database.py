import datetime
from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime, MetaData, Table, text
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
SQLITE_URL = "sqlite:///db/electricity.db"

engine = None
SessionLocal = None
Base = declarative_base()
_is_sqlite = False

class PredictionHistory(Base):
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
    global engine, SessionLocal, _is_sqlite
    
    # Try PostgreSQL first
    try:
        # Use a short connect timeout so we don't hang if database is offline
        temp_engine = create_engine(DATABASE_URL, connect_args={"connect_timeout": 3})
        # Test the connection immediately
        with temp_engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        
        engine = temp_engine
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        Base.metadata.create_all(bind=engine)
        _is_sqlite = False
        print("Successfully connected to PostgreSQL database.")
        return
    except Exception as e:
        print(f"PostgreSQL connection failed: {e}. Falling back to SQLite...")
        
    # Fallback to SQLite
    try:
        os.makedirs("db", exist_ok=True)
        engine = create_engine(SQLITE_URL, connect_args={"check_same_thread": False})
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        Base.metadata.create_all(bind=engine)
        _is_sqlite = True
        print("Successfully initialized and connected to SQLite fallback database.")
    except Exception as sq_err:
        print(f"Failed to initialize SQLite fallback database: {sq_err}")
        engine = None
        SessionLocal = None

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

def check_db_connection():
    if not SessionLocal:
        return False
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        return True
    except Exception:
        return False
    finally:
        if 'db' in locals():
            db.close()

def is_sqlite_fallback():
    return _is_sqlite


