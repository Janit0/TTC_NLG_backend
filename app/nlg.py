# -*- coding: utf-8 -*-
"""
Created on Fri Mar  6 01:05:16 2026

@author: Janit
"""

import sqlite3
import pandas as pd
import os 

def get_data():
    conn = sqlite3.connect("database/transit.db")
    df = pd.read_sql_query("SELECT * FROM trips_cleaned", conn)
    conn.close()
    return df

def get_businfo_data():
    conn = sqlite3.connect("database/transit.db")
    df = pd.read_sql_query("SELECT * from Bus_info", conn)
    conn.close()
    return df

def get_cleaned_data():
    return get_data()

def get_bus_data():
    return get_businfo_data()

df = get_cleaned_data()
bus_df = get_bus_data()

print(df.head())

def Bus_to_station_info(x):
    
    if x in df["trips_number"].values:
        
        selected_row = df[df["trips_number"] == x]
        selected_row_start = selected_row[
            selected_row["trips_station_1"].str.contains("STATION|STN", case = False) | 
            selected_row["trips_station_2"].str.contains("STATION|STN", case = False) |
            selected_row["trips_station_3"].str.contains("STATION|STN", case = False) 
            
        
                                          ]
        if selected_row_start.empty:
                return f"Bus number {x} does not go through any stations."
        stations = set()
        for  _,i in selected_row_start.iterrows():
            if "STATION" in i.trips_station_1 or "STN" in i.trips_station_1:
                stations.add(i.trips_station_1)
            if "STATION" in i.trips_station_2 or "STN" in i.trips_station_2:
                stations.add(i.trips_station_2)
            if "STATION" in i.trips_station_3 or "STN" in i.trips_station_3:
                stations.add(i.trips_station_3)
                
                
        return f"The bus number {x} goes through {' and '.join(stations).upper()}. "
    
    else: 
        return "No such bus exist"   
    
def Station_to_bus_info(y):
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
        
    
    
   
    row = df[df["trips_station_1"].str.contains(station, case = False) | 
                       df["trips_station_2"].str.contains(station, case = False) |
                       df["trips_station_3"].str.contains(station, case = False)
                       ]
    
    ### if station not in the list:::
    if row.empty: 
         return f"{station} doesnt have any buses in it's terminal."
    ###     
    else :    
        bus_numbers = set()
        for x,i in row.iterrows():
            bus_numbers.add(i.trips_number)
    
        return f"The {station} has buses {' '.join(sorted(bus_numbers))} in route."
    
    
def Bus_stops_info(bus_number, bus_df):
    
    bus_df["route_short_name"]= bus_df["route_short_name"].astype("string")
    
    data_bus_info_dropped = bus_df.dropna(subset = ["stop_name"])
    #unique_route_name = sorted(data_bus_info_dropped["route_short_name"].unique())
    selected_row = data_bus_info_dropped[data_bus_info_dropped["route_short_name"] == bus_number]
    trip = selected_row["trip_id"].iloc[0]
    selected_trip_id = selected_row[selected_row["trip_id"] == trip]
    trip_data_sorted = selected_trip_id.sort_values("arrival_time")
    return trip_data_sorted[["stop_name"]]

def bus_numbers_drop_down(bus_df):
    bus_df["route_short_name"]= bus_df["route_short_name"].astype("string")
    bus_df_dropna = bus_df.dropna(subset = ["stop_name"])
    unique_route_name = bus_df_dropna["route_short_name"].unique()
    return sorted(unique_route_name)

    
