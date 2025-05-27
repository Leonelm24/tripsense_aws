from src.extract import generar_itinerarios_desde_reservas
from src.transformation import (
    limpiar_itineraries,
    limpiar_itinerary_days,
    limpiar_day_activities
)
from src.load import (
    guardar_itinerarios,
    guardar_itinerary_days,
    guardar_day_activities
)
import pandas as pd

def run():
    print("▶ Ejecutando pipeline_itineraries...")

    df_reservas = pd.read_csv("data/processed/reservations_clean.csv")
    df_places = pd.read_csv("data/processed/places.csv")

    itineraries, itinerary_days, day_activities = generar_itinerarios_desde_reservas(df_reservas, df_places)

    df_it_raw = pd.DataFrame(itineraries)
    df_days_raw = pd.DataFrame(itinerary_days)
    df_act_raw = pd.DataFrame(day_activities)

    df_it_clean = limpiar_itineraries(df_it_raw.copy())
    df_days_clean = limpiar_itinerary_days(df_days_raw.copy())
    df_act_clean = limpiar_day_activities(df_act_raw.copy())

    guardar_itinerarios(df_it_raw, df_it_clean)
    guardar_itinerary_days(df_days_raw, df_days_clean)
    guardar_day_activities(df_act_raw, df_act_clean)

    print("✅ Pipeline de itinerarios completado.")
