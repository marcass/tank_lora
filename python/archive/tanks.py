import creds
import ast

class Tanks:
    def __init__(self, name, nodeID, diam, max_payload, invalid_min, min_vol, min_percent, line_colour):
        global status_dict_out
        global status_dict_in
        global battstatus_dict_out
        global battstatus_dict_in
        self.name = name
        self.nodeID = nodeID
        self.diam = diam                 #diameter of tank in cm
        self.max_payload = max_payload   #Distatnce from sensor to water outlet in tank in cm
        self.invalid_min = invalid_min   #Distatnce from sensor probe end to water level in full tank
        self.min_vol = min_vol
        self.line_colour = line_colour
        self.calced_vol = ((self.diam / 2.) ** 2. * 3.14 * self.max_payload)/1000.
        try:
            self.statusFlag = status_dict_out[self.name]
        except:
            self.statusFlag = 'OK'
        try:
            self.battstatusFlag = battstatus_dict_out[self.name]
        except:
            self.battstatusFlag = 'OK'
        self.pngpath = '/home/pi/git/tank_lora/python/'
        self.min_percent = min_percent
        self.pot_dist = self.max_payload - self.invalid_min
        # setup cirluclar buffer for values
        self.batt_buff = deque(maxlen=5)
        self.water_buff = deque(maxlen=5)
        #append instance to tank_list
        tank_list.append(self)

    def volume(self, payload):
        #litres (measurements in cm)
        actual_vol = self.calced_vol - ((self.diam / 2.) ** 2. * 3.14 * payload/1000.) # payload variable set in serial port function
        return actual_vol

    def set_status(self, status):
        #need to do a write to external file (eg status.py)
        #f = open('myfile', 'w')
        #f.write('hi there\n')  # python will convert \n to os.linesep
        #f.close()  # you can omit in most cases as the destructor will call it
        if status != self.statusFlag:
            self.statusFlag = status
            status_dict_in = {tank.name : tank.statusFlag for tank in tank_list}
            pers_status_dict = open(status_file, 'w')
            pers_status_dict.write(str(status_dict_in))
            pers_status_dict.close()
            print 'status changed via method'
        else:
            print 'status unchanged via method'

    def get_status(self):
        #on initialisation need to get from external file, (eg status.py)
        #if self.statusFlag == 'bad':
            #print 'it should be bad'
        #elif self.statusFlag == 'OK':
            #print 'it should be OK'
        return self.statusFlag

    def set_batt_status(self, status):
        #need to do a write to external file (eg status.py)
        #f = open('myfile', 'w')
        #f.write('hi there\n')  # python will convert \n to os.linesep
        #f.close()  # you can omit in most cases as the destructor will call it
        if status != self.battstatusFlag:
            self.battstatusFlag = status
            battstatus_dict_in = {tank.name : tank.battstatusFlag for tank in tank_list}
            pers_battstatus_dict = open(battstatus_file, 'w')
            pers_battstatus_dict.write(str(battstatus_dict_in))
            pers_battstatus_dict.close()
            print 'status changed via method'
        else:
            print 'status unchanged via method'

    def get_batt_status(self):
        #on initialisation need to get from external file, (eg status.py)
        #if self.battstatusFlag == 'bad':
            #print 'it should be bad'
        #elif self.battstatusFlag == 'OK':
            #print 'it should be OK'
        return self.battstatusFlag

def ret_status():
    global status_dict_out
    try:
        pers_status_dict = open(status_file, 'r')
        status_dict_out = ast.literal_eval(pers_status_dict.read())
        pers_status_dict.close()
        return status_dict_out
    except:
        print 'No status file exception'
        status_dict_out = -1
        return status_dict_out

def ret_battstatus():
    global battstatus_dict_out
    try:
        battstatus_dict = open(battstatus_file, 'r')
        battstatus_dict_out = ast.literal_eval(battstatus_dict.read())
        battstatus_dict.close()
        return battstatus_dict_out
    except:
        print 'No battstatus file exception'
        battstatus_dict_out = -1
        return battstatus_dict_out

#intitiate tank list so it can be accessed when instances are set up
tank_list = []
status_file = '/home/pi/git/tank_lora/python/status.txt'
battstatus_file = '/home/pi/git/tank_lora/python/battstatus.txt'
tz = 'Pacific/Auckland'

ret_status()
ret_battstatus()

t = Tanks('top',   '1', 370, 300, 45, 12000, 20.0, 'b')
n = Tanks('noels', '2', 200, 100, 20, 4000,  10.0, 'g')
s = Tanks('sals',  '3', 140, 110, 27, 400,   10.0, 'r')
m = Tanks('main',  '4', 370, 300, 45, 12000, 50.0, 'm')
b = Tanks('bay',   '5', 370, 270, 45, 12000, 10.0, 'k')
r = Tanks('relay', '6', 370, 270, 45, 12000, 10.0, 'c')

#dict creation (key is term gleaned from incoming data, value is Tank instatnce
tanks_by_name = {tank.name : tank for tank in tank_list}
tanks_by_nodeID = {tank.nodeID : tank for tank in tank_list}

#write statusFlag file:
battstatus_dict_in = {tank.name : tank.battstatusFlag for tank in tank_list}
status_dict_in = {tank.name : tank.statusFlag for tank in tank_list}
print status_dict_in
print battstatus_dict_in
print 'writing status dict'
pers_status_dict = open(status_file, 'w')
pers_status_dict.write(str(status_dict_in))
pers_status_dict.close()

pers_battstatus_dict = open(battstatus_file, 'w')
pers_battstatus_dict.write(str(battstatus_dict_in))
pers_battstatus_dict.close()
