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
    "authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6IkdYdExONzViZlZQakdvNERWdjV4QkRITHpnSSIsImtpZCI6IkdYdExONzViZlZQakdvNERWdjV4QkRITHpnSSJ9.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmZpcmVhbnQudm4iLCJhdWQiOiJodHRwczovL2FjY291bnRzLmZpcmVhbnQudm4vcmVzb3VyY2VzIiwiZXhwIjoxOTk4NDUzMTYzLCJuYmYiOjE2OTg0NTMxNjMsImNsaWVudF9pZCI6ImZpcmVhbnQud2ViIiwic2NvcGUiOlsib3BlbmlkIiwicHJvZmlsZSIsInJvbGVzIiwiZW1haWwiLCJhY2NvdW50cy1yZWFkIiwiYWNjb3VudHMtd3JpdGUiLCJvcmRlcnMtcmVhZCIsIm9yZGVycy13cml0ZSIsImNvbXBhbmllcy1yZWFkIiwiaW5kaXZpZHVhbHMtcmVhZCIsImZpbmFuY2UtcmVhZCIsInBvc3RzLXdyaXRlIiwicG9zdHMtcmVhZCIsInN5bWJvbHMtcmVhZCIsInVzZXItZGF0YS1yZWFkIiwidXNlci1kYXRhLXdyaXRlIiwidXNlcnMtcmVhZCIsInNlYXJjaCIsImFjYWRlbXktcmVhZCIsImFjYWRlbXktd3JpdGUiLCJibG9nLXJlYWQiLCJpbnZlc3RvcGVkaWEtcmVhZCJdLCJzdWIiOiI2MjA0Y2QxOC1jOGU1LTQwNTAtODhhZS1iZmJkNGFhNzRhZTIiLCJhdXRoX3RpbWUiOjE2OTg0NTMxNjMsImlkcCI6Ikdvb2dsZSIsIm5hbWUiOiJiaW5oeWVudmllbkBnbWFpbC5jb20iLCJzZWN1cml0eV9zdGFtcCI6IjE0ODI1NmNmLTViNGMtNDc2YS04ZjU2LTQ5MzUyZGQxMzUzYyIsImp0aSI6ImEzOGU1N2ExZjkwMWNmYTIwMDk2ZGY2NjhkNTAyYzM3IiwiYW1yIjpbImV4dGVybmFsIl19.JqyCjpltuNwA5YQKcWtm9CE6o0mFWlXjAeyLu61xewENK7ju7JMc9dJmKCfcCelFAztOi5bB3BkZ0D6xRSMq4vqG1Fexke8Oc3eoYcCoA9775Xm8DRb_jO7B_fErs9-oeRa17WLww32_JZGZAXn5lRAHEv9TuI73mrEVmfFqPKu6Li7OnSqnJdaHCc3zKlAacgV_N8_6ZQhhuXIB9cQ0_QhNyl0yvZMJ9RaI-SZbil0bFBQtB8Gx1vH1gRLrkmyRsDQMCCGBxJdbiJ6eE_m00TwSqyBAp_jk8KZGykWhsEvr2EX5VE2fqLOai5VE0aPJSM_wngv8Xs0IpzgelHg_pA",
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

MONGO_HOST = os.environ["MONGO_HOST"]
MONGO_PORT = os.environ["MONGO_PORT"]
MONGO_USERNAME = os.environ["MONGO_USERNAME"]
MONGO_PASSWORD = os.environ["MONGO_PASSWORD"]
MONGO_AUTH_DB = os.environ["MONGO_AUTH_DB"]
