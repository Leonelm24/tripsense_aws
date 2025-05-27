import requests
import pandas as pd
import time
import random
import boto3
from io import StringIO
from datetime import timedelta

def fetch_google_places(lat, lon, tipo, api_key, radius=3000, max_results=20):
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        "location": f"{lat},{lon}",
        "radius": radius,
        "type": tipo,
        "key": api_key
    }

    lugares = []
    next_page_token = None
    total_results = 0

    while True:
        if next_page_token:
            params["pagetoken"] = next_page_token
            time.sleep(2)

        response = requests.get(url, params=params)
        data = response.json()

        for lugar in data.get("results", []):
            lugar_info = {
                "name": lugar.get("name"),
                "lat": lugar["geometry"]["location"]["lat"],
                "lon": lugar["geometry"]["location"]["lng"],
                "rating": lugar.get("rating"),
                "user_ratings_total": lugar.get("user_ratings_total"),
                "type_list": lugar.get("types"),
                "type_main": tipo,
                "address": lugar.get("vicinity")
            }
            lugares.append(lugar_info)
            total_results += 1
            if total_results >= max_results:
                break

        next_page_token = data.get("next_page_token")
        if not next_page_token or total_results >= max_results:
            break

    return pd.DataFrame(lugares)

def extraer_places_multiples_tipos(lat, lon, tipos, api_key):
    dfs = []
    for tipo in tipos:
        df_tipo = fetch_google_places(lat, lon, tipo, api_key)
        dfs.append(df_tipo)
        time.sleep(1)
    return pd.concat(dfs, ignore_index=True)

def extract_places_by_categoria(lat, lon, api_key, categoria, lista_tipos, max_results=30):
    df_list = []
    for tipo in lista_tipos:
        df_tipo = fetch_google_places(lat, lon, tipo, api_key, max_results=max_results)
        df_tipo["categoria"] = categoria
        df_list.append(df_tipo)
    return pd.concat(df_list, ignore_index=True)

def extract_reservations_s3(bucket="tripsense", key="data/raw/Hotel_Reservations.csv"):
    s3 = boto3.client("s3")
    obj = s3.get_object(Bucket=bucket, Key=key)
    return pd.read_csv(obj["Body"])

def generar_itinerarios_desde_reservas(df_reservas, df_places):
    itineraries = []
    itinerary_days = []
    day_activities = []

    itinerary_id_counter = 1
    day_id_counter = 1
    activity_id_counter = 1

    df_places_sample = df_places.copy()

    for _, reserva in df_reservas[df_reservas["booking_status"] == "Not_Canceled"].iterrows():
        check_in = pd.to_datetime(reserva["check_in"])
        check_out = pd.to_datetime(reserva["check_out"])
        dias_estancia = (check_out - check_in).days

        itineraries.append({
            "itinerary_id": itinerary_id_counter,
            "Booking_ID": reserva["Booking_ID"],
            "created_at": check_in,
            "overall_rating": None
        })

        used_places = set()

        for dia in range(dias_estancia):
            dia_actual = check_in + timedelta(days=dia)

            itinerary_days.append({
                "itinerary_day_id": day_id_counter,
                "itinerary_id": itinerary_id_counter,
                "date": dia_actual.date()
            })

            lugares_dia = df_places_sample[~df_places_sample["place_id"].isin(used_places)].sample(n=3)
            for _, lugar in lugares_dia.iterrows():
                used_places.add(lugar["place_id"])
                for time_slot in ["morning", "afternoon", "evening"]:
                    day_activities.append({
                        "activity_id": activity_id_counter,
                        "itinerary_day_id": day_id_counter,
                        "place_id": lugar["place_id"],
                        "time_slot": time_slot,
                        "price": round(random.uniform(10, 100), 2),
                        "distance_km": round(random.uniform(0.2, 8.0), 2),
                        "guest_rating": random.randint(1, 5),
                        "guest_feedback": "",
                        "liked": None,
                        "coupon_code": random.choice([True, False])
                    })
                    activity_id_counter += 1

            day_id_counter += 1
        itinerary_id_counter += 1

    return itineraries, itinerary_days, day_activities


