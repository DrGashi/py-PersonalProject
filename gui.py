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

def delete_mechanic(mid):
    requests.delete(f"{BASE_URL}/mechanics/{mid}")

def get_cars():
    response = requests.get(f"{BASE_URL}/cars/")
    return response.json()

def add_car(data):
    requests.post(f"{BASE_URL}/cars/",json=data)

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