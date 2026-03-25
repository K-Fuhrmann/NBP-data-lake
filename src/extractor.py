import requests
import pandas as pd
from datetime import date, timedelta
from typing import List

# NBP API URL for Table A (average exchange rates)
NBP_API_URL = "http://api.nbp.pl/api/exchangerates/tables/A/"


def extract_data_nbp(start_date: date, end_date: date) -> pd.DataFrame:
    """
    Fetches NBP exchange rate data for a specified date range.
    """
    # Constructing a dynamic URL for the date range
    url = f"{NBP_API_URL}{start_date.isoformat()}/{end_date.isoformat()}/"

    print(f"INFO: Sending request to NBP API: {url}")

    try:
        response = requests.get(url, headers={'Accept': 'application/json'})
        response.raise_for_status()
        data: List[dict] = response.json()

        all_rates = []

        # Iterating through each day returned by the API
        for daily_table in data:
            exchange_date = daily_table.get('effectiveDate')
            rates = daily_table.get('rates', [])

            if rates:
                # 1. Creating a DataFrame for the given day
                rates_df = pd.DataFrame(rates)
                # 2. Adding the quotation date column
                rates_df['DataNotowania'] = exchange_date

                all_rates.append(rates_df)

        if not all_rates:
            print("WARNING: No data found in the returned date range.")
            return pd.DataFrame()

        # Concatenating all DataFrames into a single flat dataset
        final_df = pd.concat(all_rates, ignore_index=True)

        print(f"INFO: Successfully fetched and combined data from {len(data)} days.")
        return final_df

    except requests.exceptions.HTTPError as e:
        print(f"EXTRACTOR ERROR: HTTP Error: {e}. Ensure the date range is correct.")
        return pd.DataFrame()
    except Exception as e:
        print(f"EXTRACTOR ERROR: Unexpected error during JSON parsing: {e}")
        return pd.DataFrame()


if __name__ == '__main__':
    # Module Testing: fetching rates for the last 7 days
    today = date.today()
    one_week_ago = today - timedelta(days=7)
    df_test = extract_data_nbp(one_week_ago, today)

    if not df_test.empty:
        print("\n--- Data Sample after EXTRACTION (Multiple Days) ---")
        print(df_test.tail())
        print(f"\nTotal row count: {len(df_test)}")