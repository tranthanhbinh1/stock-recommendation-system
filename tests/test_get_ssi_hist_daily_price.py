import unittest
from datetime import datetime
from unittest.mock import patch

import pandas as pd
import requests
from get_ssi_hist_daily_price import SSIHistoricalDailyPrice


class TestSSIHistoricalDailyPrice(unittest.TestCase):
    @patch("get_ssi_hist_daily_price.requests.get")
    def test_get_historical_daily_price_success(self, mock_get):
        # Mock the response from requests.get
        mock_response = {
            "t": [1643836800, 1643923200],
            "o": [100.0, 200.0],
            "h": [150.0, 250.0],
            "l": [50.0, 150.0],
            "c": [120.0, 220.0],
            "v": [1000, 2000],
        }
        mock_get.return_value.json.return_value = mock_response

        # Set the expected result
        expected_result = pd.DataFrame(
            {
                "symbol": ["ABC", "ABC"],
                "date": ["2022-02-03 00:00:00", "2022-02-04 00:00:00"],
                "open": [100.0, 200.0],
                "high": [150.0, 250.0],
                "low": [50.0, 150.0],
                "close": [120.0, 220.0],
                "volume": [1000, 2000],
            }
        )

        # Call the method under test
        result = SSIHistoricalDailyPrice.get_historical_daily_price("ABC")

        # Assert the result
        pd.testing.assert_frame_equal(result, expected_result)

    @patch("get_ssi_hist_daily_price.requests.get")
    def test_get_historical_daily_price_no_data(self, mock_get):
        # Mock the response from requests.get
        mock_response = {}
        mock_get.return_value.json.return_value = mock_response

        # Call the method under test
        result = SSIHistoricalDailyPrice.get_historical_daily_price("ABC")

        # Assert the result is None
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
