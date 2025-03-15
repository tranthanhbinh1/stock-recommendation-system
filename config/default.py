import os
from dotenv import load_dotenv
from typing import Literal

load_dotenv()

VIET_STOCK_HEADERS = {
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Cookie": "ASP.NET_SessionId=hhqxe2uikmsba1a2nkx43zcg; __RequestVerificationToken=e9T6xAGiBU0Oef2nIeDhxMizCiPUSVSTsp0zBgMJjRgygs4zDISTsImYQ-_CYaDrHR25ygn80nJA9btHYnxfEchCinaqc23_EIFm3P7et401; CookieNewsFirt=0; _ga=GA1.1.1089638179.1742021198; isShowLogin=true; _ga_EXMM0DKVEX=GS1.1.1742021197.1.1.1742021215.42.0.0",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.55",
}

SSI_HEADERS = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en,vi;q=0.9,en-US;q=0.8,zh-CN;q=0.7,zh;q=0.6',
    'origin': 'https://iboard.ssi.com.vn',
    'priority': 'u=1, i',
    'referer': 'https://iboard.ssi.com.vn/',
    'sec-ch-ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
    'Cookie': '__cf_bm=t7wQxTbdZu20dl0uHEfFD5WBlTkQnABCKiLP0uBChKc-1742022870-1.0.1.1-wI6fgwQfplnOixdk5Se36j75eF7AjhS_HcKx7oVKtZcEXpWm15Ce4I4HzvGFxdBsOVXO7FwVekEroqF4WWlVh8D9jUauRiLn.RoQtc1Fo2g; _cfuvid=r_hIh334vWqtOTV7A3cOZf01jAlpXz_sw2T7kUgDXAw-1742022870944-0.0.1.1-604800000'
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
# TS_HOST = os.environ["TS_HOST"]
# TS_PORT = os.environ["TS_PORT"]
# TS_USERNAME = os.environ["TS_USERNAME"]
# TS_PASSWORD = os.environ["TS_PASSWORD"]
# TS_DATABASE = os.environ["TS_DATABASE"]

# TS_HOST_2 = os.environ["TS_HOST_2"]
# TS_PORT_2 = os.environ["TS_PORT_2"]
# TS_USERNAME_2 = os.environ["TS_USERNAME_2"]
# TS_PASSWORD_2 = os.environ["TS_PASSWORD_2"]
# TS_DATABASE_2 = os.environ["TS_DATABASE_2"]

# MONGO_HOST = os.environ["MONGO_HOST"]
# MONGO_PORT = os.environ["MONGO_PORT"]
# MONGO_USERNAME = os.environ["MONGO_USERNAME"]
# MONGO_PASSWORD = os.environ["MONGO_PASSWORD"]
# MONGO_AUTH_DB = os.environ["MONGO_AUTH_DB"]

industries_type = Literal[
    "Dịch vụ tài chính",
    "Điện tử và thiết bị điện",
    "Kim loại",
    "Xây dựng và vật liệu",
    "Thiết bị, dịch vụ và phân phối dầu khí",
    "Bán lẻ",
    "Phần mềm và dịch vụ máy tính",
    "Hóa Chất",
    "Phần mềm dịch vụ máy tính",
    "Vận tải",
    "Lâm nghiệp và giấy",
    "Bất Động Sản",
    "Sản xuất thực phẩm",
    "Ngân hàng",
    "Dược phẩm",
    "Thiết bị và phần cứng",
    "Sản xuất và phân phối điện",
    "Sản xuất dược phẩm",
    "Du lịch và giải trí",
    "Sản xuất dầu khí",
    "Hàng cá nhân",
    "Công nghiệp nặng",
    "Nước và khí đốt",
    "Bảo hiểm nhân thọ",
    "Bia và đồ uống",
]
