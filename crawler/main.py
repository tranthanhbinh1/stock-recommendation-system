from .get_fin_statement import GetFinancialStatement
from .get_vn100 import get_vn100_symbols

# Write logic here


def main():
    vn100 = get_vn100_symbols()
    fin_stm_type = ["BalanceSheet", "IncomeStatement", "CashFlow"]
    fin_page = [24]
    # [8, 16, 24]

    for symbol in vn100:
        for type in fin_stm_type:
            for page in fin_page:
                try:
                    get_fin_instance = GetFinancialStatement(
                        organ_code=symbol, statement_type=type, page=page)
                    print("Successfully crawled data for: ", symbol, type, page)
                except Exception as e:
                    print("Error: ", e)
                
            

if __name__ == "__main__":
    main()
