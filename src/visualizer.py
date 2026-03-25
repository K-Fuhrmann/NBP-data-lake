import duckdb
import matplotlib.pyplot as plt
import pandas as pd


def create_trend_chart(currency_code='USD'):
    print(f"--- GENERATING CHART FOR {currency_code} ---")

    con = duckdb.connect()
    # Loading extensions to handle S3 connectivity
    con.execute("INSTALL httpfs; LOAD httpfs; INSTALL aws; LOAD aws;")
    con.execute("SET s3_region='eu-north-1';")
    con.execute("CALL load_aws_credentials();")

    S3_PATH = "s3://moj-projekt-data-lake-nbp/raw/nbp_kursy/**/*.parquet"

    # Fetching dates and rates, sorting them chronologically
    query = f"""
            SELECT data_notowania, kurs_sredni
            FROM read_parquet('{S3_PATH}')
            WHERE kod_waluty = '{currency_code}'
            ORDER BY data_notowania ASC
        """

    try:
        df = con.execute(query).df()

        # Convert column to datetime for proper plotting
        df['data_notowania'] = pd.to_datetime(df['data_notowania'])

        # Chart creation - X-axis uses 'data_notowania'
        plt.figure(figsize=(12, 6))
        plt.plot(df['data_notowania'], df['kurs_sredni'], marker='o', linestyle='-', color='b')

        plt.title(f'Trend kursu {currency_code} (Dane z S3 Data Lake)', fontsize=14)
        plt.xlabel('Data notowania', fontsize=12)
        
        plt.ylabel('Kurs średni (PLN)', fontsize=12)
        plt.grid(True, linestyle='--', alpha=0.7)

        # Save chart to the 'charts' directory
        output_file = f"charts/{currency_code}_trend.png"
        import os
        os.makedirs('charts', exist_ok=True)
        plt.savefig(output_file)

        print(f" Chart successfully saved to: {output_file}")
        plt.show()

    except Exception as e:
        print(f" Visualization error: {e}")


if __name__ == "__main__":
    create_trend_chart('USD')