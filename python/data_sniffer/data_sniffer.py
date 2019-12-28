import serial
import csv
from datetime import datetime
import os.path
import json

tanks_dict = {1:'Top', 2:'Noels', 3:'Sals', 4:'Main', 5:'Bay', 6:'Relay'}

def readlineCR(port):
    rv = ""
    while True:
        ch = port.read()
        # print(ch)
#        rv += ch
#       for python3 need to cast to str
        # rv += str(ch, 'UTF-8')
        try:
            s = ch.decode("UTF-8")
            rv += s
            # print(rv)
        except:
            pass
        if ch==b'\r':# or ch=='':
            print(rv)
            if 'PY' in rv:
                try:
                    tank_data = json.loads(rv)
                    # print(tank_data)
                    data = tank_data['value']
                    # print(data)
                    data_split = data.split(';')
                    # print(data_split)
                    tank = tanks_dict[int(data_split[1])]
                    water = data_split[2]
                    batt = data_split[3]
                    # print(tank)
                    # print(water)
                    # print(batt)
                    f_name = 'tanks.csv'
                    now = datetime.now()
                    strtime = now.strftime("%d/%m/%Y: %H:%M:%S")
                    # https://docs.python.org/3/library/csv.html
                    file_exists = os.path.isfile(f_name)
                    if not file_exists:
                        with open(f_name, 'w+', newline='') as csvfile:
                            fieldnames = ['timestamp', 'Tank', 'Water_level', 'Battery_level']
                            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                            writer.writeheader()
                            writer.writerow({'timestamp': strtime, 'Tank': tank, 'Water_level': water, 'Battery_level': batt})
                    else:
                        with open(f_name, 'a', newline='') as csvfile:
                            fieldnames = ['timestamp', 'Tank', 'Water_level', 'Battery_level']
                            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                            writer.writerow({'timestamp': strtime, 'Tank': tank, 'Water_level': water, 'Battery_level': batt})
                except:
                    print('fucked up')
            return rv

port = serial.Serial("/dev/ttyUSB0", baudrate=115200, timeout=3.0)
#port = serial.Serial("/dev/ttyUSB0", baudrate=9600, timeout=3.0)

if __name__ == "__main__":
    while True:
        #for debugging enable printing of serial port data
        rcv = readlineCR(port)
        #print rcv
