from pydantic import BaseModel
from typing import Optional

class VehicleBase(BaseModel):
    vin: str
    make: Optional[str] = None
    model: Optional[str] = None
    year: Optional[int] = None
    owner: Optional[str] = None

class VehicleCreate(VehicleBase):
    pass

class VehicleUpdate(BaseModel):
    make: Optional[str]
    model: Optional[str]
    year: Optional[int]
    owner: Optional[str]

class VehicleOut(VehicleBase):
    id: int
    class Config:
        orm_mode = True
