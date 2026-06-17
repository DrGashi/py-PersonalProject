import streamlit as st
import requests
import pandas as pd
from datetime import datetime
# import plotly.express as px
from dotenv import load_dotenv
import os

load_dotenv()
BASE_URL = os.getenv('BASE_URL')

def get_mechanics():
    response = requests.get(f"{BASE_URL}/mechanics/")
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to fetch mechanics.")
        return []


def add_mechanic(name):
    response = requests.post(f"{BASE_URL}/mechanics/", json={"name": name})
    if response.status_code == 200:
        st.success(f"Mechanic '{name}' added successfully!")
    else:
        st.error(f"Failed to add mechanic: {response.json().get('detail', 'Unknown error')}")


def update_mechanic(mechanic_id, name):
    response = requests.put(f"{BASE_URL}/mechanics/{mechanic_id}", json={"name": name})
    if response.status_code == 200:
        st.success(f"Mechanic '{name}' updated successfully!")
    else:
        st.error(f"Failed to update author: {response.json().get('detail', 'Unknown error')}")


def delete_mechanic(mechanic_id):
    response = requests.delete(f"{BASE_URL}/mechanics/{mechanic_id}")
    if response.status_code == 200:
        st.success("Mechanic deleted successfully!")
    else:
        st.error(f"Failed to delete mechanic: {response.json().get('detail', 'Unknown error')}")


def get_cars():
    response = requests.get(f"{BASE_URL}/cars/")
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to fetch cars.")
        return []


def add_car(car_data):
    response = requests.post(f"{BASE_URL}/cars/", json=car_data)
    if response.status_code == 200:
        st.success(f"Car '{car_data['title']}' added successfully!")
    else:
        st.error(f"Failed to add car: {response.json().get('detail', 'Unknown error')}")


def update_car(car_id, car_data):
    response = requests.put(f"{BASE_URL}/cars/{car_id}", json=car_data)
    if response.status_code == 200:
        st.success(f"Car '{car_data['name']}' updated successfully!")
    else:
        st.error(f"Failed to update car: {response.json().get('detail', 'Unknown error')}")


def delete_car(car_id):
    response = requests.delete(f"{BASE_URL}/cars/{car_id}")
    if response.status_code == 200:
        st.success("Car deleted successfully!")
    else:
        st.error(f"Failed to delete car: {response.json().get('detail', 'Unknown error')}")

def mechanics_dashboard():
    st.title("Mechanic Management")

    st.subheader("Existing Mechanics")
    mechanics = get_mechanics()
    df_mechanics = pd.DataFrame(mechanics)
    st.dataframe(df_mechanics, use_container_width=True)

    st.subheader("Add New Mechanic")
    new_mechanic_name = st.text_input("Mechanic Name")

    if st.button("Add Mechanic"):
        if new_mechanic_name.strip():
            add_mechanic(new_mechanic_name)
        else:
            st.error("Mechanic name cannot be empty.")

    action = st.radio("What would you like to do?", options=["Update Mechanic", "Delete Mechanic"])

    if action == "Update Mechanic":
        selected_mechanic = st.selectbox("Select Mechanic to Update", options=[mechanic['name'] for mechanic in mechanics])
        new_name = st.text_input("New Mechanic Name", value=selected_mechanic)

        if st.button("Update Mechanic"):
            mechanic_id = next((mechanic['id'] for mechanic in mechanics if mechanic['name'] == selected_mechanic), None)
            update_mechanic(mechanic_id, new_name)

    elif action == "Delete Mechanic":
        mechanic_to_delete = st.selectbox("Select Mechanic to Delete", options=[mechanic['name'] for mechanic in mechanics])
        if st.button("Delete Mechanic"):
            mechanic_id = next((mechanic['id'] for mechanic in mechanics if mechanic['name'] == mechanic_to_delete), None)
            delete_mechanic(mechanic_id)

