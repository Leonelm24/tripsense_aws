import os
import pandas as pd
from src.extract import extract_places_by_categoria
from src.transformation import limpiezas_generales_places, calcular_distancias_places
from src.load import guardar_df_en_s3

def lambda_handler(event, context):
    print("▶ Lambda ejecutando extracción de lugares...")

    HOTEL_LAT = float(os.environ["HOTEL_LAT"])
    HOTEL_LON = float(os.environ["HOTEL_LON"])
    GOOGLE_API_KEY = os.environ["GOOGLE_API_KEY"]

    comidas = ["restaurant", "cafe", "bakery", "meal_takeaway"]
    actividades = ["gym", "spa", "movie_theater", "bowling_alley", "amusement_park"]
    atracciones = ["museum", "park", "tourist_attraction", "church", "art_gallery"]

    df_comidas = extract_places_by_categoria(HOTEL_LAT, HOTEL_LON, GOOGLE_API_KEY, "Comida", comidas, max_results=30)
    df_actividades = extract_places_by_categoria(HOTEL_LAT, HOTEL_LON, GOOGLE_API_KEY, "Actividad", actividades, max_results=30)
    df_atracciones = extract_places_by_categoria(HOTEL_LAT, HOTEL_LON, GOOGLE_API_KEY, "Atracción", atracciones, max_results=30)

    df_all = pd.concat([df_comidas, df_actividades, df_atracciones], ignore_index=True)

    df_clean = limpiezas_generales_places(df_all)
    df_clean = calcular_distancias_places(df_clean, HOTEL_LAT, HOTEL_LON)

    guardar_df_en_s3(df_clean, "tripsense", "data/processed/places.csv")

    print("✅ lugares procesados correctamente.")
    return {"statusCode": 200, "body": "Lugares procesados"}

