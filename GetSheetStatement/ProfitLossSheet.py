import os
import threading

import pandas as pd
import requests
from bs4 import BeautifulSoup as bs4
from requests.adapters import HTTPAdapter

from MOPS import Constract


class ProfitLossSheet(threading.Thread):

    def __init__(self, sheet, year, season):
        super().__init__()
        self.sheet = Constract.FINANCIAL_STATMENT[sheet]
        self.url = Constract.MOPS_URL.format(sheet=self.sheet)
        self.header = Constract.HEADERS
        self.payload = Constract.PAYLOAD
        self.payload["year"] = int(year)
        self.payload["season"] = f"0{season}"
        self.file_path = Constract.FILE_PATH.format(
            sheet="ProfitLossSheet", year=self.payload["year"] + 1911, season=self.payload["season"]
        )

        print(f"INIT Thread: Profit_and_Loss_Account\nURL: {self.url}\nFILE_PATH: {self.file_path}\n")
        pass

    def run(self):
        # set session retry option
        web_ss = requests.session()
        ss_adapter = HTTPAdapter(max_retries=3)
        web_ss.mount("https://", adapter=ss_adapter)

        # start get html
        res = web_ss.post(url=self.url, headers=self.header, data=self.payload, timeout=3)

        # check iff: Response OK
        if res.status_code == 200:
            soup = bs4(res.text, "html.parser")
            tables = soup.select("table[class='hasBorder']")
            self.process_data(tables)
        else:
            print(f"Get HTML FAIL: {res.status_code}, {res.reason}", end="\n\n")
            super().join(0)
        pass

    def process_data(self, tables):
        index = 1
        for table in tables:
            # print(table)
            table_columns = table.select("tr[class='tblHead'] > th")
            table_rows = table.select("tr[class='even']")
            if len(table_rows) <= 0:
                table_rows = table.select("tr[class='odd']")

            column_list = [column.text for column in table_columns]
            rows_list = [row for row in table_rows]
            total_list = list()
            for row in rows_list:
                temp = list()
                for td in row:
                    temp.append(td.text)
                total_list.append(temp)

            self.write_into_file(index, column_list, total_list)
            index += 1
        pass

    def write_into_file(self, index, columns, rows):
        df = pd.DataFrame(rows, columns=columns)
        print(f"{df}")
        print("---END---")
        try:
            os.makedirs(self.file_path, exist_ok=True)
        except Exception as e:
            print(f"[Error]Write Into File: {e}")
            super().join(0)
        finally:
            df.to_csv(f"{self.file_path}{index}.csv", index=False, encoding='utf-8-sig')
        pass
