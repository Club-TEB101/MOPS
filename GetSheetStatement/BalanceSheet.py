# libraries
import os
import requests
import threading
import pandas as pd
from bs4 import BeautifulSoup as bs4
from requests.adapters import HTTPAdapter

# from Project
from MOPS.GetSheetStatement import Constract


class BalanceSheet(threading.Thread):

    def __init__(self, sheet: str, year: int, season: int):
        super().__init__()
        self.sheet = Constract.FINANCIAL_STATMENT[sheet]
        self.url = Constract.MOPS_URL.format(sheet=self.sheet)
        self.header = Constract.HEADERS
        self.payload = Constract.PAYLOAD
        self.payload["year"] = int(year)
        self.payload["season"] = f"0{season}"
        self.file_path = Constract.FILE_PATH.format(
            sheet="Balance", year=self.payload["year"] + 1911, season=self.payload["season"]
        )

        print(f"INIT Thread: Balance_Sheet\nURL: {self.url}\nFILE_PATH: {self.file_path}\n")
        pass

    def run(self):
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
                tr_list = self.pre_process(soup)
                tables = soup.select("table[class='hasBorder']")
                self.process_data(tables, tr_list)
        except Exception as e:
            print(f"Get HTML FAIL: {e}", end="\n\n")
            super().join(0)
        pass

    # 因Soup處理有問題，所以改以人工獲取欄位及資料
    @staticmethod
    def pre_process(soup: bs4):
        # 取得所有欄位資料
        all_tr_list = soup.select("tr")

        # 設定欲傳回資料型態
        tr_list = dict()
        tr_list["columns"] = list()
        tr_list["rows"] = list()

        # 設定暫存清單
        temp_list = list()

        # 判斷每個欄位的 Class，如有不同則新增至傳回資料集(tr_list)，相同則先匯入暫存清單(temp_list)
        for i in range(len(all_tr_list)):
            current_tr_class = all_tr_list[i].attrs["class"]
            last_tr_class = current_tr_class \
                if len(temp_list) <= 0 \
                else temp_list[-1].attrs["class"]

            # 去除非必要欄位
            if current_tr_class[0] == "reportCont":
                continue

            # or 為加入最後取得之欄位清單
            if current_tr_class != last_tr_class or i == len(all_tr_list)-1:
                # debug用，印出暫存列表資料
                # print(f"current: {temp_list}\n --- END ---")
                if last_tr_class[0] == "tblHead":
                    tr_list["columns"].append(temp_list)
                else:
                    tr_list["rows"].append(temp_list)

                temp_list = list()

            temp_list.append(all_tr_list[i])
        return tr_list

    def process_data(self, tables: list, tr_list: dict):
        rows_data = list()
        for i in range(len(tables)):
            columns = tr_list["columns"][i][0]
            columns_list = columns.select("th")
            columns_data = [data.text for data in columns_list]
            for tr in tr_list["rows"][i]:
                td = tr.select("td")
                rows = [data.text for data in td]
                rows_data.append(rows)
            # print(f'C_Data: {columns_data}\n\nR_Data: {rows_data}')
            self.write_into_file(i, columns_data, rows_data)
            rows_data = list()

    def write_into_file(self, index: int, columns: list, rows: list):
        df = pd.DataFrame(rows, columns=columns)
        # print(f"{df}")
        # print("---END---")
        try:
            os.makedirs(self.file_path, exist_ok=True)
        except Exception as e:
            print(f"[Error]Write Into File: {e}")
            self.join(0)
        finally:
            df.to_csv(f"{self.file_path}{index}.csv", index=False, encoding='utf-8-sig')
        pass

    def join(self, timeout=None):
        print(f"{super().getName()} Joined.")
        if super().is_alive():
            super().join(timeout)
