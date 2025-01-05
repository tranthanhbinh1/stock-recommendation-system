import unittest
from io import BytesIO
from unittest.mock import patch

import pandas as pd
from get_ssi_fin_ratio import FinancialRatios


class TestFinancialRatios(unittest.TestCase):
    @patch("get_ssi_fin_ratio.requests.get")
    def test_get_financial_ratios_success(self, mock_get):
        # Mock the response from requests.get
        mock_response = (
            b"symbol,date,financial_ratio\nVIC,2022-01-01,1.5\nVIC,2022-01-02,2.0\n"
        )
        mock_get.return_value.content = mock_response

        # Set the expected result
        expected_result = pd.DataFrame(
            {
                "symbol": ["VIC", "VIC"],
                "date": ["2022-01-01", "2022-01-02"],
                "financial_ratio": [1.5, 2.0],
            }
        )

        # Call the method under test
        result = FinancialRatios.get_financial_ratios()

        # Assert the result
        pd.testing.assert_frame_equal(result, expected_result)

    @patch("get_ssi_fin_ratio.requests.get")
    def test_get_financial_ratios_failure(self, mock_get):
        # Mock the exception raised by requests.get
        mock_get.side_effect = Exception("Failed to get financial ratios")

        # Call the method under test
        result = FinancialRatios.get_financial_ratios()

        # Assert the result is an empty DataFrame
        self.assertTrue(result.empty)

    def test_get_financial_ratios_parse_error(self):
        # Set up a mock response with invalid data
        mock_response = (
            b"symbol,date,financial_ratio\nVIC,2022-01-01,1.5\nVIC,2022-01-02,invalid\n"
        )
        buffer = BytesIO(mock_response)

        # Call the method under test
        result = FinancialRatios.parse_excel(buffer)

        # Assert the result is an empty DataFrame
        self.assertTrue(result.empty)


if __name__ == "__main__":
    unittest.main()
