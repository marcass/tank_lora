import creds
import sqlite3

class Tanks:
    def __init__(self, name, nodeID, diam, max_payload, invalid_min, min_vol, line_colour):
        self.name = name
        self.nodeID = nodeID
        self.diam = diam                 #diameter of tank in cm
        self.max_payload = max_payload   #Distatnce from sensor to water outlet in tank in cm
        self.invalid_min = invalid_min   #Distatnce from sensor probe end to water level in full tank
        self.min_vol = min_vol 
        self.line_colour = line_colour
        self.calced_vol = ((self.diam / 2.) ** 2. * 3.14 * self.max_payload)/1000.
        self.statusFlag = 'OK'
        self.url = 'https://thingspeak.com/channels/300940'
        self.waterTop = 'tank/water/' +name
        self.batTop = "tank/battery/" +name
        self.pngpath = '/home/pi/git/tank_lora/python/'
        
    def volume(self, payload):
        #litres (measurements in cm)
        actual_vol = self.calced_vol - ((self.diam / 2.) ** 2. * 3.14 * payload/1000.) # payload variable set in serial port function
        return actual_vol
    
tz = 'Pacific/Auckland'
    
#t = Tanks("top",   "1", 250, 214, 40, 200, '#EA644A')
#n = Tanks("noels", "2", 200, 100, 30, 150, '#54EC48')
#s = Tanks("sals",  "3", 170,  73, 30, 150, '#7648EC')

#test data
t = Tanks("top",   "1", 370, 270, 45, 12000, 'b')
n = Tanks("noels", "2", 100, 100, 20, 150, 'g')
s = Tanks("sals",  "3", 100, 100, 20, 150, 'r')
m = Tanks("main",  "4",  370, 300, 45, 12000, 'm')
b = Tanks("bay",  "5", 370, 270, 45, 12000, 'k')
f = Tanks("relay", "6", 370, 270, 45, 12000, 'c')

#dict creation (key is term gleaned from incoming data, value is Tank instatnce
tank_list = [t,n,s,m,b,f]
#tank_list = [t,n,s]
tanks_by_wtopic = {tank.waterTop : tank for tank in tank_list}
tanks_by_btopic = {tank.batTop : tank for tank in tank_list}
tanks_by_topic = dict(tanks_by_wtopic.items() + tanks_by_btopic.items())
tanks_by_name = {tank.name : tank for tank in tank_list}
tanks_by_nodeID = {tank.nodeID : tank for tank in tank_list}

