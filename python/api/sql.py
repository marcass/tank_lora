import pytz
import sys
import time
import datetime
import sqlite3
from passlib.hash import pbkdf2_sha256
from datetime import timedelta
from dateutil import parser
import creds
import ast

# defs for funcitons in Tank class
def get_db():
    conn = sqlite3.connect(tanks_db)
    c = conn.cursor()
    return conn, c


def setup_db():
    # Create table
    conn, c = get_db()
    c.execute('''CREATE TABLE IF NOT EXISTS tanks
                    (tank TEXT UNIQUE, id TEXT UNIQUE, daim INTEGER, max_dist INTEGER, min_dist INTEGER, min_vol INTEGER, min_percent REAL, line_colour TEXT, tank_status TEXT, batt_status TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS measurements
                    (timestamp TIMESTAMP, tank_id TEXT, water_volume REAL, voltage REAL, FOREIGN KEY(tank_id) REFERENCES tanks(id))''')
    c.execute('''CREATE TABLE IF NOT EXISTS userAuth
                    (username TEXT UNIQUE, password TEXT, role TEXT)''')
    conn.commit() # Save (commit) the changes

class Tanks:
    def __init__(self, name, nodeID, diam, max_payload, invalid_min, min_vol, min_percent, line_colour):
        self.name = name
        self.nodeID = nodeID
        self.diam = diam                 #diameter of tank in cm
        self.max_payload = max_payload   #Distatnce from sensor to water outlet in tank in cm
        self.invalid_min = invalid_min   #Distatnce from sensor probe end to water level in full tank
        self.min_vol = min_vol
        self.line_colour = line_colour
        self.calced_vol = ((self.diam / 2.) ** 2. * 3.14 * self.max_payload)/1000.
        self.statusFlag = 'OK'
        self.battstatusFlag = 'OK'
        self.pngpath = '/home/pi/git/tank_lora/python/'
        self.min_percent = min_percent
        self.pot_dist = self.max_payload - self.invalid_min
        #populate db table if not already populated
        self.setup_tank(self.name, self.nodeID, self.diam, self.max_payload, self.invalid_min, self.min_vol, self.min_percent, self.line_colour, self.statusFlag, self.battstatusFlag)
        #append instance to tank_list
        tank_list.append(self)


    def volume(self, payload):
        #litres (measurements in cm)
        actual_vol = self.calced_vol - ((self.diam / 2.) ** 2. * 3.14 * payload/1000.) # payload variable set in serial port function
        return actual_vol

    def setup_tank(self, name, nodeID, diam, max_payload, invalid_min, min_vol, min_percent, line_colour, statusFlag, battstatusFlag):
        conn, c = get_db()
        try:
            c.execute("INSERT INTO tanks VALUES (?,?,?,?,?,?,?,?,?,?)", (name, nodeID, diam, max_payload, invalid_min, min_vol, min_percent, line_colour, statusFlag, battstatusFlag))
            conn.commit()
            return True
        except:
            return False

#Variable stuff
tanks_db = '/home/mw/git/tank_lora/python/api/tank_database.db'
tz = 'Pacific/Auckland'
#initiate tank list so it can be accessed when instances are set up
tank_list = []

#dict creation (key is term gleaned from incoming data, value is Tank instatnce
tanks_by_name = {tank.name : tank for tank in tank_list}
tanks_by_nodeID = {tank.nodeID : tank for tank in tank_list}

# Sort out time management!
# - check how they are being written into db now
# - make it easy on self...

def localtime_from_response(resp):
    ts = datetime.datetime.strptime(resp, "%Y-%m-%d %H:%M:%S.%f")
    ts = ts.replace(tzinfo=pytz.UTC)
    return ts.astimezone(pytz.timezone(tz))

def utc_from_string(payload):
    local = pytz.timezone(tz)
    try:
        naive = datetime.datetime.strptime(payload, "%Y-%m-%dT%H:%M:%S.%fZ")
    except:
        # print 'not first format'
        pass
        try:
            naive = datetime.datetime.strptime(payload, "%a, %b %d %Y, %H:%M")
            # print 'successful convertion'
        except:
            # print 'problem with time string format'
            pass
            try:
                naive = datetime.datetime.strptime(payload, "%Y-%m-%d %H:%M:%S.%f")
            except:
                return 'failed'
    local_dt = local.localize(naive, is_dst=None)
    utc_dt = local_dt.astimezone(pytz.utc)
    return utc_dt

#setup admin user on first run
def setup_admin_user(user, passw):
    conn, c = get_db()
    c.execute("SELECT * FROM userAuth")
    if len(c.fetchall()) > 0:
        return
    else:
        pw_hash = pbkdf2_sha256.hash(passw)
        c.execute("INSERT INTO userAuth VALUES (?,?,?)", (user, pw_hash, 'admin'))
        conn.commit()

def add_measurement(tank_id,water_volume,voltage):
    conn, c = get_db()
    try:
        c.execute("INSERT INTO measurements VALUES (?,?,?,?)", (datetime.datetime.utcnow(),tank_id,water_volume,voltage) )
        conn.commit() # Save (commit) the changes
    except:
        print 'failed to add to db'

