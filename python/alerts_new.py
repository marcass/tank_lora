import sys
import paho.mqtt.client as mqtt
import time
from threading import Timer
import telepot
import telepot.helper
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from telepot.delegate import (
    per_chat_id, create_open, pave_event_space, include_callback_query_chat_id)
import creds
from pprint import pprint
import json, ast
import os.path
import rrdtool

class Tanks:
    def __init__(self, name, min_vol, url):
        self.name = name
        self.min_vol = min_vol 
        self.waterTop = 'tank/water/' +name
        self.statusFlag = 'OK'
        self.url = url
        self.rrdpath = '/home/pi/git/tank_lora/python/mqtt2rrd/rrd/'
        self.rrd_file = self.rrdpath +name +'.rrd'
    
#t = Tanks("top",   200.0, 'https://thingspeak.com/channels/300940/charts/1?bgcolor=%23ffffff&color=%23d62020&dynamic=true&results=60&title=Top+tank&type=line&xaxis=Time&yaxis=Tank+volume+%28l%29')
#n = Tanks("noels", 150.0, 'https://thingspeak.com/channels/300940/charts/2?bgcolor=%23ffffff&color=%23d62020&dynamic=true&results=60&title=Noel%27s+break+tank&type=line&xaxis=Time&yaxis=Volume+%28l%29')
#s = Tanks("sals",  150.0, 'https://thingspeak.com/channels/300940/charts/3?bgcolor=%23ffffff&color=%23d62020&dynamic=true&results=60&title=Sal%27s+bush+break+tank&type=line&xaxis=Time&yaxis=Volume+%28l%29')
#x = Tanks("test",  150.0, 'oops')

t = Tanks("top",   200.0, 'https://thingspeak.com/channels/300940')
n = Tanks("noels", 150.0, 'https://thingspeak.com/channels/300940')
s = Tanks("sals",  150.0, 'https://thingspeak.com/channels/300940')
x = Tanks("test",  150.0, 'oops')

tanks_by_topic = {tank.waterTop : tank for tank in [t,n,s,x]}
tanks_by_name = {tank.name : tank for tank in [t,n,s,x]}
tank_list = [t,n,s,x]

tsL = 'https://thingspeak.com/channels/300940'

class Keyboard:
    def __init__(self, version):
        #disp = single alert, multi alert, graph request, help etc
        self.version = version
        
    def format_keys(self, tank_instance=0):
        if self.version == 'status':
            if tank_instance.statusFlag == 'OK':
                keyboard = InlineKeyboardMarkup(inline_keyboard=[[
                        InlineKeyboardButton(text='Get ' +tank_instance.name +' graph', callback_data='fetch graph'),
                        ]])
                
            else:
                keyboard = InlineKeyboardMarkup(inline_keyboard=[[
                        InlineKeyboardButton(text='Reset ' +tank_instance.name, callback_data='reset_alert'),
                        InlineKeyboardButton(text='Get ' +tank_instance.name +' graph', callback_data='fetch graph'),
                        ]])
        elif self.version == 'helpMe':
            keyboard = InlineKeyboardMarkup(inline_keyboard=[[
                        InlineKeyboardButton(text='Get link to graphs', callback_data='main thingspeak link'),
                        InlineKeyboardButton(text='Help', callback_data='help'),
                        ]])
        elif self.version == 'alert':
            keyboard = InlineKeyboardMarkup(inline_keyboard=[[
                        InlineKeyboardButton(text='Get link to ' +tank_instance.name +' graph', callback_data='graph'),
                        ]])
        else:
            keyboard = InlineKeyboardMarkup(inline_keyboard=[[
                        InlineKeyboardButton(text='Oops get link to graphs', callback_data='main thingspeak link'),
                        ]])
        return keyboard
    
h = Keyboard('helpMe')
st = Keyboard('status')
a = Keyboard('alert')
    
def status_mess(tank_instance):
    ret = tank_instance.name+' is '+tank_instance.statusFlag +'\n'
    return ret
        

