import pandas as pd
import numpy as np
from math import radians, sin, cos, sqrt, atan2
from datetime import timedelta

def limpiezas_generales_places(df):
    df = df.copy()
    df.columns = df.columns.str.lower().str.strip()
    df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
    df["user_ratings_total"] = pd.to_numeric(df["user_ratings_total"], errors="coerce")
    df["type_main"] = df["type_main"].str.replace("_", " ").str.capitalize()
    df = df.reset_index(drop=True)
    df["place_id"] = ["PLACE_" + str(i) for i in range(len(df))]
    return df

def calcular_distancias_places(df, hotel_lat, hotel_lon):
    def haversine(lat1, lon1, lat2, lon2):
        R = 6371
        dlat = radians(lat2 - lat1)
        dlon = radians(lon2 - lon1)
        a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
        return R * 2 * atan2(sqrt(a), sqrt(1-a))
    df["distance_km"] = df.apply(lambda row: haversine(hotel_lat, hotel_lon, row["lat"], row["lon"]), axis=1)
    return df

def categorizar_tipo_places(df):
    def mapear_categoria(lista_types):
        if isinstance(lista_types, list):
            if "restaurant" in lista_types:
                return "Comida"
            elif "tourist_attraction" in lista_types or "museum" in lista_types:
                return "Atracción"
            elif "amusement_park" in lista_types or "activity" in lista_types:
                return "Actividad"
        return "Otro"
    df["categoria"] = df["type_list"].apply(mapear_categoria)
    return df

def limpiezas_generales_reservations(df: pd.DataFrame) -> pd.DataFrame:
    df["arrival_year"] = df["arrival_year"].astype(int)
    df["arrival_month"] = df["arrival_month"].astype(int)
    df["arrival_date"] = df["arrival_date"].astype(int)
    df["check_in"] = pd.to_datetime(
        df[["arrival_year", "arrival_month", "arrival_date"]].rename(
            columns={"arrival_year": "year", "arrival_month": "month", "arrival_date": "day"}
        ),
        errors="coerce"
    )
    df["total_nights"] = df["no_of_weekend_nights"] + df["no_of_week_nights"]
    df["check_out"] = df["check_in"] + df["total_nights"].apply(lambda x: timedelta(days=int(x)))
    columnas_float = [
        "avg_price_per_room", "no_of_weekend_nights", "no_of_week_nights", "total_nights"
    ]
    for col in columnas_float:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df = df.drop_duplicates()
    df = df.dropna(subset=["check_in"])
    return df

def limpiar_itineraries(df):
    df["overall_rating"] = pd.to_numeric(df["overall_rating"], errors="coerce")
    return df

def limpiar_itinerary_days(df):
    df["date"] = pd.to_datetime(df["date"])
    return df

def limpiar_day_activities(df):
    df["price"] = pd.to_numeric(df["price"])
    df["distance_km"] = pd.to_numeric(df["distance_km"])
    df["guest_rating"] = pd.to_numeric(df["guest_rating"])
    df["liked"] = df["guest_rating"].apply(lambda x: True if x > 2 else False)
    return df


