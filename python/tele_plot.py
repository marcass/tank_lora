import matplotlib
matplotlib.use('Agg')
import pytz
import sys
import time
import telepot
import telepot.helper
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from telepot.delegate import (
    per_chat_id, create_open, pave_event_space, include_callback_query_chat_id)
import creds
import os.path
import tanks
import telepot.api
import matplotlib.pyplot as plt
#from matplotlib.dates import DayLocator, HourLocator, DateFormatter, drange
import matplotlib.dates as md
import datetime
import sqlite3
matplotlib.rcParams['timezone'] = tanks.tz


#fix for protocol error message ( see https://github.com/nickoala/telepot/issues/242 )
def always_use_new(req, **user_kw):
    return None

telepot.api._which_pool = always_use_new

#global variables
build_list = []
#days = '1'
dur = None
sql_span = None

class Keyboard:
    def __init__(self, version):
        #disp = single alert, multi alert, graph request, help etc
        self.version = version
        
    def format_keys(self, tank=0):
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
        #elif self.version == 'graphs':
            #keyboard = InlineKeyboardMarkup(inline_keyboard=[[
                        #InlineKeyboardButton(text='1 day', callback_data='1'),
                        #InlineKeyboardButton(text='3 days', callback_data='3'),
                        #InlineKeyboardButton(text='7 days', callback_data='7'),
                        #]])
       
        elif self.version == 'plot':
            keyb_list = []
            for x in tank:
                keyb_list.append(InlineKeyboardButton(text=x.name+' ', callback_data=x.name+' add tank'))
            keyboard = InlineKeyboardMarkup(inline_keyboard=[[
                        InlineKeyboardButton(text='Plot tank volume', callback_data='volume'),
                        InlineKeyboardButton(text='Plot battery voltage', callback_data='voltage'),
                        ],[
                           InlineKeyboardButton(text='Days', callback_data='days'),
                           InlineKeyboardButton(text='Hours', callback_data='hours'), 
                           ],
                               keyb_list,
                               [InlineKeyboardButton(text='Build', callback_data='add tank build')]   
                            ])
            
        else:
            keyboard = InlineKeyboardMarkup(inline_keyboard=[[
                        InlineKeyboardButton(text='Help', callback_data='help'),
                        InlineKeyboardButton(text='Status', callback_data='status'),
                        ]])
        return keyboard
    
h = Keyboard('helpMe')
st = Keyboard('status')
a = Keyboard('alert')
#g = Keyboard('graphs')
d = Keyboard('plot')

#v = Keyboard('batt')

def localtime_from_response(resp):
    ts = datetime.datetime.strptime(resp, "%Y-%m-%d %H:%M:%S.%f")
    ts = ts.replace(tzinfo=pytz.UTC)
    return ts.astimezone(pytz.timezone(tanks.tz))
    
def query_via_tankid(tank_id, period_str, q_type):
    period = int(period_str)
    conn, c = tanks.get_db()
    #if days is not None:
    c.execute("SELECT * FROM measurements WHERE tank_id=? AND timestamp BETWEEN datetime('now', '-%i %s') AND datetime('now','localtime')" % (period, q_type), (tank_id,))
    #else:
        #c.execute("SELECT * FROM measurements WHERE tank_id=? AND timestamp BETWEEN datetime('now', '-1 days') AND datetime('now','localtime')", (tank_id,))
    ret = c.fetchall()
    timestamp = [localtime_from_response(i[0]) for i in ret]
    volume = [i[2] for i in ret]
    voltage = [i[3] for i in ret]
    ret_dict = {'timestamp':timestamp, 'tank_id':tank_id, 'water_volume':volume, 'voltage':voltage }
    #print ret_dict 
    return ret_dict

