from multiprocessing import Queue as Q
from multiprocessing import Process as P
import time
import numpy as np
import paho.mqtt.publish as publish
import serial
import smtplib
import requests

#mqtt
broker = "houseslave" 
auth = {'username':"esp", 'password':"heating"}
#thingspeak
water_APIKey = "" #channel api key
batt_APIKey = ""
thingURL = "https://api.thingspeak.com/update"

def generate_fake_data():
    fake_dist = np.random.randint(0,255)
    fake_voltage = np.random.randint(0,255)
    fake_ID = np.random.randint(N)
    return [fake_ID,fake_dist,fake_voltage]

class Tanks:
    def __init__(self, name, nodeID, diam, max_payload, invalid_min, min_vol):
        self.name = name
        self.nodeID = nodeID
        self.diam = diam          # in cm
        self.max_payload = max_payload  # in cm
        self.invalid_min = invalid_min
        self.min_vol = min_vol 
        self.calced_vol = ((self.diam / 2.) ** 2. * 3.14 * self.max_payload)/1000.
        self.batTop = "tank/battery/" +self.name
        self.waterTop = "tank/water/" +self.name
        
    def volume(self, payload):
        #litres (measurements in cm)
        actual_vol = self.calced_vol - ((self.diam / 2.) ** 2. * 3.14 * payload/1000.) # payload variable set in serial port function
        #uncomment below to start spamming users inbox
        #t = threading.Timer(600.0, sendAlert, [self])
        #if actual_vol < min_vol:
        #    msg = (str(self.name) + ' tank is running low. Current volume is ' +str(self.actual_vol) +'l'))
        #    t.start() #don't send too many emails! consider making sure it only gets done once somehow?
        #else:
        #    t.cancel()
        return actual_vol
    
t = Tanks("top",   "1", 250, 214, 40, 200)
n = Tanks("noels", "2", 200, 100, 30, 150)
s = Tanks("sals",  "3", 170,  73, 30, 150)
x = Tanks("test",  "4", 170,  73, 30, 150)

tank_dict = {}
for tank in [t,n,s,x]:
    tank_dict[tank.nodeID] = tank


def readlineCR(port):
    rv = ''
    while True:
        ch = port.read()
        rv += ch
        if ch=='\n':# or ch=='':
            if 'PY' in rv:              #arduino formats message as PYTHON;<nodeID>;<payloadance>\r\n
                print rv
                rec_split = rv.split(';')   #make array like [PYTHON, nodeID, payloadance]
                print rec_split
                q.put(rec_split[1:4])           #put data in queue for processing at rate limited to every 15s er thingspeak api rules
                #in_node = rec_split[1]     #second last member of array
                #print in_node
                #payload = int(rec_split[2])        #last member of array
                #print payload
                #pub_msg(tank_dict[in_node],payload)
                rv = ''

#format mqtt message
def pub_msg():
    while True:
        while (q.empty() == False):
            data = q.get()
            in_node = data[0]
            if tank_dict.has_key(in_node):
                tank = tank_dict[in_node]
            else:
                break
            print data
            water = int(data[1])
            batt = data[2]
            vol = tank.volume(water)
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

port = serial.Serial("/dev/ttyACM0", baudrate=9600, timeout=3.0)

fetch_process = P(target=readlineCR, args=(port,))
broadcast_process = P(target=pub_msg, args=())

broadcast_process.start()
fetch_process.start()
