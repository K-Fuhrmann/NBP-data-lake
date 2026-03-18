import logging
import os
from datetime import date, timedelta
from dotenv import load_dotenv
from src.extractor import extract_data_nbp
from src.transformer import transform_nbp_data
from src.parquet_loader import load_data_to_s3

# 1. Konfiguracja logowania
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("pipeline.log"), # Zapis do pliku
        logging.StreamHandler()              # Wypis na ekran
    ]
)
logger = logging.getLogger(__name__)

# 2. Ładowanie zmiennych środowiskowych
load_dotenv()

def run_pipeline(days_back: int = 7):
    logger.info(f"--- START POTOKU ETL (Zakres: {days_back} dni) ---")

    try:
        # EKSTRAKCJA
        today = date.today()
        start_date = today - timedelta(days=days_back)
        raw_df = extract_data_nbp(start_date, today)
        
        if raw_df is None or raw_df.empty:
            logger.error("Proces przerwany: Ekstrakcja nie zwróciła danych.")
            return

        # TRANSFORMACJA
        # Tutaj try/except wyłapie np. błędy w nazwach kolumn z API
        clean_df = transform_nbp_data(raw_df)

        # ŁADOWANIE
        load_data_to_s3(clean_df)
        
        logger.info("--- POTOK ETL ZAKOŃCZONY SUKCESEM ---")

    except ConnectionError as e:
        logger.error(f"Błąd połączenia z API lub AWS: {e}")
    except Exception as e:
        logger.critical(f"KRYTYCZNY BŁĄD SYSTEMOWY: {e}", exc_info=True)

if __name__ == "__main__":
    run_pipeline(days_back=30)