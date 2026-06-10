from pydantic import BaseModel
from typing import List, Optional

class CarBase(BaseModel):
    title: str
    author_id: int
    book_link: str
    genres: List[str]  # List of genre names
    average_rating: Optional[float] = None
    published_year: Optional[int] = None

class CarCreate(CarBase):
    pass

class CarResponse(CarBase):
    id: int

class Car(CarBase):
    id: int
