import sqlite3
from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
from models.mechanic import Mechanic, MechanicCreate
from database import get_db_connection

router = APIRouter()


@router.get("/", response_model=List[Mechanic])
def get_mechanics():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM mechanics")
    mechanics = cursor.fetchall()
    conn.close()
    return [{"id": mechanic[0], "name": mechanic[1]} for mechanic in mechanics]


@router.post("/", response_model=Mechanic)
def create_mechanic(mechanic: MechanicCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO mechanics (name) VALUES (?)", (mechanic.name,))
        conn.commit()
        mechanic_id = cursor.lastrowid
        return Mechanic(id=mechanic_id, name=mechanic.name)
    except sqlite3.IntegrityError:
        conn.close()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"The mechanic '{mechanic.name}' already exists."
        )
    finally:
        conn.close()


@router.put("/{mechanic_id}", response_model=Mechanic)
def update_author(mechanic_id: int,mechanic: MechanicCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE mechanics SET name = ? WHERE id = ?", (mechanic.name, author_id))
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Mechanic not found")
    conn.commit()
    conn.close()
    return Mechanic(id=mechanic_id, name=mechanic.name)


@router.delete("/{mechanic_id}", response_model=dict)
def delete_mechanic(mechanic_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM mechanics WHERE id = ?", (mechanic_id,))
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Mechanic not found")
    conn.commit()
    conn.close()

    return {"detail": "Mechanic deleted"}

