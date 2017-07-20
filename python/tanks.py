import creds

class Tanks:
    def __init__(self, name, nodeID, diam, max_payload, invalid_min, min_vol):
        self.name = name
        self.nodeID = nodeID
        self.diam = diam                 #diameter of tank in cm
        self.max_payload = max_payload   #Distatnce from sensor to water outlet in tank in cm
        self.invalid_min = invalid_min   #Distatnce from sensor probe end to water level in full tank
        self.min_vol = min_vol 
        self.url = url
        self.calced_vol = ((self.diam / 2.) ** 2. * 3.14 * self.max_payload)/1000.
        self.waterTop = 'tank/water/' +name
        self.batTop = "tank/battery/" +name
        self.statusFlag = 'OK'
        self.rrdpath = '/home/pi/git/tank_lora/python/mqtt2rrd/rrd/'
        self.rrd_file = self.rrdpath +name +'.rrd'
        self.url = 'https://thingspeak.com/channels/300940'
        
    def volume(self, payload):
        #litres (measurements in cm)
        actual_vol = self.calced_vol - ((self.diam / 2.) ** 2. * 3.14 * payload/1000.) # payload variable set in serial port function
        return actual_vol
    
    def generate_png(self, length="-1d"):
        ret = rrdtool.graph(self.rrdpath +"net.png",\
                        "--start", length,\
                        "--vertical-label=Liter",\
                        "-w 400",\
                        "-h 200",\
                        'DEF:f='+self.rrd_file+':temp:AVERAGE', \
                        'LINE1:f#0000ff:'+self.name+' Water')
    
    def vol_action(self, vol):
        if vol < in_tank.min_vol:
            print self.name +' under thresh'
            if self.statusFlag == 'OK':
                self.statusFlag = 'bad'
                self.generate_png(self)
                # perform action required to send image with data
                send_graph = bot.sendPhoto(creds.group_ID, open(self.rrdpath +'net.png'), self.name +' tank')
                send = bot.sendMessage(creds.group_ID, self.name +' tank is low', reply_markup=a.format_keys(self.name))
            elif self.statusFlag == 'bad':
                print 'ignoring low level'
            else:
                print 'status flag error'        
        else:
            print 'level fine, doing nothing'
            
    def manage_callback(self, query_data):
        #callbacks for 'reset_alert' 'thingspeak link' 'fetch graph'
        if query_data == 'reset_alert':
            print self.name +' ' +self.statusFlag
            self.statusFlag = 'OK'
            print self.statusFlag
            #timer.cancel()
            bot.answerCallbackQuery(query_id, text='Alert now reset')
        elif query_data == 'fetch graph':
            graph = bot.sendMessage(creds.group_ID, self.url, reply_markup=a.format_keys(self.name))
            bot.answerCallbackQuery(query_id, text='Here you go (so demanding)') 
        elif query_data == 'thingspeak link':
            graph = bot.sendMessage(creds.group_ID, self.url, reply_markup=h.format_keys(self.name))
            bot.answerCallbackQuery(query_id, text='Here you go (so demanding)')
        elif query_data == 'help':
            bot.sendMessage(creds.group_ID, 'Send "/help" for more info', reply_markup=h.format_keys(self.name))
        
    
t = Tanks("top",   "1", 250, 214, 40, 200)
n = Tanks("noels", "2", 200, 100, 30, 150)
s = Tanks("sals",  "3", 170,  73, 30, 150)
x = Tanks("test",  "4", 170,  73, 30, 150)

#dict creation (key is term gleaned from incoming data, value is Tank instatnce
tanks_by_topic = {tank.waterTop : tank for tank in [t,n,s,x]}
tanks_by_name = {tank.name : tank for tank in [t,n,s,x]}
tank_list = [t,n,s,x]

