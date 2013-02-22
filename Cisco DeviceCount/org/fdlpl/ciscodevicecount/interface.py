import socket
import libssh2
import configparser
from os.path import isfile
from org.fdlpl.ciscodevicecount.deviceDB import deviceDB

def createConfig():
    config = configparser.ConfigParser()
    config['DEFAULT'] = {'ControllerAddress': 'xxx.xxx.xxx.xxx',
                         'Username': 'user',
                         'Password': 'password',
                         'DBLocation': 'countDB'}
    with open(".cdcconfig", 'w') as configfile:
        config.write(configfile)

if __name__ == '__main__':
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
    ssids = []
        
    for line in stdout:
        try:
            int(line[0])
            devices.append(line[0:16])
            aps.append(line[18:29])
#            ssids.append(line[])
        except:
            pass
    