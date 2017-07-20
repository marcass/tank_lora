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
                        InlineKeyboardButton(text='Get composite graph', callback_data='meta graph'),
                        ]])
                
            else:
                keyboard = InlineKeyboardMarkup(inline_keyboard=[[
                        InlineKeyboardButton(text='Reset ' +tank_instance.name, callback_data='reset_alert'),
                        InlineKeyboardButton(text='Get ' +tank_instance.name +' graph', callback_data='fetch graph'),
                        ]])
        elif self.version == 'helpMe':
            keyboard = InlineKeyboardMarkup(inline_keyboard=[[
                        InlineKeyboardButton(text='Get composite graph', callback_data='meta graph'),
                        InlineKeyboardButton(text='Help', callback_data='help'),
                        ]])
        elif self.version == 'alert':
            keyboard = InlineKeyboardMarkup(inline_keyboard=[[
                        InlineKeyboardButton(text='Reset ' +tank_instance.name, callback_data='reset_alert'),
                        ]])
        elif self.version == 'graphs':
            keyboard = InlineKeyboardMarkup(inline_keyboard=[[
                        InlineKeyboardButton(text='1 day', callback_data='1'),
                        InlineKeyboardButton(text='3 days', callback_data='3'),
                        InlineKeyboardButton(text='7 days', callback_data='7'),
                        ]])
        else:
            keyboard = InlineKeyboardMarkup(inline_keyboard=[[
                        InlineKeyboardButton(text='Help', callback_data='help'),
                        InlineKeyboardButton(text='Oops. get link to graphs', callback_data='meta graph'),
                        InlineKeyboardButton(text='Status', callback_data='status'),
                        ]])
        return keyboard
    
h = Keyboard('helpMe')
st = Keyboard('status')
a = Keyboard('alert')
g = Keyboard('graphs')
    
def status_mess():
    for tank in inst.tank_list:
        message = bot.sendMessage(creds.group_ID, 
           tank.name+' is '+tank.statusFlag, reply_markup=st.format_keys(tank))
        

def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    text = msg['text']
    if ('/help' in text) or ('/Help' in text):
        message = bot.sendMessage(creds.group_ID, "This bot will alert you to low water levels in the farm tanks. Send /Status to see the status of all tanks", reply_markup=h.format_keys())
    elif ('/status' in text) or ('/Status' in text):
        status_mess()
    else:
        message = bot.sendMessage(creds.group_ID, "I'm sorry, I don't recongnise that request (=bugger off, that does nothing). Send /help to see a list of commands", reply_markup=h.format_keys())

def send_png(in_tank, period):
    ret = rrdtool.graph(in_tank.rrdpath +"net.png",\
                    "--start", "-" +period +"d",\
                    "--vertical-label=Liter",\
                    "-w 400",\
                    "-h 200",\
                    'DEF:'+in_tank.name+'='+in_tank.rrd_file+':level:AVERAGE', \
                    'LINE1:'+in_tank.name+in_tank.line_colour+':'+in_tank.name+' Water')
    send_graph = bot.sendPhoto(creds.group_ID, open(in_tank.rrdpath +'net.png'), in_tank.name +' tank graph')
        
def gen_mulit_png(period):
    #use inst.t.rrdpath as it point to them all
    rrd_graph_comm = [inst.t.rrdpath +"net.png", "--start", "-" +period +"d", "--vertical-label=Liter","-w 400","-h 200"]
    for objT in inst.tank_list:
        rrd_graph_comm.append('DEF:'+objT.name+'='+objT.rrd_file+':level:AVERAGE')
        rrd_graph_comm.append('LINE'+objT.nodeID+':'+objT.name+objT.line_colour+':'+objT.name+' Water')
    ret = rrdtool.graph(rrd_graph_comm)
    send_graph = bot.sendPhoto(creds.group_ID, open(inst.t.rrdpath +'net.png'), 'One tank graph to rule them all')
    

def on_callback_query(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    #print('Callback Query:', query_id, from_id, query_data)
    mess = msg['message']['text']     #pull text from message
    tank_name = mess.split(' ')[0]         #split message on spaces and get first member   
    #sort multi graph callback here
    if query_data == 'meta graph':
        bot.sendMessage(creds.group_ID, '@FarmTankbot would like to send you some graphs. Which would you like?', reply_markup=g.format_keys())
    elif inst.tanks_by_name.has_key(tank_name):
        tank = inst.tanks_by_name[tank_name]
        #callbacks for 'reset_alert' 'meta graph' 'fetch graph'
        if query_data == 'reset_alert':
            print tank.name +' ' +tank.statusFlag
            tank.statusFlag = 'OK'
            print tank.statusFlag
            #timer.cancel()
            bot.answerCallbackQuery(query_id, text='Alert now reset')
            bot.sendMessage(creds.group_ID, tank.name +' reset to ' +tank.statusFlag, reply_markup=h.format_keys())
        elif query_data == 'fetch graph':
            bot.sendMessage(creds.group_ID, tank.name +' would like to send you some graphs. Which would you like?', reply_markup=g.format_keys(tank))
        elif query_data == '1' or '3' or '7':
            conv = str(query_data)
            send_png(tank, conv)
        elif query_data == 'help':
            bot.sendMessage(creds.group_ID, 'Send "/help" for more info', reply_markup=h.format_keys(tank))
    else: #catch all else
        if query_data == '1' or '3' or '7':
            conv = str(query_data)
            gen_mulit_png(conv)
            bot.sendMessage(creds.group_ID, 'There you go', reply_markup=h.format_keys())
        elif query_data == 'status':
            status_mess()


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
            send_png(in_tank, '1')
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
