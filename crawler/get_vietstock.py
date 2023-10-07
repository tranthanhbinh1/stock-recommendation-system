import requests
import json
from config.default import (
    vietstock_header,
    vietstock_token,
    CPI_REFERER,
    EX_IN_RATES_REFERER,
    CPI_PAYLOAD,
    EX_IN_PAYLOAD,
)


class VietstockMacroData:
    def __init__(self) -> None:
        self.default_url: str = (
            "https://finance.vietstock.vn/data/reportdatatopbynormtype"
        )
        self.default_header: str = vietstock_header  # format when use
        self.default_token: str = vietstock_token
        # self.from_year: str = None
        # self.to_year: str = None

    def get_cpi_data(self, from_year: int, to_year: int) -> None:
        cpi_payload = CPI_PAYLOAD.format(
            from_year=str(from_year), to_year=str(to_year), token=self.default_token
        )
        cpi_headers = self.default_header["Referer"].format(referer=CPI_REFERER)
        response = requests.post(self.default_url, cpi_headers, cpi_payload)
        print(response.status_code)
        with open("data/vietstock/cpi2.json", "w") as f:
            json.dump(response.json(), f, indent=2)

    def get_ex_in_rate_data(self, from_year: int, to_year: int) -> None:
        ex_in_payload = EX_IN_PAYLOAD.format(
            from_year=str(from_year), to_year=str(to_year), token=self.default_token
        )
        print(ex_in_payload)
        ex_in_headers = self.default_header["Referer"].format(referer=EX_IN_RATES_REFERER)
        response = requests.post(self.default_url, ex_in_headers, ex_in_payload)
        print(response)
        with open("data/vietstock/ex_in.json", "w") as f:
            json.dump(response.json(), f, indent=2)


if __name__ == "__main__":
    VietstockMacroData()
