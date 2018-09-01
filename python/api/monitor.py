# ToDo
# - Separate functions into:
#     - Data management (input and retreival via sql)
#     - Plots
#     - alerts (telegram.py)
#     - web front end
#     - serial listener (seriallistener.py)
# For prduction
#     - enable alerts when below thresh (tank and batt)
#     - configure input form junk to serial

# virtual serial for testing
import os
import pty
from threading import Thread
import random
from time import sleep
import sys
import time
from threading import Timer
import serial
import creds
import sql
import numpy as np
import telegram
import plot
from collections import deque
from numpy import median
import requests
# import tank_views

buffer_by_name_dict = {}
# setup que circular buffer class
class Buffer:
    def __init__(self, name):
        global buffer_by_name_dict
        self.name = name
        self.water_buff = deque([],3)
        self.batt_buff = deque([],3)
        buffer_by_name_dict[self.name] = self
    def filtered_water(self, val):
        print 'before '+str(self.water_buff)
        self.water_buff.append(val)
        print 'after '+str(self.water_buff)
        return int(median(self.water_buff))
    def filtered_batt(self, val):
        self.batt_buff.append(val)
        return int(median(self.batt_buff))

# posting stuff
jwt = ''
jwt_refresh = ''
headers = ''
def getToken():
    global jwt
    global jwt_refresh
    global headers
    r = requests.post(AUTH_URL, json = {'username': creds.user, 'password': creds.password})
    tokens = r.json()
    #print 'token data is: ' +str(tokens)
    try:
        jwt = tokens['access_token']
        jwt_refresh = tokens['refresh_token']
        headers = {"Authorization":"Bearer %s" %jwt}
    except:
        print 'oops, no token for you'

def post_data(data):
    global jwt
    global jwt_refresh
    global headers
    if (jwt == ''):
        print 'Getting token'
        getToken()
    ret = requests.post(DATA_URL, json = data, headers = headers)
    #print 'JWT = '+str(jwt)
    #print 'First response is: ' +str(ret)
    if '200' not in str(ret):
        print 'Oops, not authenticated'
        try:
            getToken()
            requests.post(DATA_URL, json = data, headers = headersi)
            ret = {'Status': 'Error', 'Message': 'Got token'}
            print 'Post NOT 200 response is: ' +str(r)
        except:
            ret =  {'Status': 'Error', 'Message': 'Failed ot get token, so cannot perform request'}

# Testing using junk data-set
tank_fake_id = 1

def junk_timer(seconds):
    sleep(seconds)
    generate_shit()

def generate_shit():
    global tank_fake_id
    # print "id is "+str(tank_fake_id)
    water = random.randint(0,300)
    batt = random.uniform(3.0,5.0)
    # build string
    packet = 'PY;'+str(tank_fake_id)+';'+str(water)+';'+str(batt)+';\r\n'
    # print 'packet is '+packet
    # increment the tank_id
    if (tank_fake_id < 7):
        tank_fake_id += 1
    else:
        tank_fake_id = 1
    #arduino formats message as PY;<nodeID>;<waterlevle;batteryvoltage;>\r\n
    rec_split = packet.split(';')   #make array like [PYTHON, nodeID, payloadance]
    # print rec_split
    sort_data(rec_split[1:4])
    myThread = Thread(target=junk_timer, args=(3,))
    myThread.start()

#global variables
build_list = []
dur = None
sql_span = None
vers = None

#production port (uncomment for production)
s_port = '/dev/LORA'

#initialise global port
port = None

