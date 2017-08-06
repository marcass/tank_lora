from multiprocessing import Queue as Q
from multiprocessing import Process as P
import time
import numpy as np
import paho.mqtt.publish as publish
import serial
import smtplib
import requests
import creds
import tanks

s_port = '/dev/ttyUSB0'

#mqtt
broker = creds.mosq_auth['broker']
auth = creds.mosq_auth
#thingspeak
water_APIKey = creds.water_APIKey #channel api key
batt_APIKey = creds.batt_APIKey
thingURL = "https://api.thingspeak.com/update"

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
            tanks.add_measurement(in_node,vol,batt)
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
