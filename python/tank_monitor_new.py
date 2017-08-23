import tanks
import sys
import time
from multiprocessing import Queue as Q
from multiprocessing import Process as P
import sys
import serial
import creds
import telegram
import sql


s_port = '/dev/LORA'
#initialise global port
port = None

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

########### Alert stuff ########################
bot = telegram.bot
telegram.mess_loop


def sort_data():
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
                    if vol < tank.min_vol:
                        print tank.name +' under thresh'
                        if tank.statusFlag == 'OK':
                            tank.statusFlag = 'bad'
                            plot_tank(tank, '1', 'water', creds.group_ID, 'days')
                            send = bot.sendMessage(creds.group_ID, tank.name +' tank is low', reply_markup=a.format_keys(tank))
                        elif tank.statusFlag == 'bad':
                            print 'ignoring low level'
                        else:
                            print 'status flag error'        
                    else:
                        print 'level fine, doing nothing'
            except:
                vol = None
            try:
                batt = float(batt)
                if batt > 5.5:
                    batt = None
                if batt < 3.2:
                    plot_tank(tank, '1', 'batt',creds.group_ID, 'days')
            except:
                batt = None
            #add to db
            sql.add_measurement(in_node,vol,batt)

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
sql.setup_db()

fetch_process = P(target=readlineCR, args=(port,))
broadcast_process = P(target=sort_data, args=())

broadcast_process.start()
fetch_process.start()
