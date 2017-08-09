import matplotlib
matplotlib.use('Agg')
matplotlib.rcParams['timezone'] = 'Pacific/Auckland'
import pytz
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
import matplotlib.pyplot as plt
#from matplotlib.dates import DayLocator, HourLocator, DateFormatter, drange
import matplotlib.dates as md
import datetime
import sqlite3


#fix for protocol error message ( see https://github.com/nickoala/telepot/issues/242 )
def always_use_new(req, **user_kw):
    return None

telepot.api._which_pool = always_use_new

#global variables
build_list = []
days = '1'

class Keyboard:
    def __init__(self, version):
        #disp = single alert, multi alert, graph request, help etc
        self.version = version
        
    def format_keys(self, tank=0, vers=0):
        if self.version == 'status':
            if type(tank) is list:
                key_list = [InlineKeyboardButton(text='Reset all', callback_data='all reset')]
                for x in tank:
                            key_list.append(InlineKeyboardButton(text=x.name +' reset', callback_data=x.name+' reset alert'))
                            #key_list.append(InlineKeyboardButton(text='Get ' +x.name +' graph', callback_data=x.name+' fetch graph'))
                #the following makes a vertical column of buttons (array of array of InlineKeyboardButton's)
                keyboard = InlineKeyboardMarkup(inline_keyboard=[[c] for c in key_list])
                #the following makes a row of buttons (hard to read when lots of alerts)
                #keyboard = InlineKeyboardMarkup(inline_keyboard=[key_list])
            else:
                keyboard = InlineKeyboardMarkup(inline_keyboard=[[
                        InlineKeyboardButton(text=tank.name+' reset', callback_data=tank.name+' reset alert'),
                            InlineKeyboardButton(text='Get ' +tank.name +' graph', callback_data=tank.name+' fetch graph'),
                            ]])
        elif self.version == 'helpMe':
            keyboard = InlineKeyboardMarkup(inline_keyboard=[[
                        InlineKeyboardButton(text='Get composite graph of all tanks', callback_data='meta graph'),
                        InlineKeyboardButton(text='Status', callback_data='status'),
                        ]])
        elif self.version == 'alert':
            keyboard = InlineKeyboardMarkup(inline_keyboard=[[
                        InlineKeyboardButton(text=tank.name+' reset', callback_data=tank.name +' reset alert'),
                        ]])
        elif self.version == 'graphs':
            keyboard = InlineKeyboardMarkup(inline_keyboard=[[
                        InlineKeyboardButton(text='1 day', callback_data='1'),
                        InlineKeyboardButton(text='3 days', callback_data='3'),
                        InlineKeyboardButton(text='7 days', callback_data='7'),
                        ]])
        elif self.version == 'build':
            keyb_list = []
            for x in tank:
                keyb_list.append(InlineKeyboardButton(text=x.name+' ', callback_data=x.name+' add tank')) 
            keyb_list.append(InlineKeyboardButton(text='Build', callback_data='add tank build ' +vers))
            #print keyb_list
            keyboard = InlineKeyboardMarkup(inline_keyboard=[keyb_list])
        #elif self.version == 'batt':
            
        else:
            keyboard = InlineKeyboardMarkup(inline_keyboard=[[
                        InlineKeyboardButton(text='Help', callback_data='help'),
                        InlineKeyboardButton(text='Status', callback_data='status'),
                        ]])
        return keyboard
    
h = Keyboard('helpMe')
st = Keyboard('status')
a = Keyboard('alert')
g = Keyboard('graphs')
b = Keyboard('build')
#v = Keyboard('batt')

def localtime_from_response(resp):
    ts = datetime.datetime.strptime(resp, "%Y-%m-%d %H:%M:%S.%f")
    ts = ts.replace(tzinfo=pytz.UTC)
    return ts.astimezone(pytz.timezone('Pacific/Auckland'))
    
def query_via_tankid(tank_id, days_str):
    days = int(days_str)
    conn, c = tanks.get_db()
    #if days is not None:
    c.execute("SELECT * FROM measurements WHERE tank_id=? AND timestamp BETWEEN datetime('now', '-%i days') AND datetime('now','localtime')" % (days), (tank_id,))
    #else:
        #c.execute("SELECT * FROM measurements WHERE tank_id=? AND timestamp BETWEEN datetime('now', '-1 days') AND datetime('now','localtime')", (tank_id,))
    ret = c.fetchall()
    timestamp = [localtime_from_response(i[0]) for i in ret]
    volume = [i[2] for i in ret]
    voltage = [i[3] for i in ret]
    ret_dict = {'timestamp':timestamp, 'tank_id':tank_id, 'water_volume':volume, 'voltage':voltage }
    #print ret_dict 
    return ret_dict

