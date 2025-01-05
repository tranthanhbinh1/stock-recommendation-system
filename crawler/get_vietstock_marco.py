import pandas as pd
import requests

from config.default import (
    CPI_PAYLOAD,
    EX_PAYLOAD,
    GDP_PAYLOAD,
    IN_PAYLOAD,
    VIET_STOCK_HEADERS,
)
from utils.utils import convert_timestamp


class VietstockCrawler:
    DEFAULT_HEADERS = VIET_STOCK_HEADERS
    DEFAULT_URL = "https://finance.vietstock.vn/data/reportdatatopbynormtype"

    @classmethod
    def vietstock_get_gdp(
        cls,
        from_year: str,
        to_year: str,
        from_quarter: str = "1",
        to_quarter: str = "3",
        URL: str = DEFAULT_URL,
        headers: dict = DEFAULT_HEADERS,
    ):
        payload = GDP_PAYLOAD.format(
            from_year=from_year,
            to_year=to_year,
            from_quarter=from_quarter,
            to_quarter=to_quarter,
        )
        response = requests.post(
            url=URL,
            data=payload,
            headers=headers,
        )
        data = response.json()["data"]
        if data is None:
            return None

        df = pd.DataFrame(data)
        df = pd.DataFrame.from_records(data)
        df["TernDay"] = df["TernDay"].apply(convert_timestamp)
        df.drop(columns=["CssStyle", "GroupName"], inplace=True)
        return df

    @classmethod
    def vietstock_get_cpi(
        cls,
        from_year: str,
        to_year: str,
        from_month: str = "1",
        to_month: str = "12",
        URL: str = DEFAULT_URL,
        headers: dict = DEFAULT_HEADERS,
    ):
        payload = CPI_PAYLOAD.format(
            from_year=from_year,
            to_year=to_year,
            from_month=from_month,
            to_month=to_month,
        )
        response = requests.post(
            url=URL,
            data=payload,
            headers=headers,
        )
        data = response.json()["data"]
        if data is None:
            return None

        df = pd.DataFrame(data)
        df = pd.DataFrame.from_records(data)
        df["TernDay"] = df["TernDay"].apply(convert_timestamp)
        df.drop(columns=["CssStyle", "GroupName"], inplace=True)
        return df

    @classmethod
    def vietstock_get_ex(
        cls,
        from_year: str = "2022",
        to_year: str = "2022",
        from_date: str = "2022-01-01",
        to_date: str = "2022-12-31",
        URL: str = DEFAULT_URL,
        headers: dict = DEFAULT_HEADERS,
    ):
        payload = EX_PAYLOAD.format(
            from_year=from_year,
            to_year=to_year,
            from_date=from_date,
            to_date=to_date,
        )
        response = requests.post(
            url=URL,
            data=payload,
            headers=headers,
        )
        data = response.json()["data"]
        if data is None:
            return None

        df = pd.DataFrame(data)
        df = pd.DataFrame.from_records(data)
        df["TernDay"] = df["TernDay"].apply(convert_timestamp)
        df.drop(columns=["CssStyle", "GroupName"], inplace=True)
        return df

    @classmethod
    def vietstock_get_in(
        cls,
        from_year: str = "2022",
        to_year: str = "2022",
        from_date: str = "2022-01-01",
        to_date: str = "2022-12-31",
        URL: str = DEFAULT_URL,
        headers: dict = DEFAULT_HEADERS,
    ):
        payload = IN_PAYLOAD.format(
            from_year=from_year,
            to_year=to_year,
            from_date=from_date,
            to_date=to_date,
        )
        response = requests.post(
            url=URL,
            data=payload,
            headers=headers,
        )
        data = response.json()["data"]
        if data is None:
            return None

        df = pd.DataFrame(data)
        df = pd.DataFrame.from_records(data)
        df["TernDay"] = df["TernDay"].apply(convert_timestamp)
        df.drop(columns=["CssStyle", "GroupName"], inplace=True)
        return df
