#!/usr/bin/python

import time
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import threading


class tanks:
    def __init__(self, name, topic, diam, max_dist, invalid_min, min_vol, field):
        self.name = name
        self.topic = topic
        self.diam = diam
        self.max_dist = max_dist
        self.invalid_min = invalid.min
        self.max_dist = max_dist
        #invalid_max = (max_dist + 20)
        self.min_vol = min_vol
        self.field = field
    def volume():
        #litres (measurements in cm)
        vol_calc = (diam / 2 * 3.14 * max_dist)/1000
        actual_vol = (vol_calc - (diam / 2 * 3.14 * dist/1000))
        #uncomment below to start spamming users inbox
        #t = threading.Timer(600.0, sendAlert, [self])
        #if actual_vol < min_vol:
        #    msg = (str(self.name) + ' tank is running low. Current volume is ' +str(self.actual_vol) +'l'))
        #    t.start() #don't send too many emails! consider making sure it only gets done once somehow?
        #else:
        #    t.cancel()
        return actual_vol
    
n = tanks("noels", "tank/noels", "200", "100", "30", "150"), "field2")
t = tanks("top", "tank/top", "250", "214", "40", "200", "field1")
s = tanks("sals", "tank/sals", "170", "73", "30", "150", "field3")
x = tanks("test", "tank/test", "170", "73", "30", "150")


class mqtt_broker:
    def __init__(self, url, port, qos, username=0, password=0)
    self.url = url
    self.port = port
    self.qos = qos 
    self.uername = username
    self.passwork = password

ts = mqtt_broker("mqtt.thingspeak.com", "8883", "0")
ts.channelID = "<put channel id in here>"
ts.APIkey = "<put API key in here"
loc = mqtt_broker("localhost", "1883", "0", "esp", "heating")


# The callback for when the client receives a CONNACK response from the server.
# http://www.steves-internet-guide.com/subscribing-topics-mqtt-client/
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe([(n.topic, loc.qos),(s.topic, loc.qos),(t.topic, loc.qos)])

def on_publish(client,userdata,result):             #create function for callback
    print("data published \n")
    pass

def on_disconnect(client, userdata, rc):
   print("client disconnected ok")

# The callback for when a PUBLISH message is received from the local broker.
def on_message(client, userdata, msg):
    ######### Just use fucking JSON string to update via api:
    #https://au.mathworks.com/help/thingspeak/update-channel-feed.html mqtt is too hard (their api is too restrictive)





    #thingspeak network config - connect when mesage incoming on subscribed topics
    tsc = mqtt.Client()
    tsc.connect(ts.url, ts.port, 10)
    tsc.on_connect = ts_on_connect
    tsc.on_message = ts_on_message
    tsc.on_publish = on_publish
    tsc.on_disconnect = on_disconnect
    print(msg.topic+' '+str(msg.payload))
    #filter incoming messages by topic and parse payload accordingly
    if msg.topic == n.topic:
        n.dist = int(msg.payload)
        print('channels/' +str(ts.channelID) +'/publish/fields/' +str(n.field) +'/' +str(ts.APIkey), int(n.volume))
        #syntax is <obj>.publish(topic, data)
        #tipic string syntax stolen from here: https://au.mathworks.com/help/thingspeak/use-arduino-client-to-publish-to-a-channel.html
        pub = tsc.publish('channels/' +str(ts.channelID) +'/publish/fields/' +str(n.field) +'/' +str(ts.APIkey), int(n.volume))
    if msg.topic == s.topic:
        s.dist = int(msg.payload)
        pub = tsc.publish('channels/' +str(ts.channelID) +'/publish/fields/' +str(s.field) +'/' +str(ts.APIkey), int(s.volume))
    if msg.topic == t.topic:
        t.dist = int(msg.payload)
        pub = tsc.publish('channels/' +str(ts.channelID) +'/publish/fields/' +str(t.field) +'/' +str(ts.APIkey), int(t.volume))
    #disconnect to thing speak after sending message (qos is zero according to their terms)
    ts.disconnect()

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
    while True:
      client.loop_start()
