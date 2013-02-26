import socket
import time
import libssh2
import configparser
from os.path import isfile
from org.fdlpl.ciscodevicecount.deviceDB import deviceDB

database = None

def createConfig():
    config = configparser.ConfigParser()
    config['DEFAULT'] = {'ControllerAddress': 'xxx.xxx.xxx.xxx',
                         'Username': 'user',
                         'Password': 'password',
                         'DBLocation': 'countDB'}
    with open(".cdcconfig", 'w') as configfile:
        config.write(configfile)

def getDevices():
    # load configuration file
    if not isfile(".cdcconfig"):
        createConfig()
    config = configparser.ConfigParser()
    config.read(".cdcconfig")
    dbLocation = config['DEFAULT']['DBLocation']
    controllerAddress = config['DEFAULT']['ControllerAddress']
    user = config['DEFAULT']['Username']
    pword = config['DEFAULT']['Password']
    
    # load database
    database = deviceDB(dbLocation)
    
    # connect with SSH
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((controllerAddress, 22))
    session = libssh2.Session()
    session.startup(sock)
    session.userauth_password(user, pword)
    
    channel = session.channel()
    channel.execute('terminal length 0')
    channel.execute('show client summary')
    
    stdout,stderr = []
    while not channel.eof:
        data = channel.read(1024)
        if data:
            stdout.append(data)
            
        data = channel.read(1024, libssh2.STDERR)
        if data:
            stderr.append(data)
            
    while True:
        if "More" in stdout[-1]:
            channel.send(" ")
        else:
            break
        
    devices = []
    aps = []
    
    for line in stdout:
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
        
def getCount():
    return database.getCount()

def flush():
    database.flush()

if __name__ == '__main__':
    createConfig()
    while True:
        i = 0
        while i < 48:
            getDevices()
            i += 1
            time.sleep(300) # waits 5 minutes
        print(getCount)
        flush()
        