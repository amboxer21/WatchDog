#!/usr/bin/env python

import os
import re
import time
import threading
import subprocess

class WatchDog(object):
    def __init__(self, divisor=4):
        self.divisor = divisor

    def reboot(self):
        os.popen("/sbin/shutdown -r now")

    def monitor(self,trigger='mem'):
        item_dict = {}
        free_m = subprocess.Popen(['/usr/bin/free -m'], 
            shell=True, stdout=subprocess.PIPE).stdout.read()
        for item in ('mem', 'swap'):
            line = re.search('^(' + str(item) + ':)(\s+)(\d+)(\s+)(\d+)(\s+)(\d+)',
                str(free_m), re.I | re.M)
            item_dict[item] = {'total': line.group(3), 'free': line.group(7)}
            threshold = int(item_dict[item]['total']) / int(self.divisor)
            if (int(item_dict[item]['free']) < int(threshold) and
                list(item_dict.keys())[0] == trigger):
                    print("Restarting now!")
                    self.reboot()

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
