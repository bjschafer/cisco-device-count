import sqlite3 as sqlite
from datetime import datetime

class deviceDB(object):
    '''
    Database for keeping track of the unique devices that
    connect to the wireless in one day; done by MAC
    address.
    '''


    def __init__(self, location):
        '''
        Creates the connection to the database and the schema.
        '''
        self.columns = ["mac", "ap", "ssid", "datetime"]
        self.conn = sqlite.connect(location)
        c = self.conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS devices
        (mac TEXT PRIMARY KEY,
        ap TEXT,
        datetime TEXT)''')
        self.conn.commit()
        c.close()
        
    def store(self, device):
        '''
        Stores the device in the database.
        Takes a dictionary as input, with two
        keys: mac and ap.
        
        mac is the mac address formatted as found on the
        wireless controller
        
        ap is the AP name it was connected to, as found on
        the wireless controller
        
        To store in the database it has to be a tuple, so
        t is created as the tuple with the requisite values.
        It also adds to the tuple the current date and time
        for future uses.
        '''
        
        c = self.conn.cursor()
        t = (device["mac"], device["ap"], datetime.now())
        
        c.execute('''INSERT OR REPLACE INTO devices VALUES
        (?, ?, ?)''',t)
        self.conn.commit()
        c.close()
        
    def getCount(self):
        '''
        Returns a count of devices currently in the database.
        '''
        c = self.conn.cursor()
        c.execute('''SELECT COUNT(*) FROM devices''')
        return c.fetchone()
    
    def present(self, device):
        '''
        Checks to see if the specified device is currently in the
        database.  Returns a boolean.
        '''
        c = self.conn.cursor()
        c.execute('''SELECT COUNT(*) FROM devices WHERE mac=?''',device["mac"])
        devicePresent = c.fetchone()
        if devicePresent == 0:
            return False
        else:
            return True
    def flush(self):
        '''
        Clears the database.
        '''
        c = self.conn.cursor()
        c.execute('''DELETE * FROM devices''')
        self.conn.commit()
        c.close()