import typing
import pandas as pd

class get_financial_statement:
    def __init__(self, organ_code: str, statement_type: typing.Literal("BalanceSheet", "IncomeStatement")):
        self.url = f"https://fiin-fundamental.ssi.com.vn/FinancialStatement/Download{statement_type}?language=en&OrganCode={organ_code}&Skip=1&Frequency=Quarterly"