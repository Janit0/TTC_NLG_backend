# -*- coding: utf-8 -*-
"""
Created on Fri Mar  6 01:05:16 2026

@author: Janit
"""

import sqlite3
import pandas as pd
import os 

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "database", "transit.db")
DB_PATH = os.path.abspath(DB_PATH)

def Bus_to_station_info(bus_number):

    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    query_bus_number = '''
    SELECT 1 from trips_cleaned WHERE trips_number = ? LIMIT 1
    '''
    cursor.execute(query_bus_number, (bus_number,))
    
    bus = cursor.fetchone()
    
    if not bus:
        conn.close()
        return f" No such bus exist"

    query = '''
    
    SELECT trips_station_1, trips_station_2, trips_station_3 FROM trips_cleaned WHERE
    trips_number = ?
    '''
    cursor.execute(query, (bus_number,))
    rows = cursor.fetchall()
    stations = set()
    
    for row in rows:
        for station in row:
            if station and station.upper().endswith("STATION"):
                stations.add(station.strip())
                
    conn.close()
            
    if not stations:
        return f"This bus number {bus_number} does not go through any stations"

    
    return f"The bus number {bus_number} goes through {' and '.join(stations)}." 
    
def Station_to_bus_info(y):
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    y_l = y.lower()
    y_cleaned = " ".join(y_l.split())
    if not y_cleaned.endswith("station"):
        y_cleaned += " station"
    
    station = y_cleaned.upper()

    ttc_station_list = ["FINCH STATION", "NORTH YORK CENTRE STATION", "SHEPPARD_YONGE STATION", "YORK MILLS STATION", "LAWRENCE STATION", "EGLINTON STATION", "DAVISVILLE STATION", "ST CLAIR STATION", "SUMMERHILL STATION", "ROSEDALE STATION", "BLOOR-YONGE", "WELLESLEY STATION", "COLLEGE", "TMU STATION", "QUEEN STATION", "KING STATION", "UNION STATION", "ST ANDREW STATION", "OSGOODE STATION", "ST PATRICK STATION", "QUEEN'S PARK STATION", "MUSEUM STATION", "ST GEORGE STATION", "SPADINA STATION", "DUPONT STATION", "ST CLAIR WEST STATION", "CEDARVALE STATION", "GLENCAIRN STATION", "LAWRENCE WEST STATION","YORKDALE STATION","WILSON STATION", "SHEPPARD WEST STATION", "DOWNSVIEW PARK STATION", "FINCH WEST STATION", "YORK UNIVERSITY STATION", "PIONEER VILLAGE STATION", "HIGHWAY 407 STATION", "VAUGHAN STATION",
                    "KIPLING STATION", "ISLINGTON STATION", "ROYAL YORK STATION", "OLD MILL STATION", "JANE STATION", "RUNNYMEDE STATION", "HIGH PARK STATION", "KEELE STATION", "DUNDAS WEST STATION", "LANSDOWNE STATION", "DUFFERIN STATION", "OSSINGTON STATION", "CHRISTIE STATION", "BATHURST STATION", "BAY STATION", "SHERBOURNE STATION", "CASTLE FRANK STATION", "BROADVIEW STATION", "CHESTER STATION", "PAPE STATION", "DONLANDS STATION", "GREENWOOD STATION", "COXWELL STATION", "WOODBINE STATION", "MAIN STREET STATION", "VICTORIA PARK STATION", "WARDEN STATION", "KENNEDY STATION",
                    "BAYVIEW STATION", "BESSARION STATION", "LESLIE STATION", "DON MILLS STATION",
                    "MOUNT DENNIS STATION", "KEELESDALE STATION", "CALEDONIA STATION", "FAIRBANK STATION", "OAKWOOD STATION", "FOREST HILL STATION", "CHAPLIN STATION", "AVENUE STATION", "MOUNT PLEASANT STATION", "LEASIDE STATION", "LAIRD STATION", "SUNNYBROOK PARK STATION", "DON VALLEY STATION", "AGA KHAN & MUSEUM STATION", "WYNFORD STATION", "SLOANE STATION", "O'CONNOR STATION", "PHARMACY STATION", "HAKIMI LEBOVIC STATION","GOLDEN MILE STATION", "BIRCHMOUNT STATION", "IONVIEW STATION" 
                    ]
    if station not in ttc_station_list:
        return f"{station} doesn't exist, please try something else."

        
    query_station = '''
    SELECT DISTINCT trips_number FROM trips_cleaned 
    WHERE  
     (trips_station_1 LIKE ?) 
    OR (trips_station_2 LIKE ?)
    OR (trips_station_3 LIKE ?)
    '''
    station_param = f"%{station}%"
    cursor.execute(query_station, (station_param, station_param, station_param))
    rows = cursor.fetchall()
    
    
    if not rows:
        conn.close()
        return f" The {station} does not have any buses in route."
    
    bus_numbers = set()
    
    for row in rows:
        if row[0]:
            bus_numbers.add(row[0])
    
    
    
    return f"The {station} has buses {' '.join(sorted(bus_numbers))} in route."
    
    
    
    
    
    
def Bus_stops_info(bus_number):
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    query_stops = "SELECT trip_id from Bus_info where route_short_name = ? GROUP BY trip_id ORDER BY count(stop_name) DESC LIMIT 1"
    cursor.execute(query_stops, (bus_number,) )
    
    trip_id = cursor.fetchone()
    
    if not trip_id:
        conn.close()
        return []
    trip = trip_id[0]
    
    
    query_sequence = "SELECT stop_name from Bus_info WHERE route_short_name = ? AND trip_id = ? ORDER BY arrival_time"
    
    cursor.execute(query_sequence, (bus_number , trip))
    rows = cursor.fetchall()
    
    conn.close()
    
    return [{"stop_name": r[0]} for r in rows]

def bus_numbers_drop_down():

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    query = """
        SELECT DISTINCT route_short_name
        FROM Bus_info
        WHERE route_short_name GLOB '[0-9]*'
        ORDER BY route_short_name
    """

    cursor.execute(query)
    rows = cursor.fetchall()

    conn.close()

    return [r[0] for r in rows]

    
