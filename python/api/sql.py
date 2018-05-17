import tanks
import pytz
import sys
import time
import datetime
import sqlite3
from passlib.hash import pbkdf2_sha256
from datetime import timedelta
from dateutil import parser

#sqlite stuff
tanks_db = '/home/pi/git/tank_lora/python/tank_database.db'
tz = 'Pacific/Auckland'

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

def get_db():
    conn = sqlite3.connect(tanks_db)
    c = conn.cursor()
    return conn, c


def setup_db():
    # Create table
    conn, c = get_db()
        c.execute('''CREATE TABLE IF NOT EXISTS tanks
                    (tank TEXT UNIQUE, id INTEGER UNIQUE, daim INTEGER, max_dist INTEGER, min_dist INTEGER, min_vol INTEGER, min_percent INTEGER, line_colour TEXT, tank_status TEXT, batt_status TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS measurements
                    (timestamp TIMESTAMP, FOREIGN KEY(tank_id) REFERENCES tanks(id), water_volume REAL, voltage REAL)''')
    c.execute('''CREATE TABLE IF NOT EXISTS userAuth
                    (username TEXT UNIQUE, password TEXT, role TEXT)''')
    conn.commit() # Save (commit) the changes

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
    # Insert a row of data
    conn, c = get_db()
    tanks = get_all_tanks()[0]["id"]
    if tank_id not in tanks:
        try:
            # send a message to telegram requesting setup of tank

            # c.execute("INSERT INTO tanks VALUES (?,?)", (tanks.tanks_by_name[tank_id], tank_id))
            # conn.commit
        except:
            print "Cannot add tank"
    c.execute("INSERT INTO measurements VALUES (?,?,?,?)", (datetime.datetime.utcnow(),tank_id,water_volume,voltage) )
    conn.commit() # Save (commit) the changes

def localtime_from_response(resp):
    ts = datetime.datetime.strptime(resp, "%Y-%m-%d %H:%M:%S.%f")
    ts = ts.replace(tzinfo=pytz.UTC)
    return ts.astimezone(pytz.timezone(tanks.tz))

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
def get_all_users():
    conn, c = get_db()
    c.execute("SELECT * FROM userAuth")
    res = c.fetchall()
    users = [i[0] for i in res]
    return [{'users':users}]

def get_user(column):
    conn, c = get_db()
    c.execute("SELECT %s FROM userAuth" %(column))
    ret = [i[0] for i in c.fetchall()]
    return ret

def get_all_tanks():
    conn, c = get_db()
    c.execute("SELECT * FROM tanks ")
    tank_name =  [i[0] for i in c.fetchall()]
    tank_id = [i[1] for i in c.fetchall()]
    tank_diam = [i[2] for i in c.fetchall()]
    tank_max_dist = [i[3] for i in c.fetchall()]
    tank_min_dis = [i[4] for i in c.fetchall()]
    tank_min_vol = [i[5] for i in c.fetchall()]
    tank_min_percent = [i[6] for i in c.fetchall()]
    tank_colour = [i[7] for i in c.fetchall()]
    tank_status = [i[8] for i in c.fetchall()]
    return [{"name":tank_name, "id":tank_id, "diam":tank_diam, "max":tank_max_dist, "min":tank_min_dist, "min_vol":tank_min_vol, "min_percent":tank_min_percent, "line_colour":tank_colour, "status":tank_status }]

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

def setup_tank(name, nodeID, diam, max_payload, invalid_min, min_vol, min_percent, line_colour, tank_status, batt_status):
    conn, c = get_db()
    try:
        c.execute("INSERT INTO tanks VALUES (?,?,?,?,?,?,?,?,?,?)", (name, nodeID, diam, max_payload, invalid_min, min_vol, min_percent, line_colour, tank_status, batt_status))
        conn.commit()
        return True
    except:
        return False

def write_userdata(resp):
    conn, c = get_db()
    users_in = get_users('username')
    if resp['username'] not in users_in:
        try:
            if (setup_user(resp['username'], resp['password'], resp['role'])):
                # c.execute("INSERT INTO userAuth VALUES (?,?,?)",(resp['username'], resp['password'], resp['role']))
                return {'status':'Setup new user'}
                conn.commit()
            else:
                return {'status':'Failed to setup user'}
        except:
            return {'status':'Failed as non-unique new user'}
    else:
        # may want to validate password or setup a system for chaning it?
        c.execute("UPDATE userAuth SET password=?, role=? WHERE user=?", (pbkdf2_sha256.hash(resp['password'], resp['role'], resp['username']))
        conn.commit()
    return {'status':'Success'}

def delete_user(user):
    conn, c = get_db()
    c.execute("DELETE FROM userAuth WHERE username=?", (user,))
    conn.commit()

# def plot_tank(tank, period, vers, target_id, q_range):
#     format_date = md.DateFormatter('%H:%M\n%d-%m')
#     # Note that using plt.subplots below is equivalent to using
#     # fig = plt.figure and then ax = fig.add_subplot(111)
#     fig, ax = plt.subplots()
#     if vers == 'water':
#         data = 'water_volume'
#         label = 'Volume (l)'
#     if vers == 'batt':
#         data = 'voltage'
#         label = 'Battery Voltage'
#     if type(tank) is list:
#         title_name = ''
#         for i in tank:
#             d = query_via_tankid(i.nodeID, period, q_range)
#             ax.plot_date(d['timestamp'],d[data], i.line_colour, label=i.name, marker='o', markersize='5')
#             title_name += ' '+i.name
#             ax.set(xlabel='Datetime', ylabel=label, title='Tanks '+label)
#         title_name += ' plot'
#     else:
#         d = query_via_tankid(tank.nodeID, period, q_range)
#         if vers == 'bi_plot':
#             title_name = 'Water Level and Voltage for '+tank.name+' Tank'
#             ax.plot_date(d['timestamp'],d['water_volume'], 'b', label='Water Volume (l)',  marker='o', markersize='5')
#             ax.set_xlabel('Time')
#             # Make the y-axis label, ticks and tick labels match the line color.
#             ax.set_ylabel('Water Volume', color='b')
#             ax.tick_params('y', colors='b')
#             ax2 = ax.twinx()
#             ax2.plot_date(d['timestamp'],d['voltage'], 'r', label='Voltage (V)', marker='p', markersize='5')
#             ax2.set_ylabel('Voltage', color='r')
#             ax2.tick_params('y', colors='r')
#         else:
#             title_name = tank.name+' plot'
#             ax.plot_date(d['timestamp'],d[data], tank.line_colour, label=tank.name, marker='o', markersize='5')
#             ax.set(xlabel='Datetime', ylabel=label, title=tank.name+' '+label)
#             plt.axhspan(tank.min_vol, tank.calced_vol, facecolor='#2ca02c', alpha=0.3)
#     ax.get_xaxis().set_major_formatter(format_date)
#     #times = ax.get_xticklabels()
#     #plt.setp(times, rotation=30)
#     plt.legend()
#     ax.grid()
#     plt.tight_layout()
#     fig.savefig(tanks.tank_list[0].pngpath+'net.png')
#     plt.close()
#     #send_graph = bot.sendPhoto(target_id, open(tanks.tank_list[0].pngpath +'net.png'), title_name)
#     send_graph = bot.sendPhoto(target_id, open(tanks.tank_list[0].pngpath +'net.png'))

#setup database
sql.setup_db()
