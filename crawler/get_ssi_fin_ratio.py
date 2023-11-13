from crawler.get_vn100 import get_vn100_symbols
from config.logging_config import setup_logging
from utils.timescale_connector import TimescaleConnector
from config.default import SSI_HEADERS
from datetime import datetime
from dataclasses import dataclass
import requests
import logging
import pandas as pd


@dataclass
class GetFinRatio():
    DEFAULT_URL = "https://fiin-fundamental.ssi.com.vn/FinancialAnalysis/GetFinancialRatioV2"
    
    @classmethod
    def get_financial_ratios(
        lang
    )