def plot_tank(tank, period, vers, target_id):
    if vers == 'water':
        data = 'water_volume'
        label = 'volume (l)'
    else: #must be voltage
        data = 'voltage'
        label = data
    format_date = md.DateFormatter('%d-%m\n%H:%M')
    # Note that using plt.subplots below is equivalent to using
    # fig = plt.figure and then ax = fig.add_subplot(111)
    fig, ax = plt.subplots()
    if type(tank) is list:
        title_name = ''
        for i in tank:
            d = query_via_tankid(i.nodeID, period)
            ax.plot_date(d['timestamp'],d[data], i.line_colour, label=i.name, marker='o', markersize='5')
            title_name += ' '+i.name
            ax.set(xlabel='time', ylabel=label, title='Tanks '+data)
    else:
        title_name = tank.name
        d = query_via_tankid(tank.nodeID, period)  
        ax.plot_date(d['timestamp'],d[data], tank.line_colour, label=tank.name, marker='o', markersize='5')
        ax.set(xlabel='time', ylabel=label, title=tank.name+' '+data)
    ax.get_xaxis().set_major_formatter(format_date)
    times = ax.get_xticklabels()
    #plt.setp(times, rotation=30)
    plt.legend()
    ax.grid()
    plt.tight_layout()
    fig.savefig(tanks.tank_list[0].pngpath+'net.png')
    plt.close()
    send_graph = bot.sendPhoto(target_id, open(tanks.tank_list[0].pngpath +'net.png'), title_name +' tank graph for '+label)
    
def status_mess(tag, chat_id):
    if tag == 'all':
        data = 'Tank status:\n'
        bad = []
        for tank in tanks.tank_list:
            data = data +tank.name +' is ' +tank.statusFlag +'\n'
            if tank.statusFlag == 'bad':
                bad.append(tank)
            #message = bot.sendMessage(creds.group_ID, 
            #tank.name+' is '+tank.statusFlag, reply_markup=st.format_keys(tank))
        message = bot.sendMessage(chat_id, data, reply_markup=st.format_keys(bad))
    else:
        message = bot.sendMessage(chat_id, tag.name+' is '+tag.statusFlag, reply_markup=st.format_keys(tag))

def on_chat_message(msg):
    global days
    content_type, chat_type, chat_id = telepot.glance(msg)
    try:
        text = msg['text']
        if ('/help' in text) or ('/Help' in text):
            #message = bot.sendMessage(creds.group_ID, "This bot will alert you to low water levels in the farm tanks. Any message you send prefixed with a '/' will be replied to by the bot. Send (or click the status button) /status alone or followed by tank name (top, noels or sals to get tank status(es)\n/build [days] to build a graph with custom tanks in it over [days] (eg, /build 10 will give you last 10 days)\n/url to get thingspeak link for data", reply_markup=h.format_keys())
            message = bot.sendMessage(chat_id, "This bot will alert you to low water levels in the farm tanks. Any message you send prefixed with a '/' will be replied to by the bot. Send (or click the status button) /status alone or followed by tank name (top, noels or sals to get tank status(es)\n/build [days] to build a graph with custom tanks in it over [days] (eg, /build 10 will give you last 10 days)\n/url to get thingspeak link for data", reply_markup=h.format_keys())
        elif ('/status' in text) or ('/Status' in text):
            #hasKey = lambda text, tanks.tanks_by_name: any(k in text for k in tanks.tanks_by_name)
            if any(k in text for k in tanks.tanks_by_name):
                in_tank = tanks.tanks_by_name[text.split(' ')[-1]]
                status_mess(in_tank, chat_id)
            else:
                status_mess('all', chat_id)
        elif ('/URL' in text) or ('/url' in text):
            message = bot.sendMessage(creds.group_ID, tanks.t.url, reply_markup=h.format_keys())
        elif ('/build' in text) or ('/Build' in text) or ('/batt' in text):
            if '/batt' in text:
                vers = 'batt'
            else:
                vers = 'water'
            in_msg = text.split(' ')
            msg_error = 0
            if len(in_msg) == 2:
	        days = in_msg[1]
                #print 'days = '+days
                if days.isdigit():
                    message = bot.sendMessage(chat_id, 'Click the button for each tank you would like then click the build button when done', reply_markup=b.format_keys(tanks.tank_list, vers))
                else:
                    msg_error = 1
            else:
                msg_error = 1
            if msg_error:
                message = bot.sendMessage(chat_id, "I'm sorry, I can't recognise that. Please type '/build [number]', eg /build 2")
        elif '/batt' in text:
            in_msg = text.split(' ')
            msg_error = 0
            if len(in_msg) == 2:
	        days = in_msg[1]
                #print 'days = '+days
                if days.isdigit():
                    message = bot.sendMessage(chat_id, 'Click the button for each tank you would like then click the build button when done', reply_markup=v.format_keys(tanks.tank_list))
                else:
                    msg_error = 1
            else:
                msg_error = 1
            if msg_error:
                message = bot.sendMessage(chat_id, "I'm sorry, I can't recognise that. Please type '/batt [number]', eg /batt 2")
        else:
            message = bot.sendMessage(chat_id, "I'm sorry, I don't recongnise that request (=bugger off, that does nothing). Commands that will do something are: \n/help to see a list of commands\n/status alone or followed by tank name (top, noels or sals to get tank status(es)\n/url to get thingspeak link for data", reply_markup=h.format_keys())
    except KeyError:
        bot.sendMessage(chat_id, "There's been a cock-up. Please let Marcus know what you just did")

