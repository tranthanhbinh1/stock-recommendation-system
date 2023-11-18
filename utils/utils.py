# import logging
import re

def convert_timestamp(timestamp_str):
    import pandas as pd
    # extract the timestamp
    timestamp = int(timestamp_str.strip('/Date()'))
    # convert to datetime
    datetime_obj = pd.to_datetime(timestamp, unit='ms')
    return datetime_obj

def convert_camel_to_snake(input_str: str) -> str:
    result = re.sub(r"(?<=[a-z])(?=[A-Z])", "_", input_str).lower()
    return result

