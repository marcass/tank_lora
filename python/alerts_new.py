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
import tanks

Tanks = tanks.Tanks     #ref class as Tanks in code
tank = tanks            #eg refer to instance as tank.t

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
        tanks.manage_callback(tank, query_data)

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
    tanks.vol_acton(in_tank)

#subscribe to broker and test for messages below alert values
client = mqtt.Client()
client.username_pw_set(username=creds.mosq_auth['username'], password=creds.mosq_auth['password'])
client.on_connect = on_connect
client.on_message = on_message
client.connect(creds.mosq_auth['broker'], 1883, 60)
client.loop_start()


while 1:
    time.sleep(5)
