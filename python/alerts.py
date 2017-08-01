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
import telepot.api

#fix for protocol error message ( see https://github.com/nickoala/telepot/issues/242 )
def always_use_new(req, **user_kw):
    return None

telepot.api._which_pool = always_use_new


Tanks = tanks.Tanks     #ref class as Tanks in code
inst = tanks            #eg refer to instance as inst.t
build_list = []

class Keyboard:
    def __init__(self, version):
        #disp = single alert, multi alert, graph request, help etc
        self.version = version
        
    def format_keys(self, tank_instance=0, tank_list=0):
        if self.version == 'status':
            if tank_instance == 0:
                key_list = []
                for tank in tank_list:
                            key_list = key_list.append(InlineKeyboardButton(text='Reset ' +tank.name, callback_data='reset_alert'),
                            InlineKeyboardButton(text='Get ' +tank.name +' graph', callback_data='fetch graph'))
                keyboard = InlineKeyboardMarkup(inline_keyboard=[key_list])
            else:
                keyboard = InlineKeyboardMarkup(inline_keyboard=[[
                        InlineKeyboardButton(text='Reset ' +tank.name, callback_data='reset_alert'),
                            InlineKeyboardButton(text='Get ' +tank.name +' graph', callback_data='fetch graph'),
                            ]])
        elif self.version == 'helpMe':
            keyboard = InlineKeyboardMarkup(inline_keyboard=[[
                        InlineKeyboardButton(text='Get composite graph', callback_data='meta graph'),
                        InlineKeyboardButton(text='Status', callback_data='status'),
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
        elif self.version == 'build':
            keyboard = InlineKeyboardMarkup(inline_keyboard=[[
                        for tank in tank_list:
                            InlineKeyboardButton(text='Add ' +tank.name, callback_data=tank+' add tank'), 
                        InlineKeyboardButton(text='Build graph', callback_data='add tank build'),
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
b = Keyboard('build')
    
def status_mess(tag):
    if tag == 'all':
        data = 'Tank status:\n'
        bad = []
        for tank in inst.tank_list:
            data = data +tank.name +' is ' +tank.statusFlag +'\n'
            if tank.statusFlag == 'bad':
                bad = bad.append(tank)
            #message = bot.sendMessage(creds.group_ID, 
            #tank.name+' is '+tank.statusFlag, reply_markup=st.format_keys(tank))
        message = bot.sendMessage(creds.group_ID, data, reply_markup=st.format_keys(0, bad))
    else:
        message = bot.sendMessage(creds.group_ID, 
            tag.name+' is '+tag.statusFlag, reply_markup=st.format_keys(tag, 0))

def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    text = msg['text']
    if ('/help' in text) or ('/Help' in text):
        message = bot.sendMessage(creds.group_ID, "This bot will alert you to low water levels in the farm tanks. Any message you send prefixed with a '/' will be replied to by the bot. Send (or click the status button) /status alone or followed by tank name (top, noels or sals to get tank status(es)\n/build [days] to build a graph with custom tanks in it over [days] (eg, 10 will give you last 10 days)\n/url to get thingspeak link for data", reply_markup=h.format_keys())
    elif ('/status' in text) or ('/Status' in text):
        #hasKey = lambda text, inst.tanks_by_name: any(k in text for k in inst.tanks_by_name)
        if any(k in text for k in inst.tanks_by_name):
            in_tank = inst.tanks_by_name[text.split(' ')[-1]]
            status_mess(in_tank)
        else:
            status_mess('all')
    elif ('/URL' in text) or ('/url' in text):
        message = bot.sendMessage(creds.group_ID, inst.t.url, reply_markup=h.format_keys())
    elif ('/build' in text) or ('/Build' in text):
        message = bot.sendMessage(creds.group_ID, 'Click the button for each tank you would like then click the build button when done', reply_markup=b.format_keys(0, inst.tank_list))
    else:
        message = bot.sendMessage(creds.group_ID, "I'm sorry, I don't recongnise that request (=bugger off, that does nothing). Commands that will do something are: \n/help to see a list of commands\n/status alone or followed by tank name (top, noels or sals to get tank status(es)\n/url to get thingspeak link for data", reply_markup=h.format_keys())

def send_png(in_tank, period, vers):
    #if (period != '1') or (period != '3') or (period != '7'):
        #period = '1'
    #"--step 3600",\ #one hour resolution
    if vers == 'water':
        label = 'Litres'
        legend = 'Water'
    if vers == 'batt':
        label = 'Volts'
        legend = 'Battery'
    print(in_tank.rrdpath +"net.png", "--start", "-" +period +"d", "--vertical-label=Liter", "-w 400", "-h 200", 'DEF:'+in_tank.name+'='+in_tank.rrdpath+vers+in_tank.name+'.rrd'+':'+vers+':AVERAGE', 'AREA1:'+in_tank.name+in_tank.line_colour+':'+in_tank.name+' '+legend)
    ret = rrdtool.graph(in_tank.rrdpath +"net.png", "--slope-mode", "--start", "end-" +period +"d", "--vertical-label="+label, "-w 400", "-h 200", 'DEF:'+in_tank.name+'='+in_tank.rrdpath+vers+in_tank.name+'.rrd'+':'+vers+':AVERAGE:step=3600', 'AREA:'+in_tank.name+in_tank.line_colour+':'+in_tank.name+' '+legend)
    send_graph = bot.sendPhoto(creds.group_ID, open(in_tank.rrdpath +'net.png'), in_tank.name +' tank graph for the '+legend)
        
def gen_multi_png(period, vers, tanks_graph):
    #hack for error: start time: There should be number after '-'
    #if (period != '1') or (period != '3') or (period != '7'):
        #period = '1'
    #use inst.t.rrdpath as it point to them all
    if vers == 'water':
        label = 'Litres'
        legend = 'Water'
    if vers == 'batt':
        label = 'Volts'
        legend = 'Battery'
    rrd_graph_comm = [inst.tank_list[0].rrdpath +"net.png", "--start", "-" +period +"d", "--vertical-label="+label,"-w 400","-h 200"]
    for objT in tank_graph:
        rrd_graph_comm.append(objT.rrd_def)
        rrd_graph_comm.append(objT.rrd_line)
        #rrd_graph_comm.append('DEF:'+objT.name+'='+objT.rrdpath+vers+objT.name+'.rrd'+':'+vers+':AVERAGE:step=3600')
        #rrd_graph_comm.append('LINE'+objT.nodeID+':'+objT.name+objT.line_colour+':'+objT.name+' '+legend)
    print(rrd_graph_comm)
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
    # do multi tank build here
    elif 'add tank' in query_data:
        if 'build' in query_data:
            gen_multi_png('2', 'water' build_list)
            build_list = [] # finished build, so empty list
        else:
            build_list = build_list.append(query_data.split(' ')[0])
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
        elif query_data == 'status':
            status_mess(tank)
        elif query_data == '1' or '3' or '7':
            conv = str(query_data)
            send_png(tank, conv, 'water')
        elif query_data == 'help':
            bot.sendMessage(creds.group_ID, 'Send "/help" for more info', reply_markup=h.format_keys(tank))
    else: #catch all else
        if query_data == 'status':
            status_mess('all')
        elif query_data == '1' or '3' or '7':
            print query_data
            conv = str(query_data)
            print('This is query_data'+query_data+'stop')
            gen_multi_png(conv, 'water')
            bot.sendMessage(creds.group_ID, 'There you go', reply_markup=h.format_keys())


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
    sub_list = []
    for var in tanks.tank_list:
        sub_list.append((var.waterTop, 0))
        sub_list.append((var.batTop, 0))
    print sub_list
    client.subscribe(sub_list)
    #client.subscribe([(inst.t.waterTop, 0), (inst.n.waterTop, 0), (inst.s.waterTop, 0)])

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+' '+msg.payload)
    vol = float(msg.payload)
    in_tank = inst.tanks_by_topic[msg.topic]
    if 'water' in msg.topic:
        #print in_tank.name
        print in_tank.name +' tank message incoming ' + 'minimum vol = ' +str(in_tank.min_vol) +' actual volume = ' +str(vol)
        if vol < in_tank.min_vol:
            print in_tank.name +' under thresh'
            if in_tank.statusFlag == 'OK':
                in_tank.statusFlag = 'bad'
                send_png(in_tank, '1', 'water')
                send = bot.sendMessage(creds.group_ID, in_tank.name +' tank is low', reply_markup=a.format_keys(in_tank))
            elif in_tank.statusFlag == 'bad':
                print 'ignoring low level'
            else:
                print 'status flag error'        
        else:
            print 'level fine, doing nothing'
    elif 'battery' in msg.topic:
        val = float(msg.payload)
        print in_tank.name +' tank battery message incoming ' + 'minimum voltage = 3.2 actual volume = ' +str(val)
        if val < 2.9:
            send_png(in_tank, '1', 'batt')

#subscribe to broker and test for messages below alert values
client = mqtt.Client()
client.username_pw_set(username=creds.mosq_auth['username'], password=creds.mosq_auth['password'])
client.on_connect = on_connect
client.on_message = on_message
client.connect(creds.mosq_auth['broker'], 1883, 60)
client.loop_start()


while 1:
    time.sleep(5)
