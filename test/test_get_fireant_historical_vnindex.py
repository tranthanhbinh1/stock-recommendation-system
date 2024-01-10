import unittest
from unittest.mock import patch
from datetime import datetime, timedelta
import pandas as pd

from get_fireant_historical_vnindex import FireantHistoricalVnIndex

class TestFireantHistoricalVnIndex(unittest.TestCase):
    @patch('get_fireant_historical_vnindex.requests.get')
    def test_get_fireant_historical_vnindex(self, mock_get):
        # Mock the response from requests.get
        mock_response = {
            "date": ["2022-01-01", "2022-01-02"],
            "priceOpen": [100.0, 200.0],
            "priceHigh": [150.0, 250.0],
            "priceLow": [50.0, 150.0],
            "priceClose": [120.0, 220.0],
            "totalVolume": [1000, 2000]
        }
        mock_get.return_value.json.return_value = mock_response

        # Set the expected result
        expected_result = pd.DataFrame({
            "date": ["2022-01-01", "2022-01-02"],
            "open": [100.0, 200.0],
            "high": [150.0, 250.0],
            "low": [50.0, 150.0],
            "close": [120.0, 220.0],
            "volume": [1000, 2000],
            "percent_change": [0.0, 83.33333333333334]
        })

        # Call the method under test
        result = FireantHistoricalVnIndex.get_fireant_historical_vnindex()

        # Assert the result
        pd.testing.assert_frame_equal(result, expected_result)

    @patch('get_fireant_historical_vnindex.FireantHistoricalVnIndex.get_fireant_historical_vnindex')
    def test_transform_data(self, mock_get_fireant_historical_vnindex):
        # Mock the result of get_fireant_historical_vnindex
        mock_result = pd.DataFrame({
            "date": ["2022-01-01", "2022-01-02"],
            "open": [100.0, 200.0],
            "high": [150.0, 250.0],
            "low": [50.0, 150.0],
            "close": [120.0, 220.0],
            "volume": [1000, 2000]
        })
        mock_get_fireant_historical_vnindex.return_value = mock_result

        # Set the expected result
        expected_result = pd.DataFrame({
            "date": ["2022-01-02", "2022-01-01"],
            "open": [200.0, 100.0],
            "high": [250.0, 150.0],
            "low": [150.0, 50.0],
            "close": [220.0, 120.0],
            "volume": [2000, 1000],
            "percent_change": [100.0, -45.45454545454545]
        })

        # Call the method under test
        result = FireantHistoricalVnIndex.transform_data()

        # Assert the result
        pd.testing.assert_frame_equal(result, expected_result)

if __name__ == '__main__':
    unittest.main()