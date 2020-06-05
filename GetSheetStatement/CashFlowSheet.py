import threading
from MOPS.stock_codes.codes import codes
from MOPS.GetSheetStatement import Constract


class CashFlowThread(threading.Thread):

    def __init__(self, sheet: str, year: int, month: int):
        super().__init__()
        self.url = Constract.MOPS_URL
        self.header = Constract.HEADERS
        self.payload = Constract.PAYLOAD
        self.sheet = Constract.FINANCIAL_STATMENT["Cash_Flow_Statement"]
        self.sheet = Constract.FILE_PATH
        pass

    def run(self):
        pass

