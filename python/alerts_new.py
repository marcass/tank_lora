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
inst = tanks            #eg refer to instance as inst.t

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
                        InlineKeyboardButton(text='Get link to graphs', callback_data='meta graph'),
                        InlineKeyboardButton(text='Help', callback_data='help'),
                        ]])
        elif self.version == 'alert':
            keyboard = InlineKeyboardMarkup(inline_keyboard=[[
                        InlineKeyboardButton(text='Reset ' +tank_instance.name, callback_data='reset_alert'),
                        ]])
        else:
            keyboard = InlineKeyboardMarkup(inline_keyboard=[[
                        InlineKeyboardButton(text='Help', callback_data='help'),
                        InlineKeyboardButton(text='Oops. get link to graphs', callback_data='meta graph'),
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
        message = bot.sendMessage(creds.group_ID, "This bot will alert you to low water levels in the farm tanks. Send /Status to see the status of all tanks", reply_markup=h.format_keys())
    elif ('/status' in text) or ('/Status' in text):
        for tank in inst.tank_list:
            message = bot.sendMessage(creds.group_ID, 
                status_mess(tank) \
                +'Status as requested',
            reply_markup=st.format_keys(tank))
    else:
        message = bot.sendMessage(creds.group_ID, "I'm sorry, I don't recongnise that request (=bugger off, that does nothing). Send /help to see a list of commands", reply_markup=h.format_keys())

def generate_png(in_tank):
    ret = rrdtool.graph(in_tank.rrdpath +"net.png",\
                    "--start", "-1d",\
                    "--vertical-label=Liter",\
                    "-w 400",\
                    "-h 200",\
                    'DEF:f='+in_tank.rrd_file+':temp:AVERAGE', \
                    'LINE1:f#0000ff:'+in_tank.name+' Water')
        
def gen_mulit_png():
    #colours = ['place holder', #00C957 , #1874CD, #FF0000]
    #use inst.t.rrdpath as it point to them all
    ret = rrdtool.graph(inst.t.rrdpath +"net.png",\
                    "--start", "-1d",\
                    "--vertical-label=Liter",\
                    "-w 400",\
                    "-h 200",\
                    'DEF:t='+inst.t.rrd_file+':temp:AVERAGE', \
                    'DEF:n='+inst.n.rrd_file+':temp:AVERAGE', \
                    'DEF:s='+inst.s.rrd_file+':temp:AVERAGE', \
                    'LINE1:#EA644A:' +inst.t.name +' Water', \
                    'LINE2:#54EC48:' +inst.n.name +' Water', \
                    'LINE3:#7648EC:' +inst.s.name +' Water')
           
    send_graph = bot.sendPhoto(creds.group_ID, open(inst.t.rrdpath +'net.png'), 'One tank graph to rule them all')
    

def on_callback_query(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    print('Callback Query:', query_id, from_id, query_data)
    print 'printing message now'
    mess = msg['message']['text']     #pull text from message
    print mess
    tank_name = mess.split(' ')[0]         #split message on spaces and get first member   
    if inst.tanks_by_name.has_key(tank_name):
        tank = inst.tanks_by_name[tank_name]
        #callbacks for 'reset_alert' 'meta graph' 'fetch graph'
        if query_data == 'reset_alert':
            print tank.name +' ' +tank.statusFlag
            tank.statusFlag = 'OK'
            print tank.statusFlag
            #timer.cancel()
            bot.answerCallbackQuery(query_id, text='Alert now reset')
        elif query_data == 'fetch graph':
            send_png('1', tank)
            bot.answerCallbackQuery(query_id, text='Here you go (so demanding)') 
        elif query_data == 'meta graph':
            graph = bot.sendMessage(creds.group_ID, tank.url, reply_markup=h.format_keys(tank))
            bot.answerCallbackQuery(query_id, text='Here you go (so demanding)')
        elif query_data == 'help':
            bot.sendMessage(creds.group_ID, 'Send "/help" for more info', reply_markup=h.format_keys(tank))
    else:
        if query_data == 'meta graph':
            gen_mulit_png()
        


TOKEN = creds.botAPIKey
botID = creds.bot_ID
bot = telepot.Bot(TOKEN)
MessageLoop(bot, {'chat': on_chat_message, 'callback_query': on_callback_query}).run_as_thread()
print('Listening ...')

#make a pretty graph and send it
def send_png(target):
    generate_png(target)
    # perform action required to send image with data
    send_graph = bot.sendPhoto(creds.group_ID, open(target.rrdpath +'net.png'), target.name +' tank graph')

#mqtt callbacks
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe([(inst.t.waterTop, 0), (inst.n.waterTop, 0), (inst.s.waterTop, 0)])

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    #print(msg.topic+' '+msg.payload)
    vol = float(msg.payload)
    in_tank = inst.tanks_by_topic[msg.topic]
    #print in_tank.name
    print in_tank.name +' tank message incoming ' + 'minimum vol = ' +str(in_tank.min_vol) +' actual volume = ' +str(vol)
    if vol < in_tank.min_vol:
        print in_tank.name +' under thresh'
        if in_tank.statusFlag == 'OK':
            in_tank.statusFlag = 'bad'
            send_png(in_tank)
            send = bot.sendMessage(creds.group_ID, in_tank.name +' tank is low', reply_markup=a.format_keys(in_tank))
        elif in_tank.statusFlag == 'bad':
            print 'ignoring low level'
        else:
            print 'status flag error'        
    else:
        print 'level fine, doing nothing'

#subscribe to broker and test for messages below alert values
client = mqtt.Client()
client.username_pw_set(username=creds.mosq_auth['username'], password=creds.mosq_auth['password'])
client.on_connect = on_connect
client.on_message = on_message
client.connect(creds.mosq_auth['broker'], 1883, 60)
client.loop_start()


while 1:
    time.sleep(5)
