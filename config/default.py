import os
from dotenv import load_dotenv

load_dotenv()

VIET_STOCK_HEADERS = {
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Cookie": "ASP.NET_SessionId=4asce003hqjtvz04znp35z3d; __RequestVerificationToken=vZDaJa5OJFBPweE7FImnak_oVGBkN1hAYKhoziURMBmXHq9qWeEI-k4pmgV1MvHxvuPLGlJV6Puin5CnVq01N8uJM2TOweVXfZtB3xJNxvk1; Theme=Light; _ga=GA1.1.1833990620.1696654322; language=en-US; AnonymousNotification=; vts_usr_lg=21AEC8FA62123721AC65A2E47817E2DE669DB1D9ED464B7B851DBAD0180B9FD3A3365989A7C498EE5BC99C1D08AB991FAF1032CD1E492DC1738F52E87B31E0979E288D25560901BA92693BB0C0AC34DA31C5CF8E9B193BAF16E75801817B755D0A11E3246D6CC4C9EE2F42BEFD4092797AFAF1DB2D3928913737AF883DC1529F86363787C577896E44FEBBD4EAEC19B9; _pbjs_userid_consent_data=3524755945110770; dable_uid=undefined; _ga_EXMM0DKVEX=GS1.1.1697155153.17.1.1697155289.59.0.0; language=vi-VN",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.55",
}

GDP_PAYLOAD = "type=3&fromYear={from_year}&toYear={to_year}&from={from_quarter}&to={to_quarter}&normTypeID=43&page=0&pages=0&__RequestVerificationToken=xTqpS5pkIIC6a9mSLYN_mexBwEhFGqK2UiRPKtjNbkMAya_pVeI7mt54TrPD_SGIwu8yog9ivFLBDuKwO74t1PmJvkCrbLm-JFXFYVsCaEWvWmgvjhw4ygTM4I--fD2s37W8rqNCgfdCnzz-dj78oA2"
CPI_PAYLOAD = "type=2&fromYear={from_year}&toYear={to_year}&from={from_month}&to={to_month}&normTypeID=52&page=0&pages=0&__RequestVerificationToken=xTqpS5pkIIC6a9mSLYN_mexBwEhFGqK2UiRPKtjNbkMAya_pVeI7mt54TrPD_SGIwu8yog9ivFLBDuKwO74t1PmJvkCrbLm-JFXFYVsCaEWvWmgvjhw4ygTM4I--fD2s37W8rqNCgfdCnzz-dj78oA2"
EX_PAYLOAD = "type=1&fromYear={from_year}&toYear={to_year}&from={from_date}&to={to_date}&normTypeID=53&page=0&pages=0&__RequestVerificationToken=xTqpS5pkIIC6a9mSLYN_mexBwEhFGqK2UiRPKtjNbkMAya_pVeI7mt54TrPD_SGIwu8yog9ivFLBDuKwO74t1PmJvkCrbLm-JFXFYVsCaEWvWmgvjhw4ygTM4I--fD2s37W8rqNCgfdCnzz-dj78oA2"
IN_PAYLOAD = "type=1&fromYear={from_year}&toYear={to_year}&from={from_date}&to={to_date}&normTypeID=66&page=0&pages=0&__RequestVerificationToken=xTqpS5pkIIC6a9mSLYN_mexBwEhFGqK2UiRPKtjNbkMAya_pVeI7mt54TrPD_SGIwu8yog9ivFLBDuKwO74t1PmJvkCrbLm-JFXFYVsCaEWvWmgvjhw4ygTM4I--fD2s37W8rqNCgfdCnzz-dj78oA2"
# DATABASE CONNECTIONS
DB_HOST = os.environ["DB_HOST"]
DB_USERNAME = os.environ["DB_USERNAME"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_DATABASE = os.environ["DB_DATABASE"]
