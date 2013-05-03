from __future__ import with_statement
import subprocess
from datetime import datetime
import time
from deviceDB import deviceDB

database = deviceDB("countDB")

def update():
    proc = subprocess.Popen(["wificlients.pl"], stdout=subprocess.PIPE, shell=True)
    (results, err) = proc.communicate()
        
    macs = []
    aps = []
    
    for line in results:
        macs.append(line[0:16])
        aps.append(line[18:29])
        
    devices = []
    for mac, ap in map(None, macs, aps):
        devices.append({"mac": mac, "ap": ap})
        
    for device in devices:
        database.store(device)
        
if __name__ == '__main__':
    while True:
        i = 0
        count = 0
        while i < 49:
            update()
            count += database.lastSeenUpdate()
            time.sleep(300)
            i += 1
        with open('stats.txt', 'a') as f:
            f.write(str(datetime.now()) + ": " + str(database.getCount() + count))
        database.flush()
        count = 0
