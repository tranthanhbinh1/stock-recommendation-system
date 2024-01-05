import os
from dotenv import load_dotenv

load_dotenv()

VIET_STOCK_HEADERS = {
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Cookie": "ASP.NET_SessionId=4asce003hqjtvz04znp35z3d; __RequestVerificationToken=vZDaJa5OJFBPweE7FImnak_oVGBkN1hAYKhoziURMBmXHq9qWeEI-k4pmgV1MvHxvuPLGlJV6Puin5CnVq01N8uJM2TOweVXfZtB3xJNxvk1; Theme=Light; _ga=GA1.1.1833990620.1696654322; language=en-US; AnonymousNotification=; vts_usr_lg=21AEC8FA62123721AC65A2E47817E2DE669DB1D9ED464B7B851DBAD0180B9FD3A3365989A7C498EE5BC99C1D08AB991FAF1032CD1E492DC1738F52E87B31E0979E288D25560901BA92693BB0C0AC34DA31C5CF8E9B193BAF16E75801817B755D0A11E3246D6CC4C9EE2F42BEFD4092797AFAF1DB2D3928913737AF883DC1529F86363787C577896E44FEBBD4EAEC19B9; _pbjs_userid_consent_data=3524755945110770; dable_uid=undefined; _ga_EXMM0DKVEX=GS1.1.1697155153.17.1.1697155289.59.0.0; language=vi-VN",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.55",
}

SSI_HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}

SSI_FIIN_HEADERS = {
    "authority": "fiin-fundamental.ssi.com.vn",
    "accept": "application/json",
    "accept-language": "en-US,en;q=0.9,vi;q=0.8",
    "content-type": "application/json",
    "origin": "https://iboard.ssi.com.vn",
    "referer": "https://iboard.ssi.com.vn/",
    "sec-ch-ua": '"Microsoft Edge";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0",
    "x-fiin-key": "KEY",
    "x-fiin-seed": "SEED",
    "x-fiin-user-id": "ID",
}

FIREANT_HEADERS = {
    "authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6IkdYdExONzViZlZQakdvNERWdjV4QkRITHpnSSIsImtpZCI6IkdYdExONzViZlZQakdvNERWdjV4QkRITHpnSSJ9.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmZpcmVhbnQudm4iLCJhdWQiOiJodHRwczovL2FjY291bnRzLmZpcmVhbnQudm4vcmVzb3VyY2VzIiwiZXhwIjoxODg5NjIyNTMwLCJuYmYiOjE1ODk2MjI1MzAsImNsaWVudF9pZCI6ImZpcmVhbnQudHJhZGVzdGF0aW9uIiwic2NvcGUiOlsiYWNhZGVteS1yZWFkIiwiYWNhZGVteS13cml0ZSIsImFjY291bnRzLXJlYWQiLCJhY2NvdW50cy13cml0ZSIsImJsb2ctcmVhZCIsImNvbXBhbmllcy1yZWFkIiwiZmluYW5jZS1yZWFkIiwiaW5kaXZpZHVhbHMtcmVhZCIsImludmVzdG9wZWRpYS1yZWFkIiwib3JkZXJzLXJlYWQiLCJvcmRlcnMtd3JpdGUiLCJwb3N0cy1yZWFkIiwicG9zdHMtd3JpdGUiLCJzZWFyY2giLCJzeW1ib2xzLXJlYWQiLCJ1c2VyLWRhdGEtcmVhZCIsInVzZXItZGF0YS13cml0ZSIsInVzZXJzLXJlYWQiXSwianRpIjoiMjYxYTZhYWQ2MTQ5Njk1ZmJiYzcwODM5MjM0Njc1NWQifQ.dA5-HVzWv-BRfEiAd24uNBiBxASO-PAyWeWESovZm_hj4aXMAZA1-bWNZeXt88dqogo18AwpDQ-h6gefLPdZSFrG5umC1dVWaeYvUnGm62g4XS29fj6p01dhKNNqrsu5KrhnhdnKYVv9VdmbmqDfWR8wDgglk5cJFqalzq6dJWJInFQEPmUs9BW_Zs8tQDn-i5r4tYq2U8vCdqptXoM7YgPllXaPVDeccC9QNu2Xlp9WUvoROzoQXg25lFub1IYkTrM66gJ6t9fJRZToewCt495WNEOQFa_rwLCZ1QwzvL0iYkONHS_jZ0BOhBCdW9dWSawD6iF1SIQaFROvMDH1rg",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
}