def plot_tank(tank, period, vers, target_id, q_type):
    format_date = md.DateFormatter('%H:%M\n%d-%m')
    # Note that using plt.subplots below is equivalent to using
    # fig = plt.figure and then ax = fig.add_subplot(111)
    fig, ax = plt.subplots()
    if vers == 'water':
        data = 'water_volume'
        label = 'Volume (l)'
    if vers == 'batt':
        data = 'voltage'
        label = 'Battery Voltage'
    if type(tank) is list:
        title_name = ''
        for i in tank:
            d = query_via_tankid(i.nodeID, period, q_type)
            ax.plot_date(d['timestamp'],d[data], i.line_colour, label=i.name, marker='o', markersize='5')
            title_name += ' '+i.name
            ax.set(xlabel='Datetime', ylabel=label, title='Tanks '+label)
        title_name += ' plot'
    else:
        d = query_via_tankid(tank.nodeID, period)
        if vers == 'bi_plot':
            title_name = 'Water Level and Voltage for '+tank.name+' Tank'
            ax.plot_date(d['timestamp'],d['water_volume'], 'b', label='Water Volume (l)',  marker='o', markersize='5')
            ax.set_xlabel('Time')
            # Make the y-axis label, ticks and tick labels match the line color.
            ax.set_ylabel('Water Volume', color='b')
            ax.tick_params('y', colors='b')
            ax2 = ax.twinx()
            ax2.plot_date(d['timestamp'],d['voltage'], 'r', label='Voltage (V)', marker='p', markersize='5')
            ax2.set_ylabel('Voltage', color='r')
            ax2.tick_params('y', colors='r')
        else:
            title_name = tank.name+' plot'
            ax.plot_date(d['timestamp'],d[data], tank.line_colour, label=tank.name, marker='o', markersize='5')
            ax.set(xlabel='Datetime', ylabel=label, title=tank.name+' '+label)
            plt.axhspan(tank.min_vol, tank.calced_vol, facecolor='#2ca02c', alpha=0.3)
    ax.get_xaxis().set_major_formatter(format_date)
    #times = ax.get_xticklabels()
    #plt.setp(times, rotation=30)       
    plt.legend()
    ax.grid()
    plt.tight_layout()
    fig.savefig(tanks.tank_list[0].pngpath+'net.png')
    plt.close()
    #send_graph = bot.sendPhoto(target_id, open(tanks.tank_list[0].pngpath +'net.png'), title_name)
    send_graph = bot.sendPhoto(target_id, open(tanks.tank_list[0].pngpath +'net.png'))
    
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
    global dur
    content_type, chat_type, chat_id = telepot.glance(msg)
    try:
        text = msg['text']
        help_text = "This bot will alert you to low water levels in the farm tanks. Any message you send prefixed with a '/' will be replied to by the bot. Sending the following will give you a result:\n/status or /status [tank] (or click the status button) to get tank status(es)\n/plot [number] to build a graph with custom tank volumes in it over [days/hours] \n/vl [days] [tank] will plot voltage data and volume data for the specified tank, eg /vl 1 top"#\n/url to get thingspeak link for data"
        if ('/help' in text) or ('/Help' in text) or ('/start' in text):
            message = bot.sendMessage(chat_id, help_text, reply_markup=h.format_keys())
        elif ('/status' in text) or ('/Status' in text):
            #hasKey = lambda text, tanks.tanks_by_name: any(k in text for k in tanks.tanks_by_name)
            if any(k in text for k in tanks.tanks_by_name):
                in_tank = tanks.tanks_by_name[text.split(' ')[-1]]
                status_mess(in_tank, chat_id)
            else:
                status_mess('all', chat_id)
        elif ('/Plot' in text) or ('/plot' in text):# or ('/batt' in text):
            in_msg = text.split(' ')
            msg_error = 0
            if len(in_msg) == 2:
	        dur = in_msg[1]
                if dur.isdigit():
                    message = bot.sendMessage(chat_id, 'Blay, blah', reply_markup=d.format_keys(tanks.tank_list))    
                    #message = bot.sendMessage(chat_id, 'Please select buttons that apply.\nClick Volume or Battery to plot either and set the plot for ' +dur' Hours or Days to display the data you require.\n Then click the tank(s) you require.\nFinally click the build button to produce the graph', reply_markup=dur.format_keys(tanks.tank_list))
                    #message = bot.sendMessage(chat_id, 'Click the button for each tank you would like then click the build button when done', reply_markup=b.format_keys(tanks.tank_list, vers))
                else:
                    msg_error = 1
            else:
                msg_error = 1
            if msg_error:
                message = bot.sendMessage(chat_id, "I'm sorry, I can't recognise that. Please type '/plot [number]', eg /plot 2")
        
        elif '/vl' in text:
            in_msg = text.split(' ')
            volt_error = 0
            if len(in_msg) == 3:
                if any(k in text for k in tanks.tanks_by_name):
                    in_tank = tanks.tanks_by_name[text.split(' ')[-1]]                
                    print 'in_tank = '+in_tank.name
                    days = text.split(' ')[-2]
                    if days.isdigit():
                        plot_tank(in_tank, days, 'bi_plot', chat_id)
                    else:
                        volt_error = 1
                else:
                    volt_error = 1
            else:
                volt_error = 1
            if volt_error:
                message = bot.sendMessage(chat_id, "I'm sorry, I can't recognise that. Please type '/volt_vol [days] [tank name]', eg /volt_vol 1 top")
        else:
            message = bot.sendMessage(chat_id, "I'm sorry, I don't recongnise that request (=bugger off, that does nothing). " +help_text, reply_markup=h.format_keys())
    except KeyError:
        bot.sendMessage(chat_id, "There's been a cock-up. Please let Marcus know what you just did (if it wasn't adding somebody to the chat group)")

