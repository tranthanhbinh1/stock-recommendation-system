# import logging

# Convert column names from CamelCase to snake_case to follow database naming convention
def camel_to_snake(name):
    import re
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()

def convert_timestamp(timestamp_str):
    import pandas as pd
    # extract the timestamp
    timestamp = int(timestamp_str.strip('/Date()'))
    # convert to datetime
    datetime_obj = pd.to_datetime(timestamp, unit='ms')
    return datetime_obj
