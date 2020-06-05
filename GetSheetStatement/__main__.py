# packages
import os
import time
import random
import datetime

# project class
from .ProfitLossSheet import ProfitLossSheet
from .BalanceSheet import BalanceSheet
from .CashFlowSheet import CashFlowThread

# global value
_year = 2013  # IFRs後報表為102年後
_season = 1
now = datetime.datetime.now()
SHEET_DIR = ["Balance", "ProfitLossSheet", "CashFlow"]


# check data is all updating
def check_data_latest():
    file_path = f"./MOPS/"
    file_list = list()
    try:
        # In each sheet, year, season, check files exist
        for sheet in SHEET_DIR:
            for year in range(_year, now.year + 1):
                for season in range(1, 5):
                    temp_path = f"{file_path}{sheet}/{year}/0{season}/"
                    if not os.path.exists(temp_path):
                        file_list.append(temp_path)

        print(file_list)
    except NotADirectoryError as nade:
        print(f"NotADirectoryError, MSG: {nade}")
    except Exception as e:
        print(f"Walking file in {file_path} Failed.\nMSG: {e}")
    finally:
        # If not exist, set ETL thread
        if len(file_list) <= 0:
            print("All Data are latest")
        else:
            sheet_threads = list()
            for file_path in file_list:
                sheet_threads.append(sheet_thread_set(file_path))

            start_jobs(sheet_threads)


# Set Thread which lost in each season
# param file_path: str
#   The lost data in each season
# return threads: list
#   Get Data Thread List
def sheet_thread_set(file_path: str):
    threads = list()
    _sheet = file_path.split("/")[2]
    _year = int(file_path.split("/")[3])
    _season = int(file_path.split("/")[4])

    if _sheet == SHEET_DIR[0]:
        thread = BalanceSheet("Balance_Sheet", (_year-1911), _season)
        thread.setName(f"Balance_Sheet_{(_year-1911)}_{ _season}")
    elif _sheet == SHEET_DIR[1]:
        thread = ProfitLossSheet("Profit_and_Loss_Account", (_year-1911), _season)
        thread.setName(f"Profit_and_Loss_Account{(_year - 1911)}_{_season}")
    elif _sheet == SHEET_DIR[2]:
        thread = CashFlowThread("Cash_Flow_Statement", (_year-1911), _season)
        thread.setName(f"Cash_Flow_Statement{(_year - 1911)}_{_season}")
    else:
        thread = None

    now = datetime.datetime.now()
    if _year == now.year:
        now_season = (now.month % 12) // 3
        if _season >= now_season:
            thread = None

    if thread is not None:
        thread.start()
        threads.append(thread)

    return threads


# Start to run each thread
# param sheet_thread_list: list
#   The thread list for get each sheet data
def start_jobs(sheet_thread_list: list):
    for threads in sheet_thread_list:
        if len(threads) <= 0:
            continue
        try:
            for thread in threads:
                if thread.is_alive():
                    thread.join()
        except Exception as e:
            print(f"Thread Starting Error: {e}")

    print(f"--- Financial Get Complete. ---\nSleep 5sec...")
    time.sleep(5)
