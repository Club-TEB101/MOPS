import threading

from MOPS import Constract


class CashFlowThread(threading.Thread):

    def __init__(self):
        super().__init__()
        self.url = Constract.MOPS_URL
        self.header = Constract.HEADERS
        self.payload = Constract.PAYLOAD
        self.sheet = Constract.FINANCIAL_STATMENT["Cash_Flow_Statement"]
        self.sheet = Constract.FILE_PATH
        pass

    def main(self):
        pass

    def start(self):
        pass
