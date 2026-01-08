import pandas as pd
import awswrangler as wr  # Biblioteka AWS Data Wrangler - najlepsza do S3 i Parquet
import boto3

# --- KONFIGURACJA AWS ---
# Tutaj wpisz nazwę swojego bucketu
S3_BUCKET_NAME = "moj-projekt-data-lake-nbp"
S3_BASE_PATH = f"s3://{S3_BUCKET_NAME}/raw/nbp_kursy/"


def load_data_to_s3(df: pd.DataFrame, s3_path: str = S3_BASE_PATH):
    """
    Zapisuje DataFrame bezpośrednio do AWS S3 w formacie Parquet z partycjonowaniem.
    """
    if df.empty:
        print("OSTRZEŻENIE: Brak danych do wysłania na S3.")
        return

    print(f"INFO: Rozpoczynam wysyłkę {len(df)} wierszy do AWS S3...")
    print(f"CEL: {s3_path}")

    try:
        # AWS Wrangler robi wszystko za nas:
        # 1. Konwertuje DataFrame na Parquet
        # 2. Tworzy partycje (foldery w S3)
        # 3. Łączy się przez Twoje poświadczenia AWS (boto3)
        wr.s3.to_parquet(
            df=df,
            path=s3_path,
            dataset=True,  # Informacja, że to jest zbiór danych (Data Lake)
            partition_cols=['rok', 'miesiac'],  # Tworzy strukturę s3://bucket/rok=2025/miesiac=12/
            mode="append"  # Jeśli pliki już są, dodaje nowe (nie kasuje starych)
        )
        print("SUKCES: Dane są już bezpieczne w Twoim Buckecie S3!")

    except Exception as e:
        print(f"BŁĄD AWS: Nie udało się wysłać danych na S3. Sprawdź uprawnienia! \nDetale: {e}")


if __name__ == '__main__':
    # TEST: Spróbujmy wysłać małą próbkę (wymaga skonfigurowanego AWS CLI / poświadczeń)
    test_df = pd.DataFrame([
        {'waluta': 'USD', 'kurs_sredni': 4.10, 'rok': 2025, 'miesiac': 12, 'kod_waluty': 'USD',
         'data_notowania': '2025-12-15'}
    ])

    # load_data_to_s3(test_df) # Odkomentuj, gdy będziesz gotowy do testu w chmurze