def query_via_tankid(tank_id, days_str, q_range):
    try:
        time_range = int(days_str)
    except:
        time_range = 1
    plot_range = days_str+' '+q_range
    print 'plot range = '+plot_range
    conn, c = get_db()
    #if days is not None:
    #c.execute("SELECT * FROM measurements WHERE tank_id=? AND timestamp BETWEEN datetime('now', '-%i days') AND datetime('now','localtime')" % (days), (tank_id,))
    c.execute("SELECT * FROM measurements WHERE tank_id=? AND timestamp BETWEEN datetime('now', '-%i %s') AND datetime('now','localtime')" % (time_range, q_range), (tank_id,))
    #else:
        #c.execute("SELECT * FROM measurements WHERE tank_id=? AND timestamp BETWEEN datetime('now', '-1 days') AND datetime('now','localtime')", (tank_id,))
    ret = c.fetchall()
    timestamp = [localtime_from_response(i[0]) for i in ret]
    volume = [i[2] for i in ret]
    voltage = [i[3] for i in ret]
    ret_dict = {'timestamp':timestamp, 'tank_id':tank_id, 'water_volume':volume, 'voltage':voltage }
    #print ret_dict
    return ret_dict


###################  GETs  ########################
def auth_user(thisuser, passw):
    conn, c = get_db()
    try:
        c.execute("SELECT * FROM userAuth WHERE username=?", (thisuser,))
        ret = c.fetchall()
        pw_hash = ret[0][1]
        role = ret[0][2]
        if (pbkdf2_sha256.verify(passw, pw_hash)):
            status = 'passed'
        else:
            status = 'failed'
        ret_dict = {'status': status, 'role': role}
    except:
        ret_dict = {'status': 'exception', 'role': 'undefined'}
    return ret_dict

def get_all_users():
    conn, c = get_db()
    c.execute("SELECT * FROM userAuth")
    res = c.fetchall()
    users = [i[0] for i in res]
    role = [i[2] for i in res]
    return {'users':users, 'role':role}

def get_user(column):
    conn, c = get_db()
    c.execute("SELECT %s FROM userAuth" %(column))
    ret = [i[0] for i in c.fetchall()]
    return ret

def fetch_user_data(payload, col):
    try:
        conn, c = get_db()
        c.execute("SELECT * FROM userAuth WEHRE %s=?" %(col),  (user,))
        res = c.fetchall()
        username = [i[0] for i in res]
        role = [i[2] for i in res]
        return {'username':username, 'role':role}
    except:
        return {'status':'Data not found in userdb'}


def get_all_tanks():
    conn, c = get_db()
    c.execute("SELECT * FROM tanks ")
    res = c.fetchall()
    tank_name =  [i[0] for i in res]
    tank_id = [i[1] for i in res]
    tank_diam = [i[2] for i in res]
    tank_max_dist = [i[3] for i in res]
    tank_min_dist = [i[4] for i in res]
    tank_min_vol = [i[5] for i in res]
    tank_min_percent = [i[6] for i in res]
    line_colour = [i[7] for i in res]
    tank_status = [i[8] for i in res]
    batt_status = [i[9] for i in res]
    return {"name":tank_name, "id":tank_id, "diam":tank_diam, "max":tank_max_dist, "min":tank_min_dist, "min_vol":tank_min_vol, "min_percent":tank_min_percent, "line_colour":line_colour, "level_status":tank_status, 'batt_status':batt_status}

def get_tank(payload, col):
    conn, c = get_db()
    c.execute("SELECT * FROM tanks WHERE %s=?" %(col), (payload,))
    ret = c.fetchall()[0]
    # print ret
    res = {'name':ret[0], 'id':ret[1], 'max_dist':ret[2], 'min_dist':ret[4], 'min_percent':ret[6], 'level_status':ret[8], 'batt_status':ret[9], 'line_colour':ret[7]}
    # print res
    return res

############  Write data ########################
# Not sure what the role thing in here is for
def setup_user(user_in, passw, role=0):
    conn, c = get_db()
    try:
        pw_hash = pbkdf2_sha256.hash(passw)
        c.execute("INSERT INTO userAuth VALUES (?,?,?)", (user_in, pw_hash, role))
        conn.commit()
        return True
    except:
        return False

def write_userdata(resp):
    conn, c = get_db()
    users_in = get_all_users()
    if resp['username'] not in users_in['users']:
        try:
            if (setup_user(resp['username'], resp['password'], resp['role'])):
                return {'status':'Success', 'message':'Setup new user'}
            else:
                return {'status':'Error', 'message':'Failed to setup user'}
        except:
            return {'status':'Error', 'message':'Failed as non-unique new user'}
    else:
        # may want to validate password or setup a system for chaning it?
        c.execute("UPDATE userAuth SET password=?, role=? WHERE user=?", (pbkdf2_sha256.hash(resp['password']), resp['role'], resp['username']))
        conn.commit()
        return {'status':'Success','message':'User update success'}

def delete_user(user):
    conn, c = get_db()
    try:
        c.execute("DELETE FROM userAuth WHERE username=?", (user,))
        conn.commit()
        return {'status':'Success. User '+name+' deleted'}
    except:
        return {'status':'Error. User '+name+' not deleted'}


def write_tank_col(name, column, payload):
    conn, c = get_db()
    try:
        c.execute("UPDATE tanks SET %s=? WHERE tank=?" %(column), (payload,name))
        conn.commit()
        return {'status':'Success', 'message': 'Status updated'}
    except:
        return {'status':'Error', 'message':'Status not updated'}



#setup database
setup_db()

t = Tanks('top',   '1', 370, 300, 45, 12000, 20.0, 'b')
n = Tanks('noels', '2', 200, 100, 20, 4000,  10.0, 'g')
s = Tanks('sals',  '3', 140, 110, 27, 400,   10.0, 'r')
m = Tanks('main',  '4', 370, 300, 45, 12000, 50.0, 'm')
b = Tanks('bay',   '5', 370, 270, 45, 12000, 10.0, 'k')
r = Tanks('relay', '6', 370, 270, 45, 12000, 10.0, 'c')
