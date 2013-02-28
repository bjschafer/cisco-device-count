from __future__ import with_statement
import time
from Exscript.util.start import start
from Exscript import Account,Host
import ConfigParser
from os.path import isfile
from org.fdlpl.ciscodevicecount.deviceDB import deviceDB
from io import open

database = None

def createConfig():
    if not isfile(".cdcconfig"):
        config = ConfigParser.ConfigParser()
        config['DEFAULT'] = {'ControllerAddress': 'xxx.xxx.xxx.xxx',
                             'Password': 'password',
                             'DBLocation': 'countDB'}
        with open(".cdcconfig", 'w') as configfile:
            config.write(configfile)
            
def process(info):
    devices = []
    aps = []
    
    for line in info:
        try:
            int(line[0])# tests to see if the line is a mac address
                        # and therefore a valid line by trying to
                        # convert the first character to an int.
                        # if it fails it will just pass the line.
            devices.append(line[0:16])
            aps.append(line[18:29])
        except:
            pass
        
    dbAdd = []
    i = 0
    while i < len(devices):
        dbAdd.append({devices[i]: aps[i]})
        i += 1
        
    for device in dbAdd:
        database.store(device)
            
def getInfo(job, host, conn):
    conn.execute('terminal length 0')           
    
    conn.execute('show client summary')
    
    temp = conn.response()
    
    while True:
        if "More" in temp:
            conn.send(" ")
            temp.append(conn.response())
        else:
            break
        
    conn.send("exit\r")
    conn.close()
    
        
def getCount():
    return database.getCount()

def flush():
    database.flush()
    

if __name__ == '__main__':
    # load configuration file
    createConfig()
    config = ConfigParser.ConfigParser()
    config.read(".cdcconfig")
    dbLocation = config['DEFAULT']['DBLocation']
    controllerAddress = config['DEFAULT']['ControllerAddress']
    user = config['DEFAULT']['Username']
    pword = config['DEFAULT']['Password']
    
    # load database
    database = deviceDB(dbLocation)
    
    # connect with SSH
    account = [Account(user,pword)]
    host = [Host('ssh://' + controllerAddress)]
    
    while True:
        i = 0
        while i < 48:
            getInfo()
            print "Going strong."
            i += 1
            time.sleep(300)
        print getCount()
        flush()
    start(account,host,getInfo)
    

#if __name__ == '__main__':
#    createConfig()
#    while True:
#        i = 0
#        while i < 48:
#            getDevices()
#            print "Going strong."
#            i += 1
#            time.sleep(300) # waits 5 minutes
#        print getCount
#        flush()
#        