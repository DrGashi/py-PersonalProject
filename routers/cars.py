import sqlite3
from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
from models.car import Car, CarCreate
from database import get_db_connection

router = APIRouter()


@router.get("/", response_model=List[Car])
def get_books():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, make, model, year, issue FROM cars")
    cars = cursor.fetchall()
    conn.close()

    return [
        {
            "id": car[0],
            "make": car[1],
            "model": car[2],
            "year": car[3],
            "issue": car[4]
        }
        for car in cars
    ]


@router.post("/", response_model=Car)
def create_book(car: CarCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO cars (make, model, year, issue) "
                       "VALUES (?, ?, ?, ?)",
                       (car.make, car.model, car.year, car.issue))
        conn.commit()
        car_id = cursor.lastrowid
        return Car(id=car_id, **car.dict())
    except sqlite3.IntegrityError:
        conn.close()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"The car '{car.title}' already exists."
        )
    finally:
        conn.close()


@router.put("/{car_id}", response_model=Car)
def update_book(car_id: int, car: CarCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE cars SET make = ?, model = ?, year = ?, issue = ?"
        "WHERE id = ?",
        (car.make, car.model, car.year, car.issue, car_id))
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Book not found")
    conn.commit()
    conn.close()
    return Car(id=car_id, **car.dict())


@router.delete("/{car_id}", response_model=dict)
def delete_book(car_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM cars WHERE id = ?", (car_id,))
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Car not found")
    conn.commit()
    conn.close()
    return {"detail": "Car deleted"}
