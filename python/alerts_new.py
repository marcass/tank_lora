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

class Tanks:
    def __init__(self, name, min_vol, url):
        self.name = name
        self.min_vol = min_vol 
        self.waterTop = "tank/water/" +name
        self.statusFlag = 'OK'
        self.url = url
    
#t = Tanks("top",   200.0, 'https://thingspeak.com/channels/300940/charts/1?bgcolor=%23ffffff&color=%23d62020&dynamic=true&results=60&title=Top+tank&type=line&xaxis=Time&yaxis=Tank+volume+%28l%29')
#n = Tanks("noels", 150.0, 'https://thingspeak.com/channels/300940/charts/2?bgcolor=%23ffffff&color=%23d62020&dynamic=true&results=60&title=Noel%27s+break+tank&type=line&xaxis=Time&yaxis=Volume+%28l%29')
#s = Tanks("sals",  150.0, 'https://thingspeak.com/channels/300940/charts/3?bgcolor=%23ffffff&color=%23d62020&dynamic=true&results=60&title=Sal%27s+bush+break+tank&type=line&xaxis=Time&yaxis=Volume+%28l%29')
#x = Tanks("test",  150.0, 'oops')

t = Tanks("top",   200.0, 'https://thingspeak.com/channels/300940')
n = Tanks("noels", 150.0, 'https://thingspeak.com/channels/300940')
s = Tanks("sals",  150.0, 'https://thingspeak.com/channels/300940')
x = Tanks("test",  150.0, 'oops')

tank_dict = {}
for tank in [t,n,s,x]:
    tank_dict[tank.name] = tank

#find the goddamn tank instance that is incoming    
def sort(val):
    for g in [t,n,s,x]:
        d = g.__dict__
        for k, v in d.items():
            if v == m:
                tank = g
                return tank
            break
#may need to handle fails here somehow

class Keyboard:
    def __init__(self, version):
        #disp = single alert, multi alert, graph request, help etc
        self.version = version
        
    def format_keys(self, tankID=0):
        if self.version == 'status':
            if tankID.statusFlag == 'OK':
                keyboard = InlineKeyboardMarkup(inline_keyboard=[[
                        InlineKeyboardButton(text='Get ' +tankID +' graph', callback_data='fetch graph'),
                        ]])
                
            else:
                keyboard = InlineKeyboardMarkup(inline_keyboard=[[
                        InlineKeyboardButton(text='Reset ' +tankID, callback_data='reset_alert'),
                        InlineKeyboardButton(text='Get ' +tankID +' graph', callback_data='fetch graph'),
                        ]])
        if self.version == 'helpMe':
            keyboard = InlineKeyboardMarkup(inline_keyboard=[[
                        InlineKeyboardButton(text='Get link to graphs', callback_data='thingspeak link'),
                        ]])
        return keyboard
    
h = Keyboard('helpMe')
s = Keyboard('status')
a = Keyboard('alert')


#tank_dict = {}
#for tank in [t,n,s,x]:
    #tank_dict[tank.name] = tank
    
#for in_tank in [t,n,s,x]:
    #tank_dict[tank.waterTop] = in_tank
    
def status_mess():
    for y in [t,n,s,x]:
        print y.name +' is ' +y.statusFlag
        

def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    text = msg['text']
    if '/help' or '/Help' in text:
        message = bot.sendMessage(creds.group_ID, 'Send /Status to see all tanks status', reply_markup=h.format_keys())
    elif '/status' or '/Status' in text:
        message = bot.sendMessage(creds.group_ID, 'Tanks status as requsted '
                                   +status_mess() , reply_markup=s.format_keys())
    else:
        message = bot.sendMessage(creds.group_ID, 'Bugger off, that does nothing. Send /help instead', reply_markup=h.format_keys())

def on_callback_query(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    print('Callback Query:', query_id, from_id, query_data)
    print 'printing message now'
    #need to get it to parse in_tank from button field here
    #get relevnet field here
    #tank = sort('relevant field')
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

TOKEN = creds.botAPIKey
botID = creds.bot_ID
bot = telepot.Bot(TOKEN)
MessageLoop(bot, {'chat': on_chat_message, 'callback_query': on_callback_query}).run_as_thread()
print('Listening ...')

#mqtt callbacks
def timeout():
    print 'Resetting alert for ' +tank.name
    tank.statusFlag = 'OK'
    
timer = Timer(4 * 60 * 60, timeout)

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe([(t.waterTop, 0), (n.waterTop, 0), (s.waterTop, 0)])

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    #print(msg.topic+' '+float(msg.payload))
    vol = float(msg.payload)
    in_tank = sort(msg.topic)
    print in_tank.name +' tank message incoming ' + 'minimum vol = ' +str(in_tank.min_vol) +' actual volume = ' +str(vol)
    if vol < in_tank.min_vol:
        print tank.name +' under thresh'
        if in_tank.statusFlag == 'OK':
            in_tank.statusFlag = 'bad'
            #timer.start()
            send = bot.sendMessage(creds.group_ID, in_tank.name +' tank is low', reply_markup=a.format_keys(in_tank.name))
            #send = bot.sendMessage(creds.marcus_ID, tank.name +' tank is low') # send alert with button for canceling status
        elif in_tank.statusFlag == 'bad':
            print 'ignoring low level'
        else:
            print 'status flag error'        
    else:
        print 'level fine, doing nothing'

#subscribe to broker and test for messages below alert values
client = mqtt.Client()
client.username_pw_set(username=creds.mosq_auth['username'], password=creds.mosq_auth['password'])
#mqtt.userdata_set(username='esp',password='heating')
client.on_connect = on_connect
client.on_message = on_message
client.connect(creds.mosq_auth['broker'], 1883, 60)
client.loop_start()


while 1:
    time.sleep(5)
