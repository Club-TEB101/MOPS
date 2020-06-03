import datetime
import random
import time
from MOPS import BalanceSheet, ProfitLossSheet, Constract


def get_sheetNum(run_sheet):
    sheet = ""
    if run_sheet == "1":
        sheet = "Balance_Sheet"
    elif run_sheet == "2":
        sheet = "Profit_and_Loss_Account"
    elif run_sheet == "3":
        sheet = "Cash_Flow_Statement"
    else:
        run_sheet = input("Input Number to Get Financial Sheet:\n1.Balance_Sheet\n2.Profit&Loss\n3.CashFlow\n:")
        get_sheetNum(run_sheet)
    return sheet


if __name__ == '__main__':
    now = datetime.datetime.now()
    threads = list()

    run_sheet = input("Input Number to Get Financial Sheet:\n1.Balance_Sheet\n2.Profit&Loss\n3.CashFlow\n:")
    sheet = get_sheetNum(run_sheet)

    for year in range(102, (now.year - 1910)):
        for season in range(1, 5):
            if sheet == "Balance_Sheet":
                thread = BalanceSheet.BalanceSheet(sheet, year, season)
            elif sheet == "Profit_and_Loss_Account":
                thread = ProfitLossSheet.ProfitLossSheet(sheet, year, season)
            elif sheet == "Cash_Flow_Statement":
                thread = None
            else:
                break

            if thread is not None:
                threads.append(thread)
                thread.start()
                time.sleep(random.randint(3, 10))

    for thread in threads:
        thread.join()

    print(f"--- [{sheet}] Complete. ---\nSleep 10sec...")
    time.sleep(5)
    threads = list()
