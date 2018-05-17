# ToDo
# - Separate functions into:
#     - Data management (input and retreival via sql)
#     - Plots
#     - alerts (telegram.py)
#     - web front end
#     - serial listener (seriallistener.py)

import matplotlib
matplotlib.use('Agg')
import pytz
import sys
import time
from threading import Timer
from multiprocessing import Queue as Q
from multiprocessing import Process as P
import time
import sys
import serial
import creds
import sql
import numpy as np
import telegram
import tank_views

#global variables
build_list = []
dur = None
sql_span = None
vers = None
s_port = '/dev/LORA'
#initialise global port
port = None

def sort_data(data):
    global vers
    try:
        in_node = data[0]
        if tanks.tanks_by_nodeID.has_key(in_node):
            rec_tank = tanks.tanks_by_nodeID[in_node]
            print 'found tank is '+rec_tank.name
            #print 'following in the instance statusFlags:'
            #for y in tanks.tank_list:
                #print 'status for ' +y.name+' is '+y.get_status()
        else:
            print 'tank not found'
            return
        print data
        #print 'Status as seen in sort_data'
        #for x in tanks.tank_list:
            #print x.name +' is ' +x.statusFlag
        dist = data[1]
        batt = data[2]
        try:
            dist = int(dist)
            if (dist < rec_tank.invalid_min) or (dist > rec_tank.max_payload):
                print 'Payload out of range'
                level = None
            else:
                print 'payload in range'
                dist = dist - rec_tank.invalid_min
                level = float(rec_tank.pot_dist - dist)/float(rec_tank.pot_dist) * 100.0
                if level < rec_tank.min_percent:
                    #print rec_tank.name +' under thresh'
                    #print rec_tank.name+' status prechange is '+rec_tank.statusFlag
                    if rec_tank.statusFlag != 'bad':
                        #print 'dropping through and changing status'
                        rec_tank.set_status('bad')
                        #print rec_tank
                        #print 'new status is '+rec_tank.statusFlag
                        vers = 'water'
                        plot.plot_tank(rec_tank, '1', creds.group_ID, 'days')
                        telegram.send_graph()
                        #print 'plotted'
                        send = telegram.bot.sendMessage(creds.group_ID, rec_tank.name +' tank is low', reply_markup=a.format_keys(rec_tank))
                        #print 'sent'
                    elif rec_tank.statusFlag == 'bad':
                        print 'ignoring low level as status flag is '+rec_tank.statusFlag
                    else:
                        print 'status flag error'
                else:
                    print 'level fine, doing nothing'
        except:
            print 'exception for some reason'
            level = None
        try:
            batt = float(batt)
            if (batt == 0) or (batt > 5.0):
                batt = None
            elif batt < 3.2:
                if rec_tank.battstatusFlag != 'low':
                    rec_tank.set_battstatus('low')
                    vers = 'batt'
                    plot.plot_tank(rec_tank, '1',creds.marcus_ID, 'days')
                    telegram.send_graph()
                elif rec_tank.battstatusFlag == 'low':
                    print 'ignoring low battery as status flag is '+rec_tank.battstatusFlag
                else:
                    print 'status flag error'

        except:
            batt = None
        #add to db
        print 'writing value voltage ' +str(batt) +' and volume ' +str(level) +' to db for ' +tanks.tanks_by_nodeID[in_node].name
        sql.add_measurement(in_node,level,batt)
    except:
        print 'malformed string'

def readlineCR(port):
    try:
        rv = ''
        while True:
            ch = port.read()
            rv += ch
            if ch=='\n':# or ch=='':
                if 'PY' in rv:              #arduino formats message as PY;<nodeID>;<waterlevle;batteryvoltage;>\r\n
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

#setup port and start loop
port_start()
