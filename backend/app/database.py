from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/vehicle_db")

# Handle Docker internal networking
if "db:5432" in DATABASE_URL:
    engine = create_engine(DATABASE_URL, future=True)
else:
    # For local development, add connection pool settings
    engine = create_engine(
        DATABASE_URL, 
        future=True,
        pool_pre_ping=True,
        pool_recycle=3600
    )

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()
