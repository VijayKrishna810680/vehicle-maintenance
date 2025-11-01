from sqlalchemy.orm import Session
from . import models, schemas

def get_vehicle(db: Session, vehicle_id: int):
    return db.query(models.Vehicle).filter(models.Vehicle.id == vehicle_id).first()

def get_vehicle_by_vin(db: Session, vin: str):
    return db.query(models.Vehicle).filter(models.Vehicle.vin == vin).first()

def list_vehicles(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Vehicle).offset(skip).limit(limit).all()

def create_vehicle(db: Session, v: schemas.VehicleCreate):
    db_obj = models.Vehicle(**v.dict())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def update_vehicle(db: Session, vehicle_id: int, changes: dict):
    obj = get_vehicle(db, vehicle_id)
    if not obj:
        return None
    for k,v in changes.items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj

def delete_vehicle(db: Session, vehicle_id: int):
    obj = get_vehicle(db, vehicle_id)
    if not obj:
        return None
    db.delete(obj)
    db.commit()
    return obj
