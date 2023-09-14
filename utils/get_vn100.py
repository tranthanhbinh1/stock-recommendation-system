import requests
import json

def get_vn100_symbols() -> list:
    url = "https://www.hsx.vn/Modules/Listed/Web/StockIndex/188803177?_search=false&nd=1694679412209&rows=2147483647&page=1&sidx=id&sord=desc"

    headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'en-US,en;q=0.9,vi;q=0.8',
    'Connection': 'keep-alive',
    'Cookie': 'ASP.NET_SessionId=d4fuebfaoh2dn2e3gce2pvz4; TS016df111=01343ddb6a89a1cd8885933718f1fc42ddcb0ae7925e02d98c86dae32a0a0d2a3b7813d72cab00d1f34d15de9ebf36419959f7f3f942761f7b560cf780abaf7941f9d108aa; _ga=GA1.1.1492025135.1694679217; _ga_3Z6T19EH14=GS1.1.1694679216.1.1.1694679398.0.0.0; TS0d710d04027=085cef26a9ab20004f0fc402d97b0437204581898afdb4039f0d5e48fd038422192ab817eccc3c1b08cfc7c5c21130003deb1d509ff1ece024ccb4be45d4703ad807005f2ff916b1a2c7cd7cff13fdf6600a06f36fd4f1ee05da15766e86217d; TS016df111=01343ddb6a996d855bc9970cebbb65f15798d0db3837262899df1a8c83208b9165e1895d89b77814adf1666c1243db9346b6fcae44e89da306cbfb2b09de6cb153e55ea657; TS0d710d04027=085cef26a9ab200013444d0895c4b8d13f2206586b9ff424af1d764007b4f37b95f680f617717db0085792af33113000995ff5432f7d60201e6643b2aa3d62691ebffd6e34b4975a09c54febb4ebcdbf4cf2143082858924b475543211afd7d2',
    'Referer': 'https://www.hsx.vn/Modules/Listed/Web/StockIndexView/188803177',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.76',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Microsoft Edge";v="116"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"'
    }

    response = requests.request("GET", url, headers=headers)
    data = response.json()

    rows = data["rows"]
    symbols_lst = []
    symbols_dict = {}
    for val in rows:
        cell = val["cell"]
        symbols_lst.append(str(cell[2]).strip())
        symbols_dict[str(cell[2]).strip()] = str(cell[5])
        
    return symbols_lst

