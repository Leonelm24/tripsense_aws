import boto3
import pandas as pd
from io import StringIO

def guardar_df_en_s3(df, bucket, key):
    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False)
    s3 = boto3.resource("s3")
    s3.Object(bucket, key).put(Body=csv_buffer.getvalue())

def save_clean_reservations(df):
    guardar_df_en_s3(df, "tripsense", "data/processed/reservations_clean.csv")

def guardar_itinerarios(df_raw, df_clean):
    guardar_df_en_s3(df_clean, "tripsense", "data/processed/itineraries_clean.csv")

def guardar_itinerary_days(df_raw, df_clean):
    guardar_df_en_s3(df_clean, "tripsense", "data/processed/itinerary_days_clean.csv")

def guardar_day_activities(df_raw, df_clean):
    guardar_df_en_s3(df_clean, "tripsense", "data/processed/day_activities_clean.csv")

def guardar_csv_procesado(df, nombre_archivo):
    guardar_df_en_s3(df, "tripsense", f"data/processed/{nombre_archivo}.csv")
