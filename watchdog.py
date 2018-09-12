#!/usr/bin/env python

import os
import re
import time
import threading
import subprocess

class WatchDog(object):
    def __init__(self):
        pass

    @staticmethod
    def reboot():
        os.popen("/sbin/shutdown -r now")

    def monitor(self):
        free_m = subprocess.Popen(['/usr/bin/free -m'], 
            shell=True, stdout=subprocess.PIPE).stdout.read()
        for item in ('mem', 'swap'):
            line = re.search('^(' + str(item) + ':)(\s+)(\d+)(\s+)(\d+)(\s+)(\d+)',
                str(free_m), re.I | re.M)
            total = line.group(3)
            free  = line.group(7)
            threshold = int(total) / 4
        if int(free) < int(threshold):
            print("restarting now")
            reboot()

class WatchDogThread(WatchDog):
    def __init__(self, seconds=1):
        super(WatchDogThread, self).__init__()
        thread = threading.Thread(target=self.run, args=(seconds,))
        thread.deamon = True
        thread.start()

    def run(self,seconds):
        while True:
            self.monitor()
            time.sleep(seconds)

if __name__ == '__main__':
    WatchDogThread()
