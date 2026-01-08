import duckdb


def run_analysis():
    print("--- ANALIZA DANYCH S3 (BEZPIECZNA KONFIGURACJA) ---")

    con = duckdb.connect()

    # 1. Ładowanie niezbędnych rozszerzeń
    con.execute("INSTALL httpfs; LOAD httpfs;")
    con.execute("INSTALL aws; LOAD aws;")

    # 2. KONFIGURACJA BEZPIECZNA
    # Zamiast wpisywać klucze ręcznie, nakazujemy DuckDB pobrać je z AWS CLI
    try:
        con.execute("CALL load_aws_credentials();")
        con.execute("SET s3_region='eu-north-1';")  # Ustawiamy tylko region
    except Exception as e:
        print(f"❌ Błąd ładowania poświadczeń AWS: {e}")
        return

    bucket = 'moj-projekt-data-lake-nbp'
    full_path = f"s3://{bucket}/raw/nbp_kursy/**/*.parquet"

    print(f"INFO: Łączenie z bucketem: {bucket} w regionie eu-north-1")

    try:
        # Wykonanie analizy na wszystkich plikach
        print("\n--- WYNIKI ANALIZY ---")
        query = f"""
            SELECT 
                kod_waluty, 
                AVG(kurs_sredni) as sredni_kurs 
            FROM read_parquet('{full_path}', hive_partitioning=1) 
            GROUP BY 1 
            ORDER BY 2 DESC
            LIMIT 10
        """
        df = con.execute(query).df()
        print(df)
        print("\n✅ Analiza zakończona sukcesem przy użyciu poświadczeń systemowych.")

    except Exception as e:
        print(f"❌ BŁĄD ANALIZY: {e}")


if __name__ == "__main__":
    run_analysis()