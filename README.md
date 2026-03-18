# NBP Currency Data Pipeline - Cloud Data Lake



## Opis projektu

Zautomatyzowany potok danych (ETL) pobierający kursy walut z API Narodowego Banku Polskiego, przetwarzający je do formatu analitycznego i składujący w chmurowym Data Lake (AWS S3). Projekt demonstruje podejście Modern Data Stack z wykorzystaniem partycjonowania danych i analizy bezserwerowej.



## Stack technologiczny

- Python (Pandas)
- AWS S3 (Data Lake)
- Apache Parquet 
- Duck DB (query engine dla S3)
- awswrangler(integracja z S3), requests, matplotlib


## Funkcjonalności

- Automatyczne Partycjonowanie: Dane są zapisywane w strukturze folderów S3, co optymalizuje koszty zapytań SQL (Partition Pruning).
- Bezpieczeństwo: Wykorzystanie systemowych poświadczeń AWS i brak twardo wpisanych kluczy w kodzie.
- Analiza On-the-fly: Integracja z DuckDB pozwala na wykonywanie zapytań SQL bezpośrednio na plikach Parquet w chmurze bez konieczności stawiania ciężkiej bazy danych.

## Jak uruchomić?

- Sklonuj repozytorium 
- Skonfiguruj AWS CLI (aws configure)
- Zainstaluj biblioteki: pip install -r requirements
- Uruchom proces: python main.py