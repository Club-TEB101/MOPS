# import library
import os
import time
import random
import pandas
import requests
import threading
from os import path, walk
from bs4 import BeautifulSoup as bs4
from requests.adapters import HTTPAdapter

# from project class
from ..stock_codes.codes import codes
from ..GetSheetStatement import Constract


class CashFlowThread(threading.Thread):

    def __init__(self, sheet: str, year: int, season: int):
        super().__init__()
        self.sheet = Constract.FINANCIAL_STATMENT[sheet]
        self.url = Constract.MOPS_URL.format(sheet=self.sheet)
        self.header = Constract.HEADERS
        self.payload = Constract.PAYLOAD
        self.payload["year"] = int(year)
        self.payload["season"] = f"0{season}"
        self.file_path = Constract.FILE_PATH.format(
            sheet="CashFlow", year=self.payload["year"] + 1911, season=self.payload["season"]
        )

        print(f"INIT Thread: Cash_Flow_Statement\nURL: {self.url}\nFILE_PATH: {self.file_path}\n")
        pass

    def run(self):
        stock_list = self.get_all_stock_code()
        # print(f"Stocks: {self.stock_list_in_season}\nSum: {len(self.stock_list_in_season)}\n\n")
        for stock in stock_list:
            self.etl(stock)
        pass

    def join(self, timeout=None):
        print(f"{super().getName()} Joined.")
        if super().is_alive():
            super().join(timeout)

    def get_all_stock_code(self):
        read_file_path = f"./MOPS/Balance/{self.payload['year'] + 1911}/{self.payload['season']}/"
        all_stock_in_season = pandas.DataFrame()
        try:
            for root, dir, files in walk(read_file_path):
                for file_name in files:
                    if 'csv' in file_name:
                        temp_df = pandas.read_csv(path.join(root, file_name), header=0)
                        all_stock_in_season = all_stock_in_season.append(temp_df)

        except Exception as e:
            print(f"Load Stock Code Failed: Loading in {read_file_path},\nMSG: {e}")
            self.join(0)
        finally:
            print(f"")
            return all_stock_in_season["公司代號"].tolist()

    def etl(self, code: int, retry=0):
        self.payload["co_id"] = f"{code}"

        # set session retry option
        web_ss = requests.session()
        ss_adapter = HTTPAdapter(max_retries=3)
        web_ss.mount("https://", adapter=ss_adapter)

        try:
            # start get html
            res = web_ss.post(url=self.url, headers=self.header, data=self.payload, timeout=3)
            # check iff: Response OK
            if res.status_code == 200:
                soup = bs4(res.text, "html.parser")
                kwsk = soup.select("input[value='詳細資料']")
                if len(kwsk) >= 0:
                    tables = self.preprocess()
                else:
                    tables = soup.select("table")
                if len(tables) > 0:
                    self.process_data(tables[1])
            else:
                print(f"Get HTML FAIL: {res.status_code}, {res.reason}", end="\n\n")
                super().join(0)
        except ConnectionAbortedError as e:
            print(f"Connection Abort: Sleep 5sec...\nMSG: {e}")
            self.etl(code, retry=retry+1) if retry >= 5 else self.join(0)
        pass

    def preprocess(self):
        tables = list()
        self.payload["step"] = 2
        ss_adapter = HTTPAdapter(max_retries=3)
        web_ss = requests.session()
        web_ss.mount("https://", adapter=ss_adapter)
        try:
            res = web_ss.post(url=self.url, headers=self.header, data=self.payload, timeout=3)
            soup = bs4(res.text, "html.parser")
            tables = soup.select("table")
        except Exception as e:
            print(f"Catch an Exception: {e}")
        finally:
            return tables

    def process_data(self, table):
        tr_list = table.select("tr")
        column_list = ["Columns", "Data"]
        row_list = list()

        for tr in tr_list:
            td_list = tr.select("td")
            temp_list = ["", 0]
            for td in td_list:
                if len(td_list) > 0 and td != td_list[2]:
                    temp_list.append(td)
                row_list.append(temp_list)
                temp_list = list()

        if len(row_list) > 0:
            self.write_into_file(column_list, row_list)
        pass

    def write_into_file(self, columns: list, rows: list):
        df = pandas.DataFrame(rows, columns=columns)
        print(f"{df}")

        try:
            os.makedirs(self.file_path, exist_ok=True)
        except Exception as e:
            print(f"[Error]Write Into File: {e}")
            self.join(0)
        finally:
            df.to_csv(f"{self.file_path}{self.payload['co_id']}.csv", index=False, encoding='utf-8-sig')
        pass
        pass
