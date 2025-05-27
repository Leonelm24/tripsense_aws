from src.extract import extract_reservations_csv
from src.transformation import limpiezas_generales_reservations
from src.load import save_clean_reservations

def run():
    print("▶ Ejecutando pipeline_reservations...")

    df_raw = extract_reservations_csv()
    df_clean = limpiezas_generales_reservations(df_raw)
    save_clean_reservations(df_clean)

    print("✅ Reservas procesadas correctamente.")
