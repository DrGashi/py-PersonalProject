import os
from datetime import datetime
import pandas as pd
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL")

def get_mechanics():
    return requests.get(f"{BASE_URL}/mechanics/").json()

def add_mechanic(name):
    requests.post(f"{BASE_URL}/mechanics/",json={"name": name})

def update_mechanic(mechanic_id, mechanic_data):
    requests.put(f"{BASE_URL}/mechanics/{mechanic_id}", json=mechanic_data)

def delete_mechanic(mid):
    requests.delete(f"{BASE_URL}/mechanics/{mid}")

def get_cars():
    response = requests.get(f"{BASE_URL}/cars/")
    return response.json()

def add_car(data):
    requests.post(f"{BASE_URL}/cars/",json=data)

def update_car(car_id, car_data):
    requests.put(f"{BASE_URL}/cars/{car_id}", json=car_data)

def delete_car(cid):
    requests.delete(f"{BASE_URL}/cars/{cid}")

def mechanics_dashboard():
    st.title("Mechanics")
    mechanics = get_mechanics()
    if mechanics:
        st.dataframe(pd.DataFrame(mechanics), use_container_width=True)

    st.subheader("Add Mechanic")

    name = st.text_input("Mechanic Name")

    if st.button("Add Mechanic"):
        if name:
            add_mechanic(name)
            st.rerun()

    action = st.radio("What would you like to do?", options=["Update Mechanic", "Delete Mechanic"])

    if action == "Update Mechanic":
        st.subheader("Update Mechanic")

        selected_mechanic = st.selectbox("Choose mechanic", mechanics, format_func=lambda x: f"{x['name']}")

        new_name = st.text_input("New Name", selected_mechanic["name"])

        if mechanics:

            if st.button("Update Mechanic"):
                mechanic_data = {
                    "name": new_name
                }
                update_mechanic(selected_mechanic["id"], mechanic_data)
                st.rerun()

    elif action == "Delete Mechanic":
        st.subheader("Delete Mechanic")

        if mechanics:
            selected = st.selectbox("Choose Mechanic", mechanics, format_func=lambda x: x["name"])
            if st.button("Delete Mechanic"):
                delete_mechanic(selected["id"])
                st.rerun()

def cars_dashboard():
    st.title("Cars")

    cars = get_cars()
    mechanics = get_mechanics()

    mechanic_map = {
        m["id"]: m["name"]
        for m in mechanics
    }

    display = []

    for car in cars:
        display.append({
            "ID": car["id"],
            "Make": car["make"],
            "Model": car["model"],
            "Year": car["year"],
            "Issue": car["issue"],
            "Mechanic": mechanic_map.get(car["mechanic_id"])
        })

    if display:
        st.dataframe(pd.DataFrame(display), use_container_width=True)

    st.subheader("Add Car")

    make = st.text_input("Make")
    model = st.text_input("Model")

    year = st.number_input("Year", min_value=1900, max_value=datetime.now().year, step=1)

    issue = st.text_area("Issue")

    mechanic = st.selectbox("Mechanic", mechanics, format_func=lambda x: x["name"])

    if st.button("Add Car"):
        car_data = {
            "make": make,
            "model": model,
            "year": year,
            "issue": issue,
            "mechanic_id": mechanic["id"]
        }
        add_car(car_data)
        st.rerun()

    action = st.radio("What would you like to do?", options=["Update Car", "Delete Car"], key="radio_action")

    if action == "Update Car":
        st.subheader("Update Car")

        selected_car = st.selectbox("Choose Car", cars, format_func=lambda x: f"{x['year']} {x['make']} {x['model']}")

        new_make = st.text_input("Car Make", selected_car["make"])
        new_model = st.text_input("Car Model", selected_car["model"])
        new_year = st.number_input("Car Year", min_value=1900, max_value=datetime.now().year, step=1, value=selected_car["year"])
        new_issue = st.text_area("Car Issue",selected_car["issue"])
        mechanic_index = next((i for i, mechanic in enumerate(mechanics)if mechanic["id"] == selected_car["mechanic_id"]),0)
        new_mechanic = st.selectbox("Car Mechanic", mechanics, index=mechanic_index, format_func=lambda x: x["name"])

        if cars:

            if st.button("Update Car"):
                car_data = {
                    "make": new_make,
                    "model": new_model,
                    "year": new_year,
                    "issue": new_issue,
                    "mechanic_id": new_mechanic["id"]
                }
                update_car(selected_car["id"], car_data)
                st.rerun()

    elif action == "Delete Car":
        st.subheader("Delete Car")

        if cars:

            selected_car = st.selectbox("Choose Car", cars, format_func=lambda x: f"{x['make']} {x['model']}")

            if st.button("Delete Car"):
                delete_car(selected_car["id"])
                st.rerun()

st.sidebar.title("Navigation")

page = st.sidebar.selectbox("Select Page",["Mechanics","Cars"])

if page == "Mechanics":
    mechanics_dashboard()

if page == "Cars":
    cars_dashboard()