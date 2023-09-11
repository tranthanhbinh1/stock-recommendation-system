import typing
import requests
import io
import pandas as pd

class get_financial_statement:
    def __init__(self, organ_code: str, statement_type: typing.Literal("BalanceSheet", "IncomeStatement")):
        organ_code = "VCB"
        page = 0
        fin_statement_type = "BalanceSheet"

        url = f"https://fiin-fundamental.ssi.com.vn/FinancialStatement/Download{fin_statement_type}?language=en&OrganCode={organ_code}&Skip={page}&Frequency=Quarterly"

        headers = {
        'authority': 'fiin-fundamental.ssi.com.vn',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9,vi;q=0.8',
        'access-control-request-headers': 'content-type,x-fiin-key,x-fiin-seed,x-fiin-user-id',
        'access-control-request-method': 'GET',
        'origin': 'https://iboard.ssi.com.vn',
        'referer': 'https://iboard.ssi.com.vn/',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.76',
        'Cookie': '__cf_bm=DTCnVdL.ZYR5Qb68BHPnX_vbWURBrOKVBPNboZGMkwQ-1694345120-0-AXeE6idhxc1Z0SHIK7m50wA6Nc13DQfj+gW62Oi5omSL7qpP1NWjh5cmjnVCpO4FDK/DWbsOeSIt1/TQ3BRWCEI='
        }

        response = requests.request("GET", url, headers=headers)
        
        with io.BytesIO(response.content) as buffer:  # Or define and append on buffer
            df = pd.read_excel(buffer, engine="openpyxl")
            
        # Drop NaN values
        df = df.dropna()
        # Reset and drop Indexes
        df = df.reset_index(drop=True)
        # Tranpose and reset the index again
        df = df.transpose().reset_index(drop=True)
        # Set the first row as headers
        new_headers = df.iloc[0]
        df = df[1:]
        df.columns = new_headers
        # Change "ITEMS" to "Quarter"
        df = df.rename(columns={"ITEMS": "Quarter"})
        # Reverse the order 
        df = df.iloc[::-1]
        df = df.reset_index(drop=True)
            
        # Transform DF to Parquet and upload to S3
        