import os
from dotenv import load_dotenv

load_dotenv()

S3_ACCESS_KEY=os.environ["S3_ACCESS_KEY"]
S3_ENDPOINT=os.environ["S3_ENDPOINT"]   
S3_SECRET_KEY=os.environ["S3_SECRET_KEY"]