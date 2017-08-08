import numpy as np
import matplotlib.pyplot as plt
import datetime
import sqlite3
import time

def get_db():
    conn = sqlite3.connect('tank_database.db')
    c = conn.cursor()
    return conn, c

def query_via_tankid(tank_id, days):
    conn, c = get_db()
    #if days is not None:
    c.execute("SELECT * FROM measurements WHERE tank_id=? AND timestamp BETWEEN datetime('now', '-%i days') AND datetime('now','localtime')" % (days), (tank_id,))
    #else:
        #c.execute("SELECT * FROM measurements WHERE tank_id=? AND timestamp BETWEEN datetime('now', '-1 days') AND datetime('now','localtime')", (tank_id,))
    ret = c.fetchall()
    timestamp = [datetime.datetime.strptime(i[0], "%Y-%m-%d %H:%M:%S.%f") for i in ret]
    volume = [i[2] for i in ret]
    voltage = [i[3] for i in ret]
    ret_dict = {'timestamp':timestamp, 'tank_id':tank_id, 'water_volume':volume, 'voltage':voltage }
    print ret_dict 
    return ret_dict

def plot_tank(tank_id, period):
    d = query_via_tankid(tank_id, period)
    #plt.figure()
    #plt.plot_date(d['timestamp'],d['water_volume'])
    #plt.savefig('tank_%i_volume.png' % (d['tank_id']))
    #plt.close()
    #plt.show()
    # Note that using plt.subplots below is equivalent to using
    # fig = plt.figure and then ax = fig.add_subplot(111)
    fig, ax = plt.subplots()
    ax.plot(d['timestamp'],d['water_volume'])

    ax.set(xlabel='time (s)', ylabel='volume(l)',
        title='About as simple as it gets, folks')
    ax.grid()

    fig.savefig('tank_%i_volume.png' % (d['tank_id']))
    plt.close()

if __name__ == '__main__':
    #data_dict = query_via_tankid(1)
    plot_tank(1,1)
    plot_tank(2,2)