def sort_data_test(data):
    global vers
    in_node = data[0]
    tank_data = sql.get_tank(in_node, 'id')
    # print tank_data
    if len(tank_data)>0:
        in_tank = tank_data['name']
        print 'found tank is '+in_tank
    else:
        print 'tank not found'
        return
    if in_tank not in buffer_by_name_dict:
        obj = in_tank
        obj = Buffer(in_tank)
    buff = buffer_by_name_dict[in_tank]
    dist = int(data[1])
    dist = buff.filtered_water(dist)
    batt = float(data[2])
    batt = buff.filtered_batt(batt)
    if (dist < int(tank_data['min_dist'])) or (dist > int(tank_data['max_dist'])):
        print 'Payload out of range'
        level = None
    else:
        print 'payload in range'
        dist = dist - int(tank_data['min_dist'])
        level = float(tank_data['max_dist'] - dist)/float(tank_data['max_dist']) * 100.0
        if level < tank_data['min_percent']:
            print tank_data['name']+' under thresh'
            if tank_data['level_status'] != 'bad':
                vers = 'water'
                graph = plot.plot_tank_filtered(tank_data['name'], tank_data['id'], tank_data['line_colour'], '1', 'days', 'water')
                # test send
                telegram.send_graph(creds.marcus_ID, graph)
                telegram.bot.sendMessage(creds.marcus_ID, tank_data['name'] +' tank is low', reply_markup=telegram.a.format_keys(tank_data))
                # pruduction send
                # telegram.send_graph(creds.group_ID, graph)
                # telegram.bot.sendMessage(creds.group_ID, tank_data['name'] +' tank is low', reply_markup=a.format_keys(tank_data))
                sql.write_tank_col(tank_data['name'], 'tank_status', 'bad')
            elif tank_data['level_status'] == 'bad':
                print 'ignoring low level as status flag is bad'
            else:
                print 'status flag error'
        else:
            print 'level fine, doing nothing'
    # if (batt == 0) or (batt > 5.0):
    #     batt = None
    if batt < 3.2:
        if tank_data['batt_status'] != 'low':
            # vers = 'batt'
            # plot.plot_tank(rec_tank, '1',creds.marcus_ID, 'days')
            # telegram.send_graph()
            sql.write_tank_col(tank_data['name'], 'batt_status', 'low')
        elif tank_data['batt_status'] == 'low':
            print 'ignoring low battery as status flag is '+tank_data['batt_status']
        else:
            print 'status flag error'
    sql.add_measurement(in_node,level,batt)


def sort_data(data):
    global vers
    # try:
    in_node = data[0]
    tank_data = sql.get_tank(in_node, 'id')
    # print tank_data
    if len(tank_data)>0:
        print 'found tank is '+tank_data['name']
    else:
        print 'tank not found'
        return
    if in_tank not in buffer_by_name_dict:
        obj = in_tank
        obj = Buffer(in_tank)
    buff = buffer_by_name_dict[in_tank]
    dist = int(data[1])
    dist = buff.filtered_water(dist)
    batt = float(data[2])
    batt = buff.filtered_batt(batt)
    try:
        if (dist < int(tank_data['min_dist'])) or (dist > int(tank_data['max_dist'])):
            print 'Payload out of range'
            level = None
        else:
            print 'payload in range'
            dist = dist - int(tank_data['min_dist'])
            level = float(tank_data['max_dist'] - dist)/float(tank_data['max_dist']) * 100.0
            post_data({'tags': {'type':'water_level', 'sensorID':in_tank, 'site': 'rob_tanks'}, 'value': level, 'measurement': 'tanks'})
            if level < tank_data['min_percent']:
                print tank_data['name']+' under thresh'
                if tank_data['level_status'] != 'bad':
                    vers = 'water'
                    graph = plot.plot_tank_filtered(tank_data['name'], tank_data['id'], tank_data['line_colour'], '1', 'days', 'water')
                    # test send_graph
                    # telegram.send_graph(creds.marcus_ID, graph)
                    # telegram.bot.sendMessage(creds.marcus_ID, tank_data['name'] +' tank is low', reply_markup=telegram.a.format_keys(tank_data))
                    # pruduction send
                    telegram.send_graph(creds.group_ID, graph)
                    telegram.bot.sendMessage(creds.group_ID, tank_data['name'] +' tank is low', reply_markup=telegram.a.format_keys(tank_data))
                    sql.write_tank_col(tank_data['name'], 'tank_status', 'bad')
                elif tank_data['level_status'] == 'bad':
                    print 'ignoring low level as status flag is bad'
                else:
                    print 'status flag error'
            else:
                print 'level fine, doing nothing'
    except:
        print 'exception for some reason'
        level = None
    try:
        # if (batt == 0) or (batt > 5.0):
        #     batt = None
        post_data({'tags': {'type':'batt_level', 'sensorID':in_tank, 'site': 'rob_tanks'}, 'value': batt, 'measurement': 'tanks'})
        if batt < 3.2:
            if tank_data['batt_status'] != 'low':
                # vers = 'batt'
                # plot.plot_tank(rec_tank, '1',creds.marcus_ID, 'days')
                # telegram.send_graph()
                sql.write_tank_col(tank_data['name'], 'batt_status', 'low')
            elif tank_data['batt_status'] == 'low':
                print 'ignoring low battery as status flag is '+tank_data['batt_status']
            else:
                print 'status flag error'
    except:
        batt = None
    #add to db
    # print 'writing value voltage ' +str(batt) +' and volume ' +str(level) +' to db for ' +sql.tanks_by_nodeID[in_node].name
    sql.add_measurement(in_node,level,batt)
    # except:
    #     print 'malformed string'

