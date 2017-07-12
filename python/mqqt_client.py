#!/usr/bin/python

import time
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import threading
import serial
import smtplib
import requests

#mqtt
broker = "localhost" 
auth = {'username':"tank", 'password':"level"}
#thingspeak
channelID = ""
APIKey = "" #channel api key
thingURL = "https://api.thingspeak.com/update"


#format mqtt message
def pub_msg():
    pub_thing()
    if in_node == t.nodeID:
        publish.single(t.topic, t.volume(), auth=auth, hostname=broker, retain=True)        
    if in_node == n.nodeID:
        publish.single(n.topic, n.volume(), auth=auth, hostname=broker, retain=True)       
    if in_node == s.nodeID:
        publish.single(s.topic, s.volume(), auth=auth, hostname=broker, retain=True)
    if in_node == x.nodeID:
        publish.single(x.topic, dist, auth=auth, hostname=broker, retain=True)
    #publish to thingspeak
    r = requests.post(thingURL, data = {'api_key':APIKey, 'field' +in_node:in_sens}
    print('Published' +in_sens +' for nodeID ' +in_node)

#function for reading from serial
# Harvest data from port
def readlineCR(port):
        rv = ""
        while True:
            ch = port.read()
            rv += ch
            if ch=='\r':# or ch=='':
                if 'PYTHON' in rv:              #arduino formats message as PYTHON;<nodeID>;<distance>\r\n
                    print rv
                    rec_split = rv.split(';')   #make array like [PYTHON, nodeID, distance]
                    in_node = rec_split[-2]     #second last member of array
                    dist = rec_split[-1]        #last member of array
                    pub_msg()
            return rv


port = serial.Serial("/dev/arduino", baudrate=9600, timeout=3.0)
#port = serial.Serial("/dev/ttyUSB0", baudrate=9600, timeout=3.0)


class tanks:
    def __init__(self, name, nodeID, topic, diam, max_dist, invalid_min, min_vol, field):
        self.name = name
        self.nodeID = nodeID
        self.topic = topic
        self.diam = diam
        self.max_dist = max_dist
        self.invalid_min = invalid_min
        self.max_dist = max_dist
        self.min_vol = min_vol
        self.field = field
    def volume(self):
        #litres (measurements in cm)
        vol_calc = (self.diam / 2) ** 2 * 3.14 * self.max_dist/1000
        actual_vol = (vol_calc - ((self.diam / 2) ** 2 * 3.14 * dist/1000)) # dist variable set in serial port function
        #uncomment below to start spamming users inbox
        #t = threading.Timer(600.0, sendAlert, [self])
        #if actual_vol < min_vol:
        #    msg = (str(self.name) + ' tank is running low. Current volume is ' +str(self.actual_vol) +'l'))
        #    t.start() #don't send too many emails! consider making sure it only gets done once somehow?
        #else:
        #    t.cancel()
        return actual_vol
    
n = tanks("noels", "2", "tank/noels", 200, 100, 30, 150, "field2")
t = tanks("top", "1", "tank/top", 250, 214, 40, 200, "field1")
s = tanks("sals", "3", "tank/sals", 170, 73, 30, 150, "field3")
x = tanks("test", "4", "tank/test", 170, 73, 30, 150, "fiel4")


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
        server = smtplib.SMTP_SSL)'smtp.gmial.com', 465)
        server.ehlo()
        server.login(gmail.user, gmail_pass)
        server.sendmail(sent_from, to, msg)
        server.close()
        print 'Email sent'
    except:
        print 'Something went wrong'

if __name__ == "__main__":
    #local broker connection
    client = mqtt.Client()
    client.username_pw_set(username=loc.password, password=loc.password))
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(loc.url, loc.port, 60)

    # Blocking call that processes network traffic, dispatches callbacks and
    # handles reconnecting.
    # Other loop*() functions are available that give a threaded interface and a
    # manual interface.
    # client.loop_forever()
    client.loop_start()
    while True:
        rcv = readlineCR(port)
        #print rcv
