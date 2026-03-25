import pandas as pd


def transform_nbp_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clear and prepare NBP data for Parquet storage.
    """
    if df.empty:
        print("WARNING: Received empty DataFrame for transformation.")
        return df

    print("INFO: Starting data transformation...")

    # 1. Data copy - No change to original DataFrame
    df = df.copy()

    # 2. Rename columns 
    column_map = {
        'currency': 'waluta',
        'code': 'kod_waluty',
        'mid': 'kurs_sredni',
        'DataNotowania': 'data_notowania'
    }
    df = df.rename(columns=column_map)

    # 3. datatype conversion (Parquet)
    # Convert string dates to datetime objects
    df['data_notowania'] = pd.to_datetime(df['data_notowania']).dt.date

    # Ensure exchange rate is a floating-point number
    df['kurs_sredni'] = pd.to_numeric(df['kurs_sredni'])

    # 4. ADD PARTITION COLUMNS (Essential for S3 Data Lake performance)
    # Extract year and month to enable physical partitioning in the storage layer
    df['rok'] = pd.to_datetime(df['data_notowania']).dt.year
    df['miesiac'] = pd.to_datetime(df['data_notowania']).dt.month

    # 5. Sort data for logical consistency
    df = df.sort_values(by=['data_notowania', 'kod_waluty'])

    # 6. Final column selection and ordering
    final_columns = ['data_notowania', 'rok', 'miesiac', 'kod_waluty', 'waluta', 'kurs_sredni']
    df = df[final_columns]

    print(f"INFO: Transformation complete. Processed {len(df)} rows.")
    return df


if __name__ == '__main__':
   # Unit test using Mock Data
    mock_data = pd.DataFrame([
        {'currency': 'dolar amerykański', 'code': 'USD', 'mid': 4.10, 'DataNotowania': '2025-12-15'},
        {'currency': 'euro', 'code': 'EUR', 'mid': 4.45, 'DataNotowania': '2025-12-15'}
    ])

    transformed_df = transform_nbp_data(mock_data)
    print("\n--- Transformed Data ---")
    print(transformed_df)
    print("\nColumn Datatypes:")
    print(transformed_df.dtypes)