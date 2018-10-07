import requests
import threading
import time

class IPChecker(threading.Thread):
    """docstring for IPChecker"""
    def __init__(self, parent = None):
        super(IPChecker, self).__init__()
        self.parent = parent
        self.url = "http://checkip.amazonaws.com"
        self.lastIP = None
        self.count = 0
        self.running = False
        self.stopEvent = threading.Event()
        
    def run(self):
        self.running = True
        while not self.stopEvent.isSet():
            try:
                r = requests.get(self.url, None)
                print(r.text)
                if self.lastIP != r.text:
                    if self.lastIP == None:
                        self.lastIP = r.text
                    else:
                        self.count+=1
                    if self.count >= 5:
                        self.lastIP = r.text
                        self.count = 0
                        if self.parent:
                            self.parent.notifyIpUpdated()
                elif self.count > 0:
                    self.count -= 1
            except Exception:
                print("Connection error.")
            print("count: %d"%self.count)
            time.sleep(10)

    def join(self, timeout=None):
        self.stopEvent.set()
        self.running = False
        threading.Thread.join(self, timeout)

# if __name__ == '__main__':
#     # 
#     t = IPChecker()
#     t.start()
