import requests
import json
from config.default import (
    vietstock_header,
    vietstock_token,
    CPI_REFERER,
    EX_IN_RATES_REFERER,
    CPI_PAYLOAD,
    EX_IN_PAYLOAD,
)


import requests

url = "https://finance.vietstock.vn/data/reportdatatopbynormtype"

payload = "type=3&fromYear=2017&toYear=2023&from=1&to=3&normTypeID=43&page=0&pages=0&__RequestVerificationToken=4Yf9wTJpMyzwDt_B-v8ymG5Snj_grIzovmEnvdaJCGsJUyCzoynrDPYr5AFT_cOU0th3uKFoJMgZ5Z_xGEK7YX9KB8nmeeLW4CDxbApOEXC-8KtCQEogxGJgfq2btV7s1Z4AM0GFIMLjogs8ZlaajA2"
headers = {
  'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
  'Cookie': 'ASP.NET_SessionId=4asce003hqjtvz04znp35z3d; __RequestVerificationToken=vZDaJa5OJFBPweE7FImnak_oVGBkN1hAYKhoziURMBmXHq9qWeEI-k4pmgV1MvHxvuPLGlJV6Puin5CnVq01N8uJM2TOweVXfZtB3xJNxvk1; Theme=Light; _ga=GA1.1.1833990620.1696654322; language=en-US; AnonymousNotification=; vts_usr_lg=21AEC8FA62123721AC65A2E47817E2DE669DB1D9ED464B7B851DBAD0180B9FD3A3365989A7C498EE5BC99C1D08AB991FAF1032CD1E492DC1738F52E87B31E0979E288D25560901BA92693BB0C0AC34DA31C5CF8E9B193BAF16E75801817B755D0A11E3246D6CC4C9EE2F42BEFD4092797AFAF1DB2D3928913737AF883DC1529F86363787C577896E44FEBBD4EAEC19B9; _pbjs_userid_consent_data=3524755945110770; dable_uid=undefined; _ga_EXMM0DKVEX=GS1.1.1697124297.15.1.1697124992.60.0.0; ASP.NET_SessionId=0tc3mq5tmbd255ewzg5eud12; __RequestVerificationToken=X-hano-1HaJGBJz3ggMpn6lDgl0BPCkS1ynp8mVM8fjqWYlVDj2cfc66SI5-VW0SHrYV6kK_bLuneQSGb6-Oo6CX1fjM0AvhWDSiTBsjrFE1; language=vi-VN',
  'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.55'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)

