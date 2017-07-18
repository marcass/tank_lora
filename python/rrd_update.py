#!/usr/bin/python
import rrdtool
import os.path
import creds
import paho.mqtt.client as mqtt
import time

class Tanks:
    def __init__(self, name, nodeID):
        self.name = name
        self.nodeID = nodeID
        self.batTop = "tank/battery/" +self.name
        self.waterTop = "tank/water/" +self.name
        self.rrd_file = '/home/pi/git/tank_lora/python/mqtt2rrd/rrd/' +name +'.rrd'

    
t = Tanks("top",   "1")
n = Tanks("noels", "2")
s = Tanks("sals",  "3")
x = Tanks("test",  "4")

tank_dict = {}
for tank in [t,n,s,x]:
    tank_dict[tank.name] = tank
    
def rrd_update(target, data)
    #check to see if database exists
    if not os.path.isfile(target.rrd_file):
        rrdtool.create(
            target.rrd_file,
            "--start", "now",
            "--step", "300",
            "RRA:AVERAGE:0.5:1:1200",
            "DS:temp:GAUGE:600:-273:5000")
    else:
        # feed updates to the database
        print('adding ' +data ' to ' target.rrd_file)
        rrdtool.update(target.rrd_file, 'N:' +data)
    
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe([(t.waterTop, 0), (n.waterTop, 0), (s.waterTop, 0)])
    
# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+' '+float(msg.payload))
    tank = tank_dict[msg.topic]
    rrd = rrd_update(tank, msg.payload)
    
    
#subscribe to broker and test for messages below alert values
client = mqtt.Client()
client.username_pw_set(username=creds.mosq_auth['username'], password=creds.mosq_auth['password'])
#mqtt.userdata_set(username='esp',password='heating')
client.on_connect = on_connect
client.on_message = on_message
client.connect(creds.mosq_auth['broker'], 1883, 60)
client.loop_start()


while 1:
    time.sleep(5)
