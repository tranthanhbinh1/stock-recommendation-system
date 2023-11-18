import typing
import requests

StatementType = typing.Literal["BalanceSheet", "IncomeStatement", "CashFlow"]
PageType = typing.Literal[0, 8, 16]


class GetFinancialStatement:
    def __init__(self, symbol: str, statement_type: StatementType, page: PageType):
        self.symbol = symbol
        self.statement_type = statement_type
        self.page = page
        self.get_data()

    def get_data(self):
        url = f"https://fiin-fundamental.ssi.com.vn/FinancialStatement/Download{self.statement_type}?language=en&OrganCode={self.symbol}&Skip={self.page}&Frequency=Quarterly"

        headers = {
            "authority": "fiin-fundamental.ssi.com.vn",
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9,vi;q=0.8",
            "access-control-request-headers": "content-type,x-fiin-key,x-fiin-seed,x-fiin-user-id",
            "access-control-request-method": "GET",
            "origin": "https://iboard.ssi.com.vn",
            "referer": "https://iboard.ssi.com.vn/",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.76",
            "Cookie": "__cf_bm=DTCnVdL.ZYR5Qb68BHPnX_vbWURBrOKVBPNboZGMkwQ-1694345120-0-AXeE6idhxc1Z0SHIK7m50wA6Nc13DQfj+gW62Oi5omSL7qpP1NWjh5cmjnVCpO4FDK/DWbsOeSIt1/TQ3BRWCEI=",
        }

        response = requests.request("GET", url, headers=headers)

        if response.status_code == 200:
            with open(
                f"financial_statements/{self.page}/{self.statement_type}_{self.symbol}_{self.page}.xlsx", "wb"
            ) as f:
                f.write(response.content)

        # with io.BytesIO(response.content) as buffer:
        #     df = pd.read_excel(buffer, engine="openpyxl")

        #     # Reset and drop Indexes
        #     df = df.iloc[6:]
        #     df = df.reset_index(drop=True)
        #     # Tranpose and reset the index again
        #     df = df.transpose().reset_index(drop=True)
        #     # Set the first row as headers
        #     new_headers = df.iloc[0]
        #     df = df[1:]
        #     df.columns = new_headers
        #     df = df.rename(columns={"ITEMS": "Quarter"})

        #     # df = df.astype(str)
        #     df.columns = df.columns.astype(str)

        #     self.df = df  # Typecast all to string to -> parquet
        #     self.df.to_parquet(f"financial_statements/{self.statement_type}_{self.symbol}.parquet")
        # Transform DF to Parquet and upload to S3
        # TODO: add from_year and to_year
        # df_to_s3_parquet(df=self.df, bucket_name="fiinpro-api",
        #                  file_name=f"FinancialStatement/{self.statement_type}_{self.symbol}")


# if __name__ == "__main__":
# run_fin_statement = GetFinancialStatement("SSI", "BalanceSheet") #Test
