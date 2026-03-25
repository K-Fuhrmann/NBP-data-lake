import os
import pandas as pd
import awswrangler as wr
import logging
from dotenv import load_dotenv

# Loading variables from .env
load_dotenv()

# Loading configuration
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
S3_REGION = os.getenv("S3_REGION")
S3_BASE_PATH = f"s3://{S3_BUCKET_NAME}/raw/nbp_kursy/"

def load_data_to_s3(df: pd.DataFrame, s3_path: str = S3_BASE_PATH):
    if df.empty:
        logging.warning("No data to upload to S3.")
        return

    logging.info(f"Starting upload of {len(df)} rows to AWS S3 at path: {s3_path}")

    try:
        wr.s3.to_parquet(
            df=df,
            path=s3_path,
            dataset=True,
            partition_cols=['rok', 'miesiac'],
            mode="append",
            boto3_session=None #  AWS CLI
        )
        logging.info("SUCCESS: Data has been written to the Data Lake.")
    except Exception as e:
        logging.error(f"ERROR AWS: Failed to upload data. Details: {e}")
        raise # Send error to main.py