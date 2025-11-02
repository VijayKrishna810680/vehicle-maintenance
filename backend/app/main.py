from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from . import models, schemas, crud
from .database import engine, SessionLocal, Base
from .agent import run  # ✅ FIXED — import the 'run' function, not 'agent'

# ✅ Create tables
Base.metadata.create_all(bind=engine)

# ✅ Initialize FastAPI
app = FastAPI(title="Vehicle Maintenance Records API")

# ✅ Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://vehicle-maintenance-frontend.onrender.com",  # frontend Render URL
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "*"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Database Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ✅ Routes
@app.get("/")
def home():
    return {"message": "Welcome to Vehicle Maintenance API!", "status": "running ✅"}

@app.post("/vehicles/", response_model=schemas.VehicleOut)
def create_vehicle(vehicle: schemas.VehicleCreate, db: Session = Depends(get_db)):
    if crud.get_vehicle_by_vin(db, vehicle.vin):
        raise HTTPException(status_code=400, detail="VIN already exists")
    return crud.create_vehicle(db, vehicle)

@app.get("/vehicles/", response_model=list[schemas.VehicleOut])
def read_vehicles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.list_vehicles(db, skip, limit)

@app.get("/vehicles/{vehicle_id}", response_model=schemas.VehicleOut)
def read_vehicle(vehicle_id: int, db: Session = Depends(get_db)):
    v = crud.get_vehicle(db, vehicle_id)
    if not v:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return v

@app.put("/vehicles/{vehicle_id}", response_model=schemas.VehicleOut)
def update_vehicle(vehicle_id: int, vehicle_update: schemas.VehicleUpdate, db: Session = Depends(get_db)):
    updated = crud.update_vehicle(db, vehicle_id, vehicle_update.dict(exclude_unset=True))
    if not updated:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return updated

@app.delete("/vehicles/{vehicle_id}")
def delete_vehicle(vehicle_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_vehicle(db, vehicle_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return {"ok": True}

# ✅ AI Chat Endpoint
class ChatRequest(BaseModel):
    message: str
    use_memory: bool = True

@app.post("/chat")
def chat_endpoint(req: ChatRequest):
    resp = run(req.message)  # ✅ FIXED — call the 'run' function directly
    return {"response": resp}
