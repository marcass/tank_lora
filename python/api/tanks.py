import creds
import ast
import sql

class Tanks:
    def __init__(self, name, nodeID, diam, max_payload, invalid_min, min_vol, min_percent, line_colour):
        self.name = name
        self.nodeID = nodeID
        self.diam = diam                 #diameter of tank in cm
        self.max_payload = max_payload   #Distatnce from sensor to water outlet in tank in cm
        self.invalid_min = invalid_min   #Distatnce from sensor probe end to water level in full tank
        self.min_vol = min_vol
        self.line_colour = line_colour
        self.calced_vol = ((self.diam / 2.) ** 2. * 3.14 * self.max_payload)/1000.
        self.statusFlag = 'OK'
        self.battstatusFlag = 'OK'
        self.pngpath = '/home/pi/git/tank_lora/python/'
        self.min_percent = min_percent
        self.pot_dist = self.max_payload - self.invalid_min
        #append instance to tank_list
        tank_list.append(self)

    def volume(self, payload):
        #litres (measurements in cm)
        actual_vol = self.calced_vol - ((self.diam / 2.) ** 2. * 3.14 * payload/1000.) # payload variable set in serial port function
        return actual_vol

    #populate db table if not already populated
    sql.setup_tank(self.name, self.nodeID, self.diam, self.max_payload, self.invalid_min, self.min_vol, self.min_percent, self.line_colour, self.statusFlag, self.battstatusFlag)

#intitiate tank list so it can be accessed when instances are set up
tank_list = []
tz = 'Pacific/Auckland'

t = Tanks('top',   '1', 370, 300, 45, 12000, 20.0, 'b')
n = Tanks('noels', '2', 200, 100, 20, 4000,  10.0, 'g')
s = Tanks('sals',  '3', 140, 110, 27, 400,   10.0, 'r')
m = Tanks('main',  '4', 370, 300, 45, 12000, 50.0, 'm')
b = Tanks('bay',   '5', 370, 270, 45, 12000, 10.0, 'k')
r = Tanks('relay', '6', 370, 270, 45, 12000, 10.0, 'c')

#dict creation (key is term gleaned from incoming data, value is Tank instatnce
tanks_by_name = {tank.name : tank for tank in tank_list}
tanks_by_nodeID = {tank.nodeID : tank for tank in tank_list}
