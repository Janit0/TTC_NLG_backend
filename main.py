# -*- coding: utf-8 -*-
"""
Created on Fri Mar  6 01:14:35 2026

@author: Janit
"""

import requests
import os

DB_URL = "https://ttcstorage123.blob.core.windows.net/ttc-data/transit.db"
DB_PATH = "database/transit.db"

os.makedirs("database", exist_ok=True)

def download_db():
    r = requests.get(DB_URL, timeout=30)
    with open(DB_PATH, "wb") as f:
        f.write(r.content)

if not os.path.exists(DB_PATH):
    download_db()

from fastapi import FastAPI
from app.nlg import *

app = FastAPI()

@app.get("/bus/{bus_number}")
def bus_query(bus_number : str):
    return{"result":Bus_to_station_info(bus_number)}

@app.get("/station/{station_name}")
def station_query(station_name: str):
    return {"result":Station_to_bus_info(station_name)}

@app.get("/bus/{bus_number}/stops")
def get_bus_stops(bus_number: str):
    try:
        stops_df = Bus_stops_info(bus_number, data_bus_info)
        if stops_df is None or stops_df.empty:
            return {"error": f"No stops found for bus {bus_number}"}
        return {"stops": stops_df.to_dict(orient="records")}
    except Exception as e:
        return {"error": str(e)}
    
@app.get("/bus_numbers")
def bus_numbers():
    buses = bus_numbers_drop_down(data_bus_info)
    return {"buses": buses}

if __name__ == "__main__":
    import os
    import uvicorn

    port = int(os.environ.get("PORT", 8000))

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port
    )