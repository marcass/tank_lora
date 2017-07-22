#!/usr/bin/python
import rrdtool
import os.path
import creds
import paho.mqtt.client as mqtt
import time
import tanks

step = 27 * 60 #27min - set to frequency of update of values, should equal interval in seconds which sensor sends tata (eg 30*60
#heartbeat is the time rrdtool will wait for new data point before placing a UNKNOWN value in the datastore

top = tanks.tanks_by_topic
t_name = tanks.tanks_by_name
    
def rrd_update(target, data, vers):
    #check to see if database exists
    stepStr = str(step)
    hb = '600' #5min to wait for value if late
    
    if not os.path.isfile(target.rrdpath+vers+target.name+'.rrd'):
        #DS:level:GAUGE:600:0:20000 = <datastore>:<DSname>:<DStype>:<heatbeat in s>:<low val>:<top val>
        # a step value of 30min with 1 value forming average and 1200 rows archived is 4 years of data (roughly)
        print(target.rrdpath+vers+target.name+'.rrd',
            "--step", stepStr,
            "DS:"+vers+":GAUGE:"+hb+":0:U",
            "RRA:AVERAGE:0.5:1:1200",
            "RRA:MAX:0.5:1:1200")
        rrdtool.create(target.rrdpath+vers+target.name+'.rrd',
            "--step", stepStr,
            "DS:"+vers+":GAUGE:"+hb+":0:U",
            "RRA:AVERAGE:0.5:1:1200",
            "RRA:MAX:0.5:1:1200")
        print 'data store created'
    else:
        print 'updating database this time'
        # feed updates to the database
        print('adding ' +data +' to ' +target.rrd_file)
        rrdtool.update(target.rrdpath+vers+target.name+'.rrd', 'N:' +data)
    
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    sub_list = []
    for inst in tanks.tank_list:
        sub_list.append((inst.waterTop, 0))
        sub_list.append((inst.batTop, 0))
    print sub_list
    client.subscribe(sub_list)
    #client.subscribe([(tanks.t.waterTop, 0), (tanks.n.waterTop, 0), (tanks.s.waterTop, 0)])
    
# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print msg.topic+' '+msg.payload
    tank = top[msg.topic]
    if 'water' in msg.topic:
        rrd = rrd_update(tank, msg.payload,'water')
    elif 'battery' in msg.topic:
        rrd = rrd_update(tank, msg.payload,'batt')
    
    
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
