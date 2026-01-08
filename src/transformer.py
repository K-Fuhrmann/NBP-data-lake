import pandas as pd


def transform_nbp_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Czyści i przygotowuje dane z NBP do zapisu w formacie Parquet.
    """
    if df.empty:
        print("OSTRZEŻENIE: Otrzymano pusty DataFrame do transformacji.")
        return df

    print("INFO: Rozpoczynam transformację danych...")

    # 1. Kopia danych, aby nie zmieniać oryginału w trakcie pracy
    df = df.copy()

    # 2. Zmiana nazw kolumn na techniczne (bez spacji, małe litery - lepiej dla SQL)
    column_map = {
        'currency': 'waluta',
        'code': 'kod_waluty',
        'mid': 'kurs_sredni',
        'DataNotowania': 'data_notowania'
    }
    df = df.rename(columns=column_map)

    # 3. KONWERSJA TYPÓW (Kluczowe dla Parquet)
    # Konwersja daty ze stringa na obiekt daty
    df['data_notowania'] = pd.to_datetime(df['data_notowania']).dt.date

    # Upewnienie się, że kurs jest liczbą zmiennoprzecinkową
    df['kurs_sredni'] = pd.to_numeric(df['kurs_sredni'])

    # 4. DODANIE KOLUMN DO PARTYCJONOWANIA (Opcjonalne, ale bardzo przydatne w Data Lake)
    # Wyciągamy rok i miesiąc, co pozwoli nam potem fizycznie podzielić pliki na folderach
    df['rok'] = pd.to_datetime(df['data_notowania']).dt.year
    df['miesiac'] = pd.to_datetime(df['data_notowania']).dt.month

    # 5. Sortowanie danych dla porządku
    df = df.sort_values(by=['data_notowania', 'kod_waluty'])

    # 6. Wybór ostatecznych kolumn i ich kolejności
    final_columns = ['data_notowania', 'rok', 'miesiac', 'kod_waluty', 'waluta', 'kurs_sredni']
    df = df[final_columns]

    print(f"INFO: Transformacja zakończona. Przetworzono {len(df)} wierszy.")
    return df


if __name__ == '__main__':
    # Szybki test modułu na sztucznych danych (Mock Data)
    mock_data = pd.DataFrame([
        {'currency': 'dolar amerykański', 'code': 'USD', 'mid': 4.10, 'DataNotowania': '2025-12-15'},
        {'currency': 'euro', 'code': 'EUR', 'mid': 4.45, 'DataNotowania': '2025-12-15'}
    ])

    transformed_df = transform_nbp_data(mock_data)
    print("\n--- Dane po transformacji ---")
    print(transformed_df)
    print("\nTypy kolumn:")
    print(transformed_df.dtypes)