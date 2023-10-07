import os
from dotenv import load_dotenv

# load_dotenv()

# S3_ACCESS_KEY=os.environ["S3_ACCESS_KEY"]
# S3_ENDPOINT=os.environ["S3_ENDPOINT"]   
# S3_SECRET_KEY=os.environ["S3_SECRET_KEY"]

vietstock_header ={
  'Accept': '*/*',
  'Accept-Language': 'en-US,en;q=0.9,vi;q=0.8',
  'Connection': 'keep-alive',
  'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
  'Cookie': 'language=vi-VN; ASP.NET_SessionId=4asce003hqjtvz04znp35z3d; __RequestVerificationToken=vvZDaJa5OJFBPweE7FImnak_oVGBkN1hAYKhoziURMBmXHq9qWeEI-k4pmgV1MvHxvuPLGlJV6Puin5CnVq01N8uJM2TOweVXfZtB3xJNxvk1; Theme=Light; _ga=GA1.1.1833990620.1696654322',
  'Origin': 'https://finance.vietstock.vn',
  'Referer': "{referer}",
  'Sec-Fetch-Dest': 'empty',
  'Sec-Fetch-Mode': 'cors',
  'Sec-Fetch-Site': 'same-origin',
  'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.47',
  'X-Requested-With': 'XMLHttpRequest',
  'sec-ch-ua': '"Microsoft Edge";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Linux"'
}

vietstock_token = "MdYzq9U0OkX8tn3UPvNmTOBbvEqf6_JFl--0Yq_VDv4MdBw97B4FjH7zFEf0ytg1FhtqzBpkNvYsWrnY46ZXt9Ur93zJ5VdyWkMEZhOzh-P6vIQEEuKTV2lgoh2aFaQGtyioAeVlI-Nvrhl8N-lWbg2"
CPI_REFERER = "https://finance.vietstock.vn/du-lieu-vi-mo/52/cpi.htm"
EX_IN_RATES_REFERER = "https://finance.vietstock.vn/du-lieu-vi-mo/53-64/ty-gia-lai-suat.htm"
CPI_PAYLOAD = "type=2&formYear={from_year}&toYear={to_year}&from=1&to=9&normTypeID=52&page=0&pages=0&__RequestVerificationToken={token}"
EX_IN_PAYLOAD = "type=1&fromYear={from_year}&toYear={to_year}from=2022-01-01&to=2022-12-31&normTypeID=53&page=0&pages=0&__RequestVerificationToken={token}"