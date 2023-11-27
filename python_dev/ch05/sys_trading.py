import threading

class SysTrading(threading.Thread):
    def __init__(self, corp_nm, close, vol):
        threading.Thread.__init__(self)
        self.corp_nm = corp_nm
        self.close = close
        self.vol = vol
        self.result = None
    
    def run(self):
        self.result = self.close * self.vol
    
    def getResult(self):
        return self.corp_nm + str(self.result)

sam = SysTrading('삼성전자', 71400, 100)
lg = SysTrading('LG전자', 104000, 100)

sam.start()
lg.start()

print(sam.getResult())
print(lg.getResult())
    
    
    