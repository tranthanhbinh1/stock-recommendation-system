import logging
from io import BytesIO
import pandas

import boto3
import pandas as pd
from config.default import S3_ACCESS_KEY, S3_ENDPOINT, S3_SECRET_KEY    #TODO: Put them here

s3 = boto3.resource(
    "s3",
    endpoint_url=S3_ENDPOINT,
    aws_access_key_id=S3_ACCESS_KEY,
    aws_secret_access_key=S3_SECRET_KEY,
)

def df_to_s3_parquet(df: pandas.DataFrame, bucket_name: str, file_name: str):
    parquet_buffer = BytesIO()
    try:
        df.to_parquet(parquet_buffer)
        s3.Object(bucket_name, file_name).put(Body=parquet_buffer.getvalue())
        print("Upload successfully!")
    except Exception as e:
        print("Error: ", e)

def s3_parquet_to_df(bucket_name: str, file_name: str):
    try:
        obj = s3.Object(bucket_name, file_name)
        response = obj.get()
        file_content = response["Body"].read()
        buffer = BytesIO(file_content)
        df = pd.read_parquet(buffer)
        return df
    except Exception as e:
        logging.error(f"An error occurred while reading the parquet file: {e}")
        return None
