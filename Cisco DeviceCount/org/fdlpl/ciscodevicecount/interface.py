from __future__ import with_statement
from subprocess import call
from datetime import datetime
import time
from org.fdlpl.ciscodevicecount.deviceDB import deviceDB

database = deviceDB("countDB")

def update():
    results = call(["wificlients.pl"])
    
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
        while i < 49:
            update()
            with open('stats.txt', 'a') as f:
                f.write(datetime.now() + ": " + database.getCount())
            time.sleep(300)
            i += 1
        database.flush()