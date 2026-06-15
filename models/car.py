from pydantic import BaseModel
from typing import List, Optional

class CarBase(BaseModel):
    make: str
    model: str
    year: int
    issue: str
    mechanic_id: int

class CarCreate(CarBase):
    pass

class CarResponse(CarBase):
    id: int

class Car(CarBase):
    id: int
