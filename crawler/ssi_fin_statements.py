import requests
from utils.get_fin_statement import GetFinancialStatement
from utils.get_vn100 import get_vn100_symbols

# Write logic here

vn100 = get_vn100_symbols()
fin_stm_type = ["BalanceSheet", "IncomeStatement", "CashFlow"]

for symbol in vn100:
    for type in fin_stm_type:
        get_fin_instance = GetFinancialStatement(organ_code=symbol, statement_type=type)