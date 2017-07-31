import creds

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
        self.waterTop = 'tank/water/' +name
        self.batTop = "tank/battery/" +name
        self.statusFlag = 'OK'
        self.rrdpath = '/home/pi/git/tank_lora/python/rrd/'
        self.rrd_file = self.rrdpath +name +'.rrd'
        self.url = 'https://thingspeak.com/channels/300940'
        #rrd stuff
        #DEF
        self.rrd_def = 'DEF:'+self.name+'='+self.rrdpath+vers+self.name+'.rrd'+':'+vers+':AVERAGE:step=3600'
        self.rrd_line = 'LINE'+self.nodeID+':'+self.name+self.line_colour+':'+self.name+' '+legend
        
    def volume(self, payload):
        #litres (measurements in cm)
        actual_vol = self.calced_vol - ((self.diam / 2.) ** 2. * 3.14 * payload/1000.) # payload variable set in serial port function
        return actual_vol
    
#t = Tanks("top",   "1", 250, 214, 40, 200, '#EA644A')
#n = Tanks("noels", "2", 200, 100, 30, 150, '#54EC48')
#s = Tanks("sals",  "3", 170,  73, 30, 150, '#7648EC')

#test data
t = Tanks("top",   "1", 100, 100, 30, 200, '#EA644A')
n = Tanks("noels", "2", 100, 100, 30, 150, '#54EC48')
s = Tanks("sals",  "3", 100, 100, 30, 150, '#7648EC')

#dict creation (key is term gleaned from incoming data, value is Tank instatnce
tank_list = [t,n,s]
tanks_by_wtopic = {tank.waterTop : tank for tank in tank_list}
tanks_by_btopic = {tank.batTop : tank for tank in tank_list}
tanks_by_topic = dict(tanks_by_wtopic.items() + tanks_by_btopic.items())
tanks_by_name = {tank.name : tank for tank in tank_list}

