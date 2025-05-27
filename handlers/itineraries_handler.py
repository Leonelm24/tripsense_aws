import pandas as pd
import boto3
from src.extract import generar_itinerarios_desde_reservas
from src.transformation import (
    limpiar_itineraries,
    limpiar_itinerary_days,
    limpiar_day_activities
)
from src.load import guardar_df_en_s3

def leer_csv_s3(bucket, key):
    s3 = boto3.client("s3")
    obj = s3.get_object(Bucket=bucket, Key=key)
    return pd.read_csv(obj["Body"])

def lambda_handler(event, context):
    print("▶ Lambda ejecutando generación de itinerarios...")

    df_reservas = leer_csv_s3("tripsense", "data/processed/reservations_clean.csv")
    df_places = leer_csv_s3("tripsense", "data/processed/places.csv")

    itineraries, itinerary_days, day_activities = generar_itinerarios_desde_reservas(df_reservas, df_places)

    df_it_raw = pd.DataFrame(itineraries)
    df_days_raw = pd.DataFrame(itinerary_days)
    df_act_raw = pd.DataFrame(day_activities)

    df_it_clean = limpiar_itineraries(df_it_raw.copy())
    df_days_clean = limpiar_itinerary_days(df_days_raw.copy())
    df_act_clean = limpiar_day_activities(df_act_raw.copy())

    guardar_df_en_s3(df_it_clean, "tripsense", "data/processed/itineraries_clean.csv")
    guardar_df_en_s3(df_days_clean, "tripsense", "data/processed/itinerary_days_clean.csv")
    guardar_df_en_s3(df_act_clean, "tripsense", "data/processed/day_activities_clean.csv")

    print("✅ itinerarios generados correctamente.")
    return {"statusCode": 200, "body": "Itinerarios generados"}

