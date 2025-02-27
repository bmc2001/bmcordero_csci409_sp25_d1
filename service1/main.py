"""
Program: main.py
Student Name: Brendan Cordero
Course: CSCI 409 D1
Description: Program to run routes from app.py in order to run this as a microservice
"""

from fastapi import FastAPI, Depends
from dotenv import load_dotenv
from auth import get_current_user
import requests
import os

load_dotenv()
API_KEY = os.getenv("API_KEY")  # Fill in with your API Key
ENDPOINT_URL = "https://api-v3.mbta.com/"  # DO NOT CHANGE THIS

app = FastAPI()  # Initialize the end point for FastAPI app


@app.get("/")  # Create a default route
def read_root():
    return {"message": "Welcome to my FastAPI Application within a microservice!"}


# Get a list of all routes
@app.get("/routes", dependencies=[Depends(get_current_user)])
def get_routes():
    routes_list = list()
    response = requests.get(ENDPOINT_URL + f"/routes?&api_key={API_KEY}")  # Send a request to the endpoint
    # Convert the response to json and extract the data key
    routes = response.json()["data"]
    for route in routes:
        # Loop through all routes extracting relevant information
        routes_list.append({
            "id": route["id"],
            "type": route["type"],
            "color": route["attributes"]["color"],
            "text_color": route["attributes"]["text_color"],
            "description": route["attributes"]["description"],
            "long_name": route["attributes"]["long_name"],
            "type": route["attributes"]["type"],
        })
    # Return the routes_list in JSON format
    return {"routes": routes_list}


# Get information on a specific route
@app.get("/routes/{route_id}", dependencies=[Depends(get_current_user)])
def get_route(route_id: str):
    response = requests.get(ENDPOINT_URL + f"/routes/{route_id}?api_key={API_KEY}")  # Send a request to the endpoint
    # Convert the response to json and extract the data key
    route_data = response.json()["data"]
    # Extract the relevant data
    route = {
        "id": route_data["id"],
        "type": route_data["type"],
        "color": route_data["attributes"]["color"],
        "text_color": route_data["attributes"]["text_color"],
        "description": route_data["attributes"]["description"],
        "long_name": route_data["attributes"]["long_name"],
        "type": route_data["attributes"]["type"],
    }
    # Return the data to the user
    return {"routes": route}


# gives all lines with data and other specified attributes
@app.get("/lines", dependencies=[Depends(get_current_user)])
def get_lines():
    lines_list = list()
    response = requests.get(ENDPOINT_URL + f"/routes?api_key={API_KEY}")
    routes = response.json()["data"]
    for route in routes:  # used a for loop to loop the data that's being returned
        lines_list.append({
            "id": route["id"],
            "text_color": route["attributes"]["text_color"],
            "short_name": route["attributes"].get("Short_name", ""),
            "long_name": route["attributes"]["long_name"],
            "color": route["attributes"]["color"]
        })
    return {"lines": lines_list}


# gives details for a specified line
@app.get("/lines/{line_id}", dependencies=[Depends(get_current_user)])
def get_line(line_id: str):
    response = requests.get(ENDPOINT_URL + f"/routes/{line_id}?api_key={API_KEY}")
    route_data = response.json().get("data")
    if not route_data:  # used if statement for simple error handling and returning specified lines through ID
        return {"error": "Line not found"}
    line = {
        "id": route_data["id"],
        "text_color": route_data["attributes"]["text_color"],
        "short_name": route_data["attributes"].get("short_name", ""),
        "long_name": route_data["attributes"]["long_name"],
        "color": route_data["attributes"]["color"],
    }
    return {"line": line}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001)
