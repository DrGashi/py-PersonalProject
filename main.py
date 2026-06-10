from fastapi import FastAPI
from routers import mechanics, cars
from database import create_database

app = FastAPI(
    title="Mechanic Management System",
    description="An API for managing mechanics and cars.",
    version="1.0.0",
)

app.include_router(mechanics.router, prefix="/api/mechanics", tags=["Mechanics"])
app.include_router(cars.router, prefix="/api/cars", tags=["Cars"])

@app.on_event("startup")
def startup():
    create_database()