MOPS_URL = "https://mops.twse.com.tw/mops/web/{sheet}"

HEADERS = {
    'Referer': 'https://mops.twse.com.tw/mops/web/t164sb03',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'
}

FINANCIAL_STATMENT = {
    "Balance": "ajax_t164sb03",  # 資產負債表
    "Profit_and_Loss_Account": "ajax_t163sb04",  # 綜合損益表
    "Cash_Flow_Statement": "ajax_t164sb05"  # 現金流量表
}

PAYLOAD = {
    'encodeURIComponent': 1,
    'step': 1,
    'firstin': 1,
    'off': 1,
    'queryName': 'co_id',
    'inpuType': 'co_id',
    'isnew': 'false',
    'co_id': '2330',
    'TYPEK': 'all',
    'year': 109,
    'season': '02'
}

FILE_PATH = "./{sheet}/{sid}-{year}-{season}.json"
