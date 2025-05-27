from src.extract import extract_reservations_s3
from src.transformation import limpiezas_generales_reservations
from src.load import save_clean_reservations

def lambda_handler(event, context):
    print("▶ Lambda ejecutando procesamiento de reservas...")

    df_raw = extract_reservations_s3()
    df_clean = limpiezas_generales_reservations(df_raw)
    save_clean_reservations(df_clean)

    print("✅ reservas procesadas correctamente.")
    return {"statusCode": 200, "body": "Reservas procesadas"}
