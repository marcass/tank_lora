#!/usr/bin/python

import time
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import threading
import serial
import smtplib
import requests
import Queue

#mqtt
broker = "houseslave" 
auth = {'username':"esp", 'password':"heating"}
#thingspeak
water_APIKey = "" #channel api key
batt_APIKey
thingURL = "https://api.thingspeak.com/update"
q = Queue.Queue()

#format mqtt message
def pub_msg(tank,rec_split):
    in_node = rec_split[1]     #second last member of array
    print in_node
    water = rec_split[2]
    payload = int(rec_split[3])        #last member of array
    if water == 1:
        vol = tank.volume(payload)
        publish.single(tank.waterTop, vol , auth=auth, hostname=broker, retain=True)        
        #publish to thingspeak
        r = requests.post(thingURL, data = {'api_key':water_APIKey, 'field' +tank.nodeID: vol})
        print('Published ' +str(vol) +' for nodeID ' + str(tank.nodeID) + ' to ' +waterTop)
        return vol
    if water == 0:
        publish.single(tank.batTop, payload , auth=auth, hostname=broker, retain=True)        
        #publish to thingspeak
        r = requests.post(thingURL, data = {'api_key':batt_APIKey, 'field' +tank.nodeID: payload})
        print('Published ' +str(payload) +' for nodeID ' + str(tank.nodeID) + ' to ' +batTop)
        return batt

#function for reading from serial
# Harvest data from port
def readlineCR(port):
    rv = ''
    while True:
        ch = port.read()
        rv += ch
        if ch=='\n':# or ch=='':
            if 'PYTHON' in rv:              #arduino formats message as PYTHON;<nodeID>;<payloadance>\r\n
                print rv
                rec_split = rv.split(';')   #make array like [PYTHON, nodeID, payloadance]
                print rec_split
                q.put(rec_split)           #put data in queue for processing at rate limited to every 15s er thingspeak api rules
                #in_node = rec_split[1]     #second last member of array
                #print in_node
                #payload = int(rec_split[2])        #last member of array
                #print payload
                #pub_msg(tank_dict[in_node],payload)
                rv = ''
    return rv


#port = serial.Serial("/dev/arduino", baudrate=9600, timeout=3.0)
port = serial.Serial("/dev/ttyUSB0", baudrate=9600, timeout=3.0)


class Tanks:
    def __init__(self, name, nodeID, wtopic, btopic, diam, max_payload, invalid_min, min_vol):
        self.name = name
        self.nodeID = nodeID
        self.wtopic = wtopic
        self.btopic = btopic
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

#################### Email #####################################
# http://stackabuse.com/how-to-send-emails-with-gmail-using-python/

def sendAlert(msg):
    dest = "best.nose@gmail.com"
    gmail.user = "best.nose@gmail.com"
    gmail_pass = "app specific p/w"
    
    sent_from = gmail.user
    to = dest
    subject = "Farm water tank alert"

    try:
        server = smtplib.SMTP_SSL('smtp.gmial.com', 465)
        server.ehlo()
        server.login(gmail.user, gmail_pass)
        server.sendmail(sent_from, to, msg)
        server.close()
        print 'Email sent'
    except:
        print 'Something went wrong'

if __name__ == "__main__":
    #local broker connection
    #client = mqtt.Client()
    #client.username_pw_set(username='esp', password='heating')
    #client.on_connect = on_connect
    #client.on_message = on_message
    #client.connect(broker, 1883, 60)

    # Blocking call that processes network traffic, dispatches callbacks and
    # handles reconnecting.
    # Other loop*() functions are available that give a threaded interface and a
    # manual interface.
    # client.loop_forever()
    #client.loop_start()
    while True:
        rcv = readlineCR(port)
        #print rcv
        while not q.empty() #https://stackoverflow.com/questions/4415672/python-theading-timer-how-to-pass-argument-to-the-callback
            t = Timer(16.0, pub_msg, q.get())  # Timer takes array from queue placed with q.put(rec_split) and is over 15s barrier from thingspeak
            t.start()
    
