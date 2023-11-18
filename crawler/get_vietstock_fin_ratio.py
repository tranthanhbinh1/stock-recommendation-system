import requests
import logging
import time
from dataclasses import dataclass
from crawler.get_vn100 import get_vn100_symbols
from config.default import VIET_STOCK_HEADERS
from config.logging_config import setup_logging
from utils.mongo_connector import MongoConnector
from typing import Literal


@dataclass
class VietstockFinRatio():
    DEFAULT_HEADERS = VIET_STOCK_HEADERS
    DEFAULT_URL = 