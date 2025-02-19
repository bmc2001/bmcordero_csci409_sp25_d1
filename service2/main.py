"""
Program: main.py
Student Name: Brendan Cordero
Course: CSCI 409 D1
Description: Program to run routes from app.py in order to run this as a microservice
"""

from fastapi import FastAPI, Depends
import httpx

API_KEY = "76b1c90015874a138fa71dbe8e86decf"  # Fill in with your API Key
ENDPOINT_URL = "https://api-v3.mbta.com/"  # DO NOT CHANGE THIS

app = FastAPI()  # Initialize the end point for FastAPI app


@app.get("/")  # Create a default route
def read_root():
    return {"message": "Welcome to my FastAPI Application!"}


# Dependency that will fetch all alerts with optional filters

async def get_all_alerts(route: str = None, stop: str = None):
    params = {"api_key": API_KEY}
    if route:
        params["filter[route]"] = route
    if stop:
        params["filter[stop]"] = stop

    async with httpx.AsyncClient() as client:
        response = await client.get(f"{ENDPOINT_URL}/alerts", params=params)
        response.raise_for_status()
        return response.json()


# Dependency that will fetch a specific alert using ID

async def get_alert_by_id(alert_id: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{ENDPOINT_URL}/alerts/{alert_id}?api_key={API_KEY}")
        response.raise_for_status()
        return response.json()


# route that will fetch all alerts

@app.get("/alerts")
async def read_alerts(route: str = None, stop: str = None, alerts=Depends(get_all_alerts)):
    return alerts


@app.get("/alerts/{alert_id}")
async def read_alert(alert_id: str, alert=Depends(get_alert_by_id)):
    return alert


# Dependency that will fetch all vehicles with filters


async def get_all_vehicles(route: str = None, revenue: bool = None):
    params = {"api_key": API_KEY}
    if route:
        params["filter[route]"] = route
    if revenue is not None:
        params["filter[is_revenue]"] = str(revenue).lower()

    async with httpx.AsyncClient() as client:
        response = await client.get(f"{ENDPOINT_URL}/vehicles", params=params)
        response.raise_for_status()
        return response.json()


# Dependency that fetches a specific vehicle with ID

async def get_vehicle_by_id(vehicle_id: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{ENDPOINT_URL}/vehicles/{vehicle_id}?api_key={API_KEY}")
        response.raise_for_status()
        return response.json()


# Route that will fetch all vehicles with filters


@app.get("/vehicles")
async def read_vehicles(route: str = None, revenue: bool = None, vehicles=Depends(get_all_vehicles)):
    return vehicles


# Route that will fetch a specific vehicle with ID
@app.get("/vehicles/{vehicle_id}")
async def read_vehicle(vehicle_id: str, vehicle=Depends(get_vehicle_by_id)):
    return vehicle

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
