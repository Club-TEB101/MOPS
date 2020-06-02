import datetime
import random
import time
from MOPS import BalanceSheet, ProfitLossSheet, Constract

if __name__ == '__main__':
    now = datetime.datetime.now()
    threads = list()
    for sheet in Constract.FINANCIAL_STATMENT:
        for year in range(102, (now.year - 1910)):
            for season in range(1, 5):
                if sheet == "Balance_Sheet":
                    thread = BalanceSheet.BalanceSheet(sheet, year, season)
                elif sheet == "Profit_and_Loss_Account":
                    thread = ProfitLossSheet.ProfitLossSheet(sheet, year, season)
                else:
                    thread = None

                if thread is not None:
                    threads.append(thread)
                    thread.start()
                    time.sleep(random.randint(3, 10))

        for thread in threads:
            thread.join()

        print(f"--- [{sheet}] Complete. ---\nSleep 10sec...")
        time.sleep(10)
        threads = list()

