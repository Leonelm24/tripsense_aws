from src.extract import extract_places_by_categoria
from src.transformation import limpiezas_generales_places, calcular_distancias_places
from src.load import guardar_csv, guardar_csv_procesado
from config import HOTEL_COORDS, GOOGLE_API_KEY
import pandas as pd

def run():
    print("▶ Ejecutando pipeline_places...")

    comidas = ["restaurant", "cafe", "bakery", "meal_takeaway"]
    actividades = ["gym", "spa", "movie_theater", "bowling_alley", "amusement_park"]
    atracciones = ["museum", "park", "tourist_attraction", "church", "art_gallery"]

    df_comidas = extract_places_by_categoria(HOTEL_COORDS["lat"], HOTEL_COORDS["lon"], GOOGLE_API_KEY, "Comida", comidas, max_results=30)
    df_actividades = extract_places_by_categoria(HOTEL_COORDS["lat"], HOTEL_COORDS["lon"], GOOGLE_API_KEY, "Actividad", actividades, max_results=30)
    df_atracciones = extract_places_by_categoria(HOTEL_COORDS["lat"], HOTEL_COORDS["lon"], GOOGLE_API_KEY, "Atracción", atracciones, max_results=30)

    df_all = pd.concat([df_comidas, df_actividades, df_atracciones], ignore_index=True)
    guardar_csv(df_all, "places", carpeta="data/raw")

    df_clean = limpiezas_generales_places(df_all)
    df_clean = calcular_distancias_places(df_clean, HOTEL_COORDS["lat"], HOTEL_COORDS["lon"])
    guardar_csv_procesado(df_clean, "places")

    print("✅ Places procesados correctamente.")