def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    text = msg['text']
    if ('/help' in text) or ('/Help' in text):
        message = bot.sendMessage(creds.group_ID, 'Send /Status to see all tanks status', reply_markup=h.format_keys())
    elif ('/status' in text) or ('/Status' in text):
        print 'IM AM HERE'
        for tank in tank_list:
            message = bot.sendMessage(creds.group_ID, 
                'Status as requested \n'\
                + status_mess(tank) ,
            reply_markup=st.format_keys(tank))
    else:
        message = bot.sendMessage(creds.group_ID, 'Bugger off, that does nothing. Send /help instead', reply_markup=h.format_keys())

def on_callback_query(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    print('Callback Query:', query_id, from_id, query_data)
    print 'printing message now'
    mess = msg['message']['text']     #pull text from message
    print mess
    tank_name = mess.split(' ')[0]         #split message on spaces and get first member   
    if tanks_by_name.has_key(tank_name):
        tank = tanks_by_name[tank_name]
        #callbacks for 'reset_alert' 'thingspeak link' 'fetch graph'
        if query_data == 'reset_alert':
            print tank.name +' ' +tank.statusFlag
            tank.statusFlag = 'OK'
            print tank.statusFlag
            #timer.cancel()
            bot.answerCallbackQuery(query_id, text='Alert now reset')
        elif query_data == 'fetch graph':
            graph = bot.sendMessage(creds.group_ID, tank.url, reply_markup=a.format_keys(tank.name))
            bot.answerCallbackQuery(query_id, text='Here you go (so demanding)') 
        elif query_data == 'thingspeak link':
            graph = bot.sendMessage(creds.group_ID, tsL, reply_markup=h.format_keys(tank.name))
            bot.answerCallbackQuery(query_id, text='Here you go (so demanding)')
        elif query_data == 'help':
            bot.sendMessage(creds.group_ID, 'Send "/help" for more info', reply_markup=h.format_keys(tank.name))

TOKEN = creds.botAPIKey
botID = creds.bot_ID
bot = telepot.Bot(TOKEN)
MessageLoop(bot, {'chat': on_chat_message, 'callback_query': on_callback_query}).run_as_thread()
print('Listening ...')

#mqtt callbacks
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe([(t.waterTop, 0), (n.waterTop, 0), (s.waterTop, 0)])

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    #print(msg.topic+' '+msg.payload)
    vol = float(msg.payload)
    in_tank = tanks_by_topic[msg.topic]
    #print in_tank.name
    print in_tank.name +' tank message incoming ' + 'minimum vol = ' +str(in_tank.min_vol) +' actual volume = ' +str(vol)
    if vol < in_tank.min_vol:
        print in_tank.name +' under thresh'
        if in_tank.statusFlag == 'OK':
            in_tank.statusFlag = 'bad'
            
            generate_png(in_tank)
            # perform action required to send image with data
            send_graph = bot.sendPhoto(creds.group_ID, open(in_tank.rrdpath +'net.png'), in_tank.name +' tank')
            send = bot.sendMessage(creds.group_ID, in_tank.name +' tank is low', reply_markup=a.format_keys(in_tank.name))
        elif in_tank.statusFlag == 'bad':
            print 'ignoring low level'
        else:
            print 'status flag error'        
    else:
        print 'level fine, doing nothing'

def generate_png(tank_instance):
    #put graph in here as well https://notroot.wordpress.com/2010/03/22/python-rrdtool-tutorial/
    ret = rrdtool.graph(tank_instance.rrdpath +"net.png",\
                        "--start", "-1d",\
                        "--vertical-label=Liter",\
                        "-w 400",\
                        "-h 200",\
                    
        'DEF:f='+tank_instance.rrd_file+':temp:AVERAGE', \
        'LINE1:f#0000ff:'+tank_instance.name+' Water')

#subscribe to broker and test for messages below alert values
client = mqtt.Client()
client.username_pw_set(username=creds.mosq_auth['username'], password=creds.mosq_auth['password'])
client.on_connect = on_connect
client.on_message = on_message
client.connect(creds.mosq_auth['broker'], 1883, 60)
client.loop_start()


while 1:
    time.sleep(5)