def on_callback_query(msg):
    global days
    global build_list
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    print('Callback Query:', query_id, from_id, query_data)
    print msg
    target_id = msg['message']['chat']['id']
    #mess = msg['message']['text']     #pull text from message
    #tank_name = mess.split(' ')[0]         #split message on spaces and get first member 
    if query_data == 'all reset':
        for tank in tanks.tank_list:
            tank.statusFlag = 'OK'
        bot.sendMessage(target_id, "All tank's status now reset to OK", reply_markup=h.format_keys())
        return
    #sort multi graph callback here
    if query_data == 'meta graph':
        bot.sendMessage(target_id, '@FarmTankbot would like to send you some graphs. Which would you like?', reply_markup=g.format_keys())
        return
    # do multi tank build here
    query_tank_name = query_data.split(' ')[0]
    print 'query tank name = '+query_tank_name
    if tanks.tanks_by_name.has_key(query_tank_name):
        query_tank = tanks.tanks_by_name[query_tank_name]
        print 'found a tank called '+query_tank.name
        if 'add tank' in query_data:
            print 'found "add tank" in query data'
            print 'appending '+query_tank.name
            build_list.append(query_tank)
            return
        #elif tanks.tanks_by_name.has_key(tank_name):
            #tank = tanks.tanks_by_name[tank_name]
        #callbacks for 'reset alert' 'meta graph' 'fetch graph'
        if 'reset alert' in query_data:
            #print tank.name +' ' +tank.statusFlag
            query_tank.statusFlag = 'OK'
            #print tank.statusFlag
            bot.answerCallbackQuery(query_id, text='Alert now reset')
            bot.sendMessage(target_id, query_tank.name +' reset to ' +query_tank.statusFlag)
            return
        if 'fetch graph' in query_data:
            bot.sendMessage(target_id, query_tank.name +' would like to send you some graphs. Which would you like?', reply_markup=g.format_keys(query_tank))
            return
        elif query_data == 'status':
            status_mess(query_tank, target_id)
            return
        #elif query_data == '1' or '3' or '7':
            #conv = str(query_data)
            #send_png(query_tank, conv, 'water')
            #return
    if query_data == 'help':
        bot.sendMessage(target_id, 'Send "/help" for more info', reply_markup=h.format_keys())
        return
    if 'add tank build' in query_data:
        if 'batt' in query_data:
            vers = 'batt'
        else: #'water' in query_data:
            vers = 'water'
        print 'days in build = '+days
        plot_tank(build_list, str(days), vers, target_id)
        build_list = [] # finished build, so empty list
        return
    else: #catch all else
        if query_data == 'status':
            status_mess('all', target_id)
        elif query_data == '1' or '3' or '7':
            #print query_data
            conv = str(query_data)
            in_tank_name = msg['message']['text'].split(' ')[0]
            print 'tanks is '+in_tank_name
            if tanks.tanks_by_name.has_key(in_tank_name):
                graph_tank = tanks.tanks_by_name[in_tank_name]
                print 'tank is '+graph_tank.name
                plot_tank(graph_tank, conv, 'water', target_id)
                return
            else:
                plot_tank(tanks.tank_list, conv, 'water', target_id)
                #bot.sendMessage(creds.group_ID, 'There you go', reply_markup=h.format_keys())
                return


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
    #print sub_list
    client.subscribe(sub_list)
    #client.subscribe([(tanks.t.waterTop, 0), (tanks.n.waterTop, 0), (tanks.s.waterTop, 0)])

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+' '+msg.payload)
    vol = float(msg.payload)
    in_tank = tanks.tanks_by_topic[msg.topic]
    if 'water' in msg.topic:
        #print in_tank.name
        print in_tank.name +' tank message incoming ' + 'minimum vol = ' +str(in_tank.min_vol) +' actual volume = ' +str(vol)
        if vol < in_tank.min_vol:
            print in_tank.name +' under thresh'
            if in_tank.statusFlag == 'OK':
                in_tank.statusFlag = 'bad'
                plot_tank(in_tank, '1', 'water', creds.group_ID)
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
            plot_tank(in_tank, '1', 'batt',creds.group_ID)

#subscribe to broker and test for messages below alert values
client = mqtt.Client()
client.username_pw_set(username=creds.mosq_auth['username'], password=creds.mosq_auth['password'])
client.on_connect = on_connect
client.on_message = on_message
client.connect(creds.mosq_auth['broker'], 1883, 60)
client.loop_start()


while 1:
    time.sleep(5)
