from multiprocessing import Queue as Q
from multiprocessing import Process as P
import time
import sys
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

s_port = '/dev/LORA'
#initialise global port
port = None

#thingspeak
water_APIKey = creds.water_APIKey #channel api key
batt_APIKey = creds.batt_APIKey
thingURL = "https://api.thingspeak.com/update"
#mqtt
broker = creds.mosq_auth['broker']
auth = creds.mosq_auth

#db
def setup_db():
    # Create table
    conn, c = tanks.get_db()
    c.execute('''CREATE TABLE IF NOT EXISTS measurements
                    (timestamp TIMESTAMP, tank_id INTEGER, water_volume REAL, voltage REAL)''')
    conn.commit() # Save (commit) the changes

    

def add_measurement(tank_id,water_volume,voltage):
    # Insert a row of data
    conn, c = tanks.get_db()
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
            #check to see if it's a relay (and insert null water value if it is)
            dist = data[1]
            batt = data[2]
            try:
                dist = int(dist)
                #check to see if in acceptable value range
                if (dist < tank.invalid_min) or (dist > tank.max_payload):
                    vol = None
                else:
                    vol = tank.volume(dist)
            except:
                vol = None
            try:
                batt = float(batt)
                if batt > 5.5:
                    batt = None
            except:
                batt = None
            #add to db
            add_measurement(in_node,vol,batt)
            #publish to thingspeak
            #r = requests.post(thingURL, data = {'api_key':water_APIKey, 'field' +tank.nodeID: vol})
            publish.single(tank.waterTop, vol , auth=auth, hostname=broker, retain=True)        
            print('Published ' +str(vol) +' for nodeID ' + str(tank.nodeID) + ' to ' +tank.waterTop)
            #publish to thingspeak
            #time.sleep(15)
            #r = requests.post(thingURL, data = {'api_key':batt_APIKey, 'field' +tank.nodeID: batt})
            publish.single(tank.batTop, batt , auth=auth, hostname=broker, retain=True)        
            print('Published ' +str(batt) +' for nodeID ' + str(tank.nodeID) + ' to ' +tank.batTop)
            #time.sleep(15)

#Serial port function opening fucntion
count = 0
def port_check(in_port):
    global port
    try:
        port = serial.Serial(in_port, baudrate=9600, timeout=3.0)
        print s_port+' found'
        count = 0
        return port
    except:
        port = None
        return port


#handle exceptions for absent port (and keep retrying for a while)
while (port_check(s_port) is None) and (count < 100):
    count = count + 1
    print s_port+' not found '+str(count)+' times'
    time.sleep(10)
    
if count == 100:
    print 'Exited because serial port not found'
    sys.exit()
    
#instatiate queue
q = Q()
#setup database
setup_db()

fetch_process = P(target=readlineCR, args=(port,))
broadcast_process = P(target=pub_msg, args=())

broadcast_process.start()
fetch_process.start()
