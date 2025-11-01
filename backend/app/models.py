from sqlalchemy import Column, Integer, String
from .database import Base

class Vehicle(Base):
    __tablename__ = "vehicles"
    id = Column(Integer, primary_key=True, index=True)
    vin = Column(String(64), unique=True, index=True, nullable=False)
    make = Column(String(50))
    model = Column(String(50))
    year = Column(Integer)
    owner = Column(String(100))
