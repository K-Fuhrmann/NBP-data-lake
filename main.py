from datetime import date, timedelta
from src.extractor import extract_data_nbp
from src.transformer import transform_nbp_data
from src.parquet_loader import load_data_to_s3  # Używamy wersji S3


def run_pipeline(days_back: int = 7):
    """
    Główna funkcja uruchamiająca proces ETL:
    Extract -> Transform -> Load
    """
    print(f"--- ROZPOCZYNAM POTOK ETL (Zakres: ostatnie {days_back} dni) ---")

    # 1. OKREŚLENIE ZAKRESU DAT
    today = date.today()
    start_date = today - timedelta(days=days_back)

    # 2. EKSTRAKCJA (Extract)
    # Pobieramy surowe dane z API NBP
    raw_df = extract_data_nbp(start_date, today)

    if raw_df is None or raw_df.empty:
        print("BŁĄD: Nie udało się pobrać danych. Kończę proces.")
        return

    # 3. TRANSFORMACJA (Transform)
    # Czyścimy, typujemy i dodajemy kolumny rok/miesiac
    clean_df = transform_nbp_data(raw_df)

    # 4. ŁADOWANIE (Load)
    # Wysyłamy dane prosto do chmury AWS S3
    try:
        load_data_to_s3(clean_df)
        print("--- POTOK ETL ZAKOŃCZONY SUKCESEM ---")
    except Exception as e:
        print(f"--- POTOK ETL ZAKOŃCZONY BŁĘDEM: {e} ---")


if __name__ == "__main__":
    # Tutaj decydujesz, jak głęboko w historię chcesz sięgnąć przy tym uruchomieniu
    run_pipeline(days_back=30)