import threading
import time

class C(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.isrun = True

    def run(self):
        cnt = 0
        while self.isrun:
            print cnt
            time.sleep(1)
            cnt += 1

def main():
    t = C()
    t.start()
    time.sleep(5)
    t.isrun = False


main()
