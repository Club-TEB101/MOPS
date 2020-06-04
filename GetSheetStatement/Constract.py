MOPS_URL = "https://mops.twse.com.tw/mops/web/{sheet}"

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/83.0.4103.61 Safari/537.36'
}

FINANCIAL_STATMENT = {
    "Balance_Sheet": "ajax_t163sb05",  # 資產負債表
    "Profit_and_Loss_Account": "ajax_t163sb04",  # 綜合損益表
    "Cash_Flow_Statement": "ajax_t164sb05"  # 現金流量表
}

PAYLOAD = {
    'encodeURIComponent': 1,
    'step': 1,
    'firstin': 1,
    'off': 1,
    'isQuery': 'Y',
    'TYPEK': 'sii',  # sii 上市 / otc 上櫃
    'year': 107,
    'season': '02'
}

FILE_PATH = "./MOPS/{sheet}/{year}/{season}/"