def readlineCR(port):
    try:
        rv = ''
        while True:
            ch = port.read()
            rv += ch
            if ch=='\n':# or ch=='':
                print rv
                if 'PY' in rv:              #arduino formats message as PY;<nodeID>;<waterlevel>;<batteryvoltage>;>\r\n
                    #print 'Printing status flags stuff on receive'
                    #for x in tanks.tank_list:
                        #print x.name +' is ' +x.statusFlag
                    print rv
                    rec_split = rv.split(';')   #make array like [PYTHON, nodeID, payloadance]
                    print rec_split
                    sort_data(rec_split[1:4])
                    #q.put(rec_split[1:4])           #put data in queue for processing at rate
                    rv = ''
    except (KeyboardInterrupt, SystemExit):
        print "Interrupted"
        sys.exit()
    except:
        print 'failed on port read'
        port_start()

def readlineCR_test(port):
    rv = ''
    while True:
        ch = port.read()
        rv += ch
        if ch=='\n':# or ch=='':
            print rv
            if 'PY' in rv:              #arduino formats message as PY;<nodeID>;<waterlevel>;<batteryvoltage>;>\r\n
                #print 'Printing status flags stuff on receive'
                #for x in tanks.tank_list:
                    #print x.name +' is ' +x.statusFlag
                print rv
                rec_split = rv.split(';')   #make array like [PYTHON, nodeID, payloadance]
                print rec_split
                sort_data(rec_split[1:4])
                #q.put(rec_split[1:4])           #put data in queue for processing at rate
                rv = ''


#Serial port function opening fucntion
def port_check(in_port):
    global port
    try:
        port = serial.Serial(in_port, baudrate=9600, timeout=3.0)
        print s_port+' found'
        return port
    except:
        port = None
        return port

def port_start():
    count = 0
    #handle exceptions for absent port (and keep retrying for a while)
    while (port_check(s_port) is None) and (count < 100):
        count = count + 1
        print s_port+' not found '+str(count)+' times'
        time.sleep(10)
        if count == 100:
            print 'Exited because serial port not found'
            sys.exit()
    while True:
        rcv = readlineCR(port)
        # rcv = readlineCR_test(port)

# testing with junk data (comment out prodn)
#arduino formats message as PY;<nodeID>;<waterlevle;batteryvoltage;>\r\n
# myThread = Thread(target=junk_timer, args=(10,))
# myThread.start()

#start the message bot
telegram.MessageLoop(telegram.bot, {'chat': telegram.on_chat_message, 'callback_query': telegram.on_callback_query}).run_as_thread()
print('Listening ...')

#setup port and start loop in production
port_start()