def cars_dashboard():
    st.title("Cars Management")

    st.subheader("Existing Cars")
    cars = get_cars()
    mechanics = get_mechanics()

    mechanic_id_to_name = {mechanic['id']: mechanic['name'] for mechanic in mechanics}
    for car in cars:
        car['car'] = mechanic_id_to_name.get(car['mechanic_id'], 'Unknown')
        del car['mechanic_id']

    df_cars = pd.DataFrame(cars)
    st.dataframe(df_cars, use_container_width=True)

    st.subheader("Add New Car")
    new_car_make = st.text_input("Make")
    selected_mechanic_name = st.selectbox("Select Mechanic", options=[mechanic['name'] for mechanic in mechanics],
                                        key="select_mechanic_add")
    new_car_year = st.number_input("Year", min_value=1900, max_value=datetime.now().year, step=1)

    if st.button("Add Car"):
        if new_car_make.strip():
            selected_mechanic_id = next((mechanic['id'] for mechanic in mechanics if mechanic['name'] == selected_mechanic_name),None)
            car_data = {
                "make": new_car_make,
                "mechanic_id": selected_mechanic_id,
                "year": new_car_year
            }
            add_car(car_data)
        else:
            st.error("Make and Year cannot be empty.")

    action = st.radio("What would you like to do?", options=["Update Car", "Delete Car"], key="radio_action")

    if action == "Update Car":
        selected_car = st.selectbox("Select Car to Update", options=[car['title'] for car in cars],
                                     key="select_car_update")

        if selected_car:
            car = next((car for car in cars if car['make'] == selected_car), None)
            new_car_make = st.text_input("Make", value=car['make'])
            selected_mechanic_name = st.selectbox("Select Mechanic", options=[mechanic['name'] for mechanic in mechanics],
                                                index=[author['name'] for author in mechanics].index(car['mechanic']),
                                                key="select_mechanic_update")
            new_car_year = st.number_input("Year", min_value=1440, max_value=datetime.now().year, step=1,
                                            value=car['year'])
            car_id = car['id']

            if st.button("Update Car"):
                car_data = {
                    "make": new_car_make,
                    "mechanic_id": next((mechanic['id'] for mechanic in mechanics if mechanic['name'] == selected_mechanic_name),
                                      None),
                    "year": new_car_year
                }
                update_car(car_id, car_data)

    elif action == "Delete Car":
        car_to_delete = st.selectbox("Select Car to Delete", options=[car['make'] for car in cars], key="select_car_delete")
        if st.button("Delete Book"):
            car_id = next((car['id'] for car in cars if car['make'] == car_to_delete), None)
            delete_car(car_id)

