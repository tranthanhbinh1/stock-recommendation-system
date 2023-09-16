from .get_fin_statement import GetFinancialStatement
from .get_vn100 import get_vn100_symbols

# Write logic here


def main():
    vn100 = get_vn100_symbols()
    fin_stm_type = ["BalanceSheet", "IncomeStatement", "CashFlow"]
    fin_page = [0, 8, 16]

    for symbol in vn100:
        for type in fin_stm_type:
            for page in fin_page:
                get_fin_instance = GetFinancialStatement(
                    organ_code=symbol, statement_type=type, page=page)
            

if __name__ == "__main__":
    main()