def on_callback_query(msg):
    global dur
    global sql_span
    global build_list
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    #print('Callback Query:', query_id, from_id, query_data)
    #print msg
    target_id = msg['message']['chat']['id']
    if query_data == 'all reset':
        for tank in tanks.tank_list:
            tank.statusFlag = 'OK'
        bot.sendMessage(target_id, "All tank's status now reset to OK", reply_markup=h.format_keys())
        return
    #sort multi graph callback here
    if query_data == 'meta graph':
        bot.sendMessage(target_id, '@FarmTankbot would like to send you some graphs. Which would you like?', reply_markup=g.format_keys())
        return
    query_tank_name = query_data.split(' ')[0]
    #print 'query tank name = '+query_tank_name
    if tanks.tanks_by_name.has_key(query_tank_name):
        query_tank = tanks.tanks_by_name[query_tank_name]
        #print 'found a tank called '+query_tank.name
        if 'add tank' in query_data:
            #print 'found "add tank" in query data'
            if (query_tank not in build_list):
                print 'appending '+query_tank.name
                build_list.append(query_tank)
            else:
                print query_tank.name+' already added'
            return
        if 'reset alert' in query_data:
            #print tank.name +' ' +tank.statusFlag
            query_tank.statusFlag = 'OK'
            #print tank.statusFlag
            bot.answerCallbackQuery(query_id, text='Alert now reset')
            bot.sendMessage(target_id, query_tank.name +' reset to ' +query_tank.statusFlag)
            return
        #if 'fetch graph' in query_data:
            #bot.sendMessage(target_id, query_tank.name +' would like to send you some graphs. Which would you like?', reply_markup=g.format_keys(query_tank))
            #return
        elif query_data == 'status':
            status_mess(query_tank, target_id)
            return
    if query_data == 'help':
        bot.sendMessage(target_id, 'Send "/help" for more info', reply_markup=h.format_keys())
        return
    if 'add tank build' in query_data:
        print 'period in build = '+str(dur)+' '+sql_span
        plot_tank(build_list, str(dur), vers, target_id)
        #clear variables
        build_list = [] # finished build, so empty list
        dur = None
        sql_span = None
        return
    if 'hours' in query_data:
        sql_span = 'hours'
    if 'days' in query_data:
        sql_span = 'days'
    if 'voltage' in query_data:
        vers = 'batt'
    if 'volume' in query_data:
        vers = 'water'
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

while 1:
    time.sleep(5)