# def visualizations_dashboard():
#     st.title("Visualizations Dashboard")
#
#     # Fetch the books and authors data
#     books = get_books()
#     authors = get_authors()
#
#     if books:
#         # Convert books to a DataFrame
#         df_books = pd.DataFrame(books)
#
#         if 'author_id' in df_books.columns:
#             # Map author_id to author names
#             author_id_to_name = {author['id']: author['name'] for author in authors}
#             df_books['author'] = df_books['author_id'].map(author_id_to_name)
#             df_books.drop('author_id', axis=1, inplace=True)
#
#         # Sidebar filters
#         st.sidebar.title("Filters")
#
#         # Filter by Author
#         selected_author = st.sidebar.selectbox("Select Author", options=["All"] + list(author_id_to_name.values()))
#
#         # Filter by Published Year
#         min_year = int(df_books['published_year'].min())
#         max_year = int(df_books['published_year'].max())
#         selected_year = st.sidebar.slider("Select Published Year", min_value=min_year, max_value=max_year,
#                                           value=(min_year, max_year))
#
#         # Filter by Average Rating (fixed range from 0.0 to 5)
#         selected_rating = st.sidebar.slider("Select Average Rating", min_value=0.0, max_value=5.0, value=(0.0, 5.0),
#                                             step=0.1)
#
#         # Check if any filters are applied
#         filters_applied = selected_author != "All" or selected_year != (min_year, max_year) or selected_rating != (
#             0.0, 5.0)
#
#         # Apply Filters Button
#         if st.sidebar.button("Apply Filters") or not filters_applied:
#             # Apply filters if any are set
#             filtered_books = df_books.copy()  # Default to showing all data if no filters applied
#
#             if filters_applied:
#                 if selected_author != "All":
#                     filtered_books = filtered_books[filtered_books['author'] == selected_author]
#
#                 filtered_books = filtered_books[(filtered_books['published_year'] >= selected_year[0]) & (
#                         filtered_books['published_year'] <= selected_year[1])]
#                 filtered_books = filtered_books[(filtered_books['average_rating'] >= selected_rating[0]) & (
#                         filtered_books['average_rating'] <= selected_rating[1])]
#
#             # Visualization 1: Books by Year
#             if not filtered_books.empty:
#                 st.subheader(f"Books by Year")
#                 books_by_year = filtered_books.groupby('published_year').size().reset_index(name='Count')
#                 fig_years = px.bar(
#                     books_by_year,
#                     x='published_year',
#                     y='Count',
#                     title=f'Number of Books by Year',
#                     labels={"published_year": "Published Year", "Count": "Number of Books"},
#                     text='Count'
#                 )
#                 fig_years.update_traces(texttemplate='%{text:.2s}', textposition='outside')
#                 fig_years.update_layout(
#                     uniformtext_minsize=8,
#                     uniformtext_mode='hide',
#                     xaxis=dict(
#                         tickmode='linear',
#                         tick0=min_year,
#                         dtick=5,  # Show a label every 5 years (adjust as needed)
#                         tickangle=-45,
#                         tickfont=dict(size=10)
#                     ),
#                     yaxis=dict(title='Number of Books', range=[0, books_by_year['Count'].max() + 1]),
#                     title_x=0.5
#                 )
#                 st.plotly_chart(fig_years, use_container_width=True)
#
#                 # Visualization 2: Books by Average Rating
#                 st.subheader(f"Books by Average Rating")
#                 books_by_rating = filtered_books.groupby('average_rating').size().reset_index(name='Count')
#                 fig_ratings = px.bar(
#                     books_by_rating,
#                     x='average_rating',
#                     y='Count',
#                     title='Number of Books by Average Rating',
#                     labels={"average_rating": "Average Rating", "Count": "Number of Books"},
#                     text='Count'
#                 )
#                 fig_ratings.update_traces(texttemplate='%{text:.2s}', textposition='outside')
#                 fig_ratings.update_layout(
#                     uniformtext_minsize=8,
#                     uniformtext_mode='hide',
#                     yaxis=dict(title='Number of Books', range=[0, books_by_rating['Count'].max() + 1]),
#                     title_x=0.5
#                 )
#                 st.plotly_chart(fig_ratings, use_container_width=True)
#             else:
#                 st.warning("No book data available for the selected filters.")
#     else:
#         st.warning("No book data available for visualizations.")
#
#
st.sidebar.title("Navigation")
option = st.sidebar.selectbox("Choose a dashboard", ["Mechanics Dashboard", "Cars Dashboard"])
if option == "Authors Dashboard":
    mechanics_dashboard()
elif option == "Cars Dashboard":
    cars_dashboard()






















import sqlite3
from typing import List
from fastapi import APIRouter, HTTPException, status
from models.car import Car, CarCreate
from database import get_db_connection

router = APIRouter()


@router.get("/", response_model=List[Car])
def get_cars():
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
def create_car(car: CarCreate):
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
def update_car(car_id: int, car: CarCreate):
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
def delete_car(car_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM cars WHERE id = ?", (car_id,))
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Car not found")
    conn.commit()
    conn.close()
    return {"detail": "Car deleted"}
