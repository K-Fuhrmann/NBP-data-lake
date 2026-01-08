import duckdb
import matplotlib.pyplot as plt
import pandas as pd


def create_trend_chart(currency_code='USD'):
    print(f"--- GENEROWANIE WYKRESU DLA {currency_code} ---")

    con = duckdb.connect()
    con.execute("INSTALL httpfs; LOAD httpfs; INSTALL aws; LOAD aws;")
    con.execute("SET s3_region='eu-north-1';")
    con.execute("CALL load_aws_credentials();")

    S3_PATH = "s3://moj-projekt-data-lake-nbp/raw/nbp_kursy/**/*.parquet"

    # Pobieramy daty i kursy, sortując je chronologicznie
    query = f"""
            SELECT data_notowania, kurs_sredni
            FROM read_parquet('{S3_PATH}')
            WHERE kod_waluty = '{currency_code}'
            ORDER BY data_notowania ASC
        """

    try:
        df = con.execute(query).df()

        # Pamiętaj, aby tutaj też zmienić nazwę kolumny
        df['data_notowania'] = pd.to_datetime(df['data_notowania'])

        # Tworzenie wykresu - oś X to teraz 'data_notowania'
        plt.figure(figsize=(12, 6))
        plt.plot(df['data_notowania'], df['kurs_sredni'], marker='o', linestyle='-', color='b')

        plt.title(f'Trend kursu {currency_code} (Dane z S3 Data Lake)', fontsize=14)
        plt.xlabel('Data notowania', fontsize=12)
        # ... reszta kodu bez zmian
        plt.ylabel('Kurs średni (PLN)', fontsize=12)
        plt.grid(True, linestyle='--', alpha=0.7)

        # Zapisanie wykresu do pliku
        output_file = f"charts/{currency_code}_trend.png"
        import os
        os.makedirs('charts', exist_ok=True)
        plt.savefig(output_file)

        print(f"✅ Wykres został zapisany w: {output_file}")
        plt.show()

    except Exception as e:
        print(f"❌ Błąd wizualizacji: {e}")


if __name__ == "__main__":
    create_trend_chart('USD')