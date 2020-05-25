import os

import pandas as pd
import requests
from bs4 import BeautifulSoup

url = "https://mops.twse.com.tw/mops/web/{}"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/81.0.4044.138 Safari/537.36'
}
payload = {
    'encodeURIComponent': 1,
    'step': 1,
    'firstin': 1,
    'off': 1,
    'isQuery': 'Y',
    'TYPEK': 'sii',  # sii 上市 / otc 上櫃
    'year': 107,
    'season': '02'
}
Financial_Statements = {
    "Balance_Sheet": "ajax_t163sb03",  # 資產負債表
    "Profit_and_Loss_Account": "ajax_t163sb04"  # 綜合損益表

}
# 現金流量表再另一個網址?
# "Cash_Flow_Statement": "ajax_t164sb05"


def main():
    global url, headers, payload, Financial_Statements
    for sheet in Financial_Statements:
        resp = requests.post(url.format(Financial_Statements[sheet]), data=payload, headers=headers, timeout=3)
        soup = BeautifulSoup(resp.text, 'html.parser')
        tables = soup.find_all('table')
        process_data(tables)


def process_data(sheet_table):
    for k in range(1, len(sheet_table)):
        data = []
        rows = sheet_table[k].find_all('tr')
        columns = rows[0].find_all('th')
        columns_list = [columns[i].text for i in range(len(columns))]
        # print(len(rows) - 1)
        for j in range(1, len(rows)):
            data_row = [rows[j].find_all('td')[i].text for i in range(len(columns))]
            data.append(data_row)
            # print(data_row)
            write_to_file(stock_code=k, rows=data, columns=columns_list)


def write_to_file(stock_code, columns, rows):
    file_path = f"./mops/{payload['year'] + 1911}/"
    df = pd.DataFrame(data=rows, columns=columns)
    try:
        if not os.path.exists(file_path):
            os.mkdir(file_path)
    except Exception as e:
        print(f"Create File Path Failed: {e}")
    finally:
        # ./mops/{year}_{season}_{stock_code}.csv
        df.to_csv(f"{file_path}{payload['season']}_{str(stock_code)}.csv",
                  index=False,
                  encoding='utf-8-sig')
