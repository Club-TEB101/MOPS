import os

import pandas as pd
import requests
from bs4 import BeautifulSoup

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


def main():
    global headers, payload
    resp = requests.post('https://mops.twse.com.tw/mops/web/ajax_t163sb04', data=payload, headers=headers, timeout=2)
    soup = BeautifulSoup(resp.text, 'html.parser')
    tables = soup.find_all('table')
    for k in range(1, len(tables)):
        data = []
        rows = tables[k].find_all('tr')
        columns = rows[0].find_all('th')
        columns_list = [columns[i].text for i in range(len(columns))]
        print(len(rows) - 1)
        for j in range(1, len(rows)):
            data_row = [rows[j].find_all('td')[i].text for i in range(len(columns))]
            data.append(data_row)
            # print(data_row)
            write_to_file(stock_code=k, rows=data, columns=columns_list)


def write_to_file(stock_code, columns, rows):
    df = pd.DataFrame(data=rows, columns=columns)
    try:
        if not os.path.isdir('./mops'):
            os.mkdir('./mops')
    except Exception as e:
        print(f"{e}")
    finally:
        # ./mops/{YYYY}/{stock_code}/{SS}.csv
        df.to_csv(f"./mops/{payload['year'] + 1911}/{str(stock_code)}/{payload['season']}.csv",
                  index=False,
                  encoding='utf-8-sig')