GDP_PAYLOAD = "type=3&fromYear={from_year}&toYear={to_year}&from={from_quarter}&to={to_quarter}&normTypeID=43&page=0&pages=0&__RequestVerificationToken=xTqpS5pkIIC6a9mSLYN_mexBwEhFGqK2UiRPKtjNbkMAya_pVeI7mt54TrPD_SGIwu8yog9ivFLBDuKwO74t1PmJvkCrbLm-JFXFYVsCaEWvWmgvjhw4ygTM4I--fD2s37W8rqNCgfdCnzz-dj78oA2"
CPI_PAYLOAD = "type=2&fromYear={from_year}&toYear={to_year}&from={from_month}&to={to_month}&normTypeID=52&page=0&pages=0&__RequestVerificationToken=xTqpS5pkIIC6a9mSLYN_mexBwEhFGqK2UiRPKtjNbkMAya_pVeI7mt54TrPD_SGIwu8yog9ivFLBDuKwO74t1PmJvkCrbLm-JFXFYVsCaEWvWmgvjhw4ygTM4I--fD2s37W8rqNCgfdCnzz-dj78oA2"
EX_PAYLOAD = "type=1&fromYear={from_year}&toYear={to_year}&from={from_date}&to={to_date}&normTypeID=53&page=0&pages=0&__RequestVerificationToken=xTqpS5pkIIC6a9mSLYN_mexBwEhFGqK2UiRPKtjNbkMAya_pVeI7mt54TrPD_SGIwu8yog9ivFLBDuKwO74t1PmJvkCrbLm-JFXFYVsCaEWvWmgvjhw4ygTM4I--fD2s37W8rqNCgfdCnzz-dj78oA2"
IN_PAYLOAD = "type=1&fromYear={from_year}&toYear={to_year}&from={from_date}&to={to_date}&normTypeID=66&page=0&pages=0&__RequestVerificationToken=xTqpS5pkIIC6a9mSLYN_mexBwEhFGqK2UiRPKtjNbkMAya_pVeI7mt54TrPD_SGIwu8yog9ivFLBDuKwO74t1PmJvkCrbLm-JFXFYVsCaEWvWmgvjhw4ygTM4I--fD2s37W8rqNCgfdCnzz-dj78oA2"
SSI_OHLCV_HISTORY = "https://iboard.ssi.com.vn/dchart/api/history"
SSI_DOWNLOAD_FIN_RATIO_URL = "https://fiin-fundamental.ssi.com.vn/FinancialAnalysis/DownloadFinancialRatio2?language=en&OrganCode={symbol}&CompareToIndustry=false&Frequency=Quarterly&Ratios=ryd21&Ratios=ryd25&Ratios=ryd26&Ratios=ryd28&Ratios=ryd14&Ratios=ryd7&Ratios=ryd30&Ratios=rev&Ratios=isa22&Ratios=ryq27&Ratios=ryq29&Ratios=ryq25&Ratios=ryq12&Ratios=ryq14&Ratios=ryq76&Ratios=ryq3&Ratios=ryq1&Ratios=ryq2&Ratios=ryq77&Ratios=ryq31&Ratios=ryq91&Ratios=ryq16&Ratios=ryq18&Ratios=ryq20&Ratios=cashCycle&Ratios=ryq10&Ratios=ryq6&Ratios=ryq71&Ratios=ryd11&Ratios=ryd3&TimeLineFrom={timeline_from}"

# DATABASE CONNECTIONS
TS_HOST = os.environ["TS_HOST"]
TS_PORT = os.environ["TS_PORT"]
TS_USERNAME = os.environ["TS_USERNAME"]
TS_PASSWORD = os.environ["TS_PASSWORD"]
TS_DATABASE = os.environ["TS_DATABASE"]

# MONGO_HOST = os.environ["MONGO_HOST"]
# MONGO_PORT = os.environ["MONGO_PORT"]
# MONGO_USERNAME = os.environ["MONGO_USERNAME"]
# MONGO_PASSWORD = os.environ["MONGO_PASSWORD"]
# MONGO_AUTH_DB = os.environ["MONGO_AUTH_DB"]
