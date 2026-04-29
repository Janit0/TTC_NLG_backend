# -*- coding: utf-8 -*-
"""
Created on Fri Mar  6 01:14:35 2026

@author: Janit
"""

import os
import requests

from fastapi import FastAPI
from app.nlg import (
    Bus_to_station_info,
    Station_to_bus_info,
    Bus_stops_info,
    bus_numbers_drop_down
)

from functools import lru_cache
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# ---------------- CORS ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- CACHE ----------------
@lru_cache(maxsize=500)
def cached_bus_query(bus_number: str):
    return Bus_to_station_info(bus_number)


# ---------------- ROUTES ----------------

@app.get("/bus/{bus_number}")
def bus_query(bus_number: str):
    return {"data": cached_bus_query(bus_number)}


@app.get("/station/{station_name}")
def station_query(station_name: str):
    return {"data": Station_to_bus_info(station_name)}


@app.get("/bus/{bus_number}/stops")
def get_bus_stops(bus_number: str):
   stops = Bus_stops_info(bus_number)
   return {"data" : stops}


@app.get("/bus_numbers")
def bus_numbers():
    # same fix: load inside call instead of global import dependency
    buses = bus_numbers_drop_down()
    return {"data": buses}


# ---------------- MAIN ----------------
if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", 8000))

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=False  # ✅ important for Azure stability
    )