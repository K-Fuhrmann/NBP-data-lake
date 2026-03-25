import duckdb


def run_analysis():
    print("--- S3 DATA ANALYSIS (SECURE CONFIGURATION) ---")

    con = duckdb.connect()

    # 1. Load necessary extensions
    con.execute("INSTALL httpfs; LOAD httpfs;")
    con.execute("INSTALL aws; LOAD aws;")

    # 2. SECURE CONFIGURATION
    # Instead of hardcoding keys, we instruct DuckDB to fetch them from the AWS CLI
    try:
        con.execute("CALL load_aws_credentials();")
        con.execute("SET s3_region='eu-north-1';")  # Setting the region
    except Exception as e:
        print(f" Error loading AWS credentials: {e}")
        return

    bucket = 'moj-projekt-data-lake-nbp'
    full_path = f"s3://{bucket}/raw/nbp_kursy/**/*.parquet"

    print(f"INFO: Connecting to bucket: {bucket} in region eu-north-1")

    try:
        # Perform analysis across all partitioned files
        print("\n--- ANALYSIS RESULTS ---")
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
        print("\n Analysis completed successfully using system-level credentials.")

    except Exception as e:
        print(f" ANALYSIS ERROR: {e}")


if __name__ == "__main__":
    run_analysis()