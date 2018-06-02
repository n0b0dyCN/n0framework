from submitter import Flag, Submitter
import random
import signal

def testFlagSubmitter():
    signal.signal(signal.SIGINT, quit)
    signal.signal(signal.SIGTERM, quit)

    flag_submitter = Submitter()
    flag_submitter.setDaemon(True)
    flag_submitter.start()

    while True:
        flag = raw_input("> ")
        ip = "192.168.2." + str(random.randint(0, 100))
        port = 2333
        payload = "test"
        f = Flag(flag, ip, port, payload)
        flag_submitter.add(f)
        
    flag_submitter.join()
