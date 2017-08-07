from multiprocessing import Queue as Q
from multiprocessing import Process as P
import time
import numpy as np
import paho.mqtt.publish as publish
import serial
import smtplib
import requests
import matplotlib.pyplot as plt
import datetime
import sqlite3
import creds
import tanks

s_port = '/dev/ttyUSB0'

#thingspeak
water_APIKey = creds.water_APIKey #channel api key
batt_APIKey = creds.batt_APIKey
thingURL = "https://api.thingspeak.com/update"
#mqtt
broker = creds.mosq_auth['broker']
auth = creds.mosq_auth

#db
def get_db():
    conn = sqlite3.connect('tank_database.db')
    c = conn.cursor()
    return conn, c

def setup_db():
    # Create table
    conn, c = get_db()
    c.execute('''CREATE TABLE IF NOT EXISTS measurements
                    (timestamp TIMESTAMP, tank_id INTEGER, water_volume REAL, voltage REAL)''')

def add_measurement(tank_id,water_volume,voltage):
    # Insert a row of data
    conn, c = get_db()
    c.execute("INSERT INTO measurements VALUES (?,?,?,?)", (datetime.datetime.utcnow(),tank_id,water_volume,voltage) )
    conn.commit() # Save (commit) the changes



def readlineCR(port):
    rv = ''
    while True:
        ch = port.read()
        rv += ch
        if ch=='\n':# or ch=='':
            if 'PY' in rv:              #arduino formats message as PY;<nodeID>;<waterlevle;batteryvoltage;>\r\n
                print rv
                rec_split = rv.split(';')   #make array like [PYTHON, nodeID, payloadance]
                print rec_split
                q.put(rec_split[1:4])           #put data in queue for processing at rate 
                rv = ''

#format mqtt message
def pub_msg():
    while True:
        while (q.empty() == False):
            data = q.get()
            in_node = data[0]
            if tanks.tanks_by_nodeID.has_key(in_node):
                tank = tanks.tanks_by_nodeID[in_node]
            else:
                break
            print data
            water = int(data[1])
            batt = data[2]
            vol = tank.volume(water)
            #add to db
            add_measurement(in_node,vol,batt)
            #publish to thingspeak
            r = requests.post(thingURL, data = {'api_key':water_APIKey, 'field' +tank.nodeID: vol})
            publish.single(tank.waterTop, vol , auth=auth, hostname=broker, retain=True)        
            print('Published ' +str(vol) +' for nodeID ' + str(tank.nodeID) + ' to ' +tank.waterTop)
            #publish to thingspeak
            time.sleep(15)
            r = requests.post(thingURL, data = {'api_key':batt_APIKey, 'field' +tank.nodeID: batt})
            publish.single(tank.batTop, batt , auth=auth, hostname=broker, retain=True)        
            print('Published ' +str(batt) +' for nodeID ' + str(tank.nodeID) + ' to ' +tank.batTop)
            time.sleep(15)

#instatiate queue
q = Q()

port = serial.Serial(s_port, baudrate=9600, timeout=3.0)

fetch_process = P(target=readlineCR, args=(port,))
broadcast_process = P(target=pub_msg, args=())

broadcast_process.start()
fetch_process.start()
