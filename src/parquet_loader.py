import os
import pandas as pd
import awswrangler as wr
import logging
from dotenv import load_dotenv

# Wczytanie zmiennych z .env
load_dotenv()

# Pobranie konfiguracji
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
S3_REGION = os.getenv("S3_REGION")
S3_BASE_PATH = f"s3://{S3_BUCKET_NAME}/raw/nbp_kursy/"

def load_data_to_s3(df: pd.DataFrame, s3_path: str = S3_BASE_PATH):
    if df.empty:
        logging.warning("Brak danych do wysłania na S3.")
        return

    logging.info(f"Rozpoczynam wysyłkę {len(df)} wierszy do AWS S3 na ścieżkę: {s3_path}")

    try:
        wr.s3.to_parquet(
            df=df,
            path=s3_path,
            dataset=True,
            partition_cols=['rok', 'miesiac'],
            mode="append",
            boto3_session=None # Używa domyślnej sesji AWS CLI
        )
        logging.info("SUKCES: Dane zostały zapisane w Data Lake.")
    except Exception as e:
        logging.error(f"BŁĄD AWS: Nie udało się wysłać danych. Detale: {e}")
        raise # Podajemy błąd dalej do main.py