import requests
import pandas as pd
from datetime import date, timedelta
from typing import List

# Adres API NBP dla tabeli A (średnie kursy)
NBP_API_URL = "http://api.nbp.pl/api/exchangerates/tables/A/"


def extract_data_nbp(start_date: date, end_date: date) -> pd.DataFrame:
    """
    Pobiera dane kursów walut NBP dla zadanego zakresu dat.
    """
    # Budowanie dynamicznego URL dla zakresu dat
    url = f"{NBP_API_URL}{start_date.isoformat()}/{end_date.isoformat()}/"

    print(f"INFO: Wysyłam zapytanie do API NBP: {url}")

    try:
        response = requests.get(url, headers={'Accept': 'application/json'})
        response.raise_for_status()
        data: List[dict] = response.json()

        all_rates = []

        # Iteracja po każdym dniu zwróconym przez API
        for daily_table in data:
            exchange_date = daily_table.get('effectiveDate')
            rates = daily_table.get('rates', [])

            if rates:
                # 1. Tworzenie DataFrame dla danego dnia
                rates_df = pd.DataFrame(rates)
                # 2. Dodanie kolumny z datą notowania
                rates_df['DataNotowania'] = exchange_date

                all_rates.append(rates_df)

        if not all_rates:
            print("OSTRZEŻENIE: Brak danych w zwróconym zakresie dat.")
            return pd.DataFrame()

        # Konkatenacja wszystkich DataFrame w jeden płaski zbiór danych
        final_df = pd.concat(all_rates, ignore_index=True)

        print(f"INFO: Pomyślnie pobrano i połączono dane z {len(data)} dni.")
        return final_df

    except requests.exceptions.HTTPError as e:
        print(f"BŁĄD EXTRACTORA: Błąd HTTP: {e}. Upewnij się, że zakres dat jest poprawny.")
        return pd.DataFrame()
    except Exception as e:
        print(f"BŁĄD EXTRACTORA: Nieoczekiwany błąd podczas parsowania JSON: {e}")
        return pd.DataFrame()


if __name__ == '__main__':
    # Testowanie modułu: pobranie kursów za ostatnie 7 dni
    today = date.today()
    one_week_ago = today - timedelta(days=7)
    df_test = extract_data_nbp(one_week_ago, today)

    if not df_test.empty:
        print("\n--- Próbka danych po EKSTRAKCJI (Wiele Dni) ---")
        print(df_test.tail())
        print(f"\nCałkowita liczba wierszy: {len(df_test)}")