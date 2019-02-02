import os
import pty
from threading import Thread
import random
from time import sleep
import serial

#create virtaul port for testing (comment following block for production)
master, slave = pty.openpty()
s_name = os.ttyname(slave)
ser = serial.Serial(s_name, baudrate=9600, timeout=3.0)

tank_fake_id = 1

def junk_timer(seconds):
    sleep(seconds)
    generate_shit()

def generate_shit():
    global tank_fake_id
    # print "id is "+str(tank_fake_id)
    water = random.randint(5,300)
    batt = random.uniform(3.0,5.0)
    # build string
    packet = 'PY;'+str(tank_fake_id)+';'+str(water)+';'+str(batt)+';'
    print(packet)
    #write packet to virtual port
    ser.write(packet.encode())
    # increment the tank_id
    if (tank_fake_id < 6):
        tank_fake_id += 1
    else:
        tank_fake_id = 1
    myThread = Thread(target=junk_timer, args=(3,))
    myThread.start()

# start thread for testing
myThread = Thread(target=junk_timer, args=(3,))
myThread.start()
