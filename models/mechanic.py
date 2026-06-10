from pydantic import BaseModel

class MechanicBase(BaseModel):
    name: str

class MechanicCreate(MechanicBase):
    pass

class MechanicResponse(BaseModel):
    id: int
    name: str

class Mechanic(MechanicBase):
    id: int
