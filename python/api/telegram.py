# Telegram messaging
import telepot
import telepot.helper
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from telepot.delegate import (
    per_chat_id, create_open, pave_event_space, include_callback_query_chat_id)
import telepot.api
import creds
import sql
import plot

# stupid global variables
build_list = []
build_colour = []
build_id = []
vers = None
dur = None
# ########### Alert stuff ########################
# #fix for protocol error message ( see https://github.com/nickoala/telepot/issues/242 )
def always_use_new(req, **user_kw):
    return None

telepot.api._which_pool = always_use_new

class Keyboard:
    def __init__(self, version):
        #disp = single alert, multi alert, graph request, help etc
        self.version = version

    def format_keys(self, key_tank=0):
        #print 'in tank is '+str(key_tank)
        if self.version == 'status':
            if type(key_tank) is list:
                key_list = [InlineKeyboardButton(text='Reset all', callback_data='all reset')]
                for x in key_tank:
                    key_list.append(InlineKeyboardButton(text=x +' reset', callback_data=x+' reset alert'))
                #the following makes a vertical column of buttons (array of array of InlineKeyboardButton's)
                keyboard = InlineKeyboardMarkup(inline_keyboard=[[c] for c in key_list])
                #the following makes a row of buttons (hard to read when lots of alerts)
                #keyboard = InlineKeyboardMarkup(inline_keyboard=[key_list])
            else:
                if key_tank['level_status'] == 'bad':
                    keyboard = InlineKeyboardMarkup(inline_keyboard=[[
                        InlineKeyboardButton(text=key_tank['name']+' reset', callback_data=key_tank['name']+' reset alert'),
                            InlineKeyboardButton(text='Get ' +key_tank['name'] +' graph', callback_data=key_tank['name']+' fetch graph'),
                            ]])
                else:
                   keyboard = InlineKeyboardMarkup(inline_keyboard=[[
                            InlineKeyboardButton(text='Get ' +key_tank['name'] +' graph', callback_data=key_tank['name']+' fetch graph'),
                             ]])
        elif self.version == 'battstatus':
            key_list = [InlineKeyboardButton(text='Reset all', callback_data='batt reset')]
            for x in key_tank:
                        key_list.append(InlineKeyboardButton(text=x['name'] +' reset', callback_data=x['name']+' reset batt'))
                        #key_list.append(InlineKeyboardButton(text='Get ' +x.name +' graph', callback_data=x.name+' fetch graph'))
            #the following makes a vertical column of buttons (array of array of InlineKeyboardButton's)
            keyboard = InlineKeyboardMarkup(inline_keyboard=[[c] for c in key_list])
        elif self.version == 'helpMe':
            keyboard = InlineKeyboardMarkup(inline_keyboard=[[
                        InlineKeyboardButton(text='Status', callback_data='status'),
                        ]])
        elif self.version == 'alert':
            keyboard = InlineKeyboardMarkup(inline_keyboard=[[
                        InlineKeyboardButton(text=key_tank['name']+' reset', callback_data=key_tank['name'] +' reset alert'),
                        ]])
        elif self.version == 'graphs':
            keyboard = InlineKeyboardMarkup(inline_keyboard=[[
                        InlineKeyboardButton(text='1 day', callback_data='1'),
                        InlineKeyboardButton(text='3 days', callback_data='3'),
                        InlineKeyboardButton(text='7 days', callback_data='7'),
                        ]])

        elif self.version == 'plot':
            keyb_list = []
            for x in key_tank:
                keyb_list.append(InlineKeyboardButton(text=x+' ', callback_data=x+' add tank'))
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
g = Keyboard('graphs')
d = Keyboard('plot')
battst = Keyboard('battstatus')

def send_graph(target_id, graph):
    #  bot.sendPhoto(target_id, open(tanks.tank_list[0].pngpath +'net.png'))
    try:
        bot.sendPhoto(target_id, graph)
    except:
        print('graph send failed')

def messages(target_id, text):
    bot.sendMessage(target_id, text)

def on_chat_message(msg):
    #print 'message received'
    #print msg
    global dur
    global vers
    content_type, chat_type, chat_id = telepot.glance(msg)
    try:
        text = msg['text']
        tank_data = sql.get_all_tanks()
        tank_names = tank_data['name']
        help_text = "This bot will alert you to low water levels in the farm tanks. Any message you send will be replied to by the bot. If it is not formatted correctly you will get this message again. Sending the following will give you a result:\n'/status' to get the status of all tanks  (or click the status button)\n'/status [tank name]' to get individual tank status with the option to graph them. Valid names are: "+str(tank_names)+" \n'/plot [number of days/hours]' to build a graph with custom tank volumes in it over [days/hours]"
        if ('/help' in text) or ('/Help' in text) or ('/start' in text):
            message = bot.sendMessage(chat_id, help_text, reply_markup=h.format_keys())
        elif ('/status' in text) or ('/Status' in text):
            if any(k in text for k in tank_names):
                in_tank = text.split(' ')[-1]
                status_mess(in_tank, chat_id)
            else:
                status_mess('all', chat_id)
        elif ('/Plot' in text) or ('/plot' in text):# or ('/batt' in text):
            #reset variables
            dur = None
            sql_span = None
            vers = None
            in_msg = text.split(' ')
            msg_error = 0
            if len(in_msg) == 2:
                dur = in_msg[1]
                if dur.isdigit():
                    #message = bot.sendMessage(chat_id, 'Blay, blah', reply_markup=d.format_keys(tanks.tank_list))
                    message = bot.sendMessage(chat_id, "Please select the button(s) that apply in each row of buttons, then click the 'Build' button to produce the graph", reply_markup=d.format_keys(tank_names))
                    #message = bot.sendMessage(chat_id, 'Click the button for each tank you would like then click the build button when done', reply_markup=b.format_keys(tanks.tank_list, vers))
                else:
                    msg_error = 1
            else:
                msg_error = 1
            if msg_error:
                message = bot.sendMessage(chat_id, "I'm sorry, I can't recognise that. Please type '/plot [number]', eg /plot 2")
        elif "/battstatus" in text:
            battstatus_mess(chat_id)
        else:
            message = bot.sendMessage(chat_id, "I'm sorry, I don't recongnise that request (=bugger off, that does nothing). " +help_text, reply_markup=h.format_keys())
    except KeyError:
        bot.sendMessage(chat_id, "There's been a cock-up. Please let Marcus know what you just did (if it wasn't adding somebody to the chat group)")

def on_callback_query(msg):
    global dur
    global sql_span
    global build_list
    global build_colour
    global build_id
    global vers
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    print(('Callback Query:', query_id, from_id, query_data))
    #print msg
    tank_data = sql.get_all_tanks()
    target_id = msg['message']['chat']['id']
    if query_data == 'all reset':
        #print 'resetting all on callback'
        for x in tank_data['name']:
            sql.write_tank_col(x, 'tank_status', 'OK')
        bot.sendMessage(target_id, "All tank's status now reset to OK", reply_markup=h.format_keys())
        return
    query_tank_name = query_data.split(' ')[0]
    if query_data == 'batt reset':
        for x in tank_data['name']:
            sql.write_tank_col(tank_data['name'][x], 'batt_status', 'OK')
        bot.sendMessage(target_id, "All tank's battery status now reset to OK", reply_markup=h.format_keys())
    #print 'query tank name = '+query_tank_name
    if query_tank_name in tank_data['name']:
        # it's in the list so lets get index:
        i = tank_data['name'].index(query_tank_name)
        query_tank = tank_data['name'][i]
        query_tank_colour = tank_data['line_colour'][i]
        query_tank_id = tank_data['id'][i]
        #print 'found a tank called '+query_tank.name
        if 'add tank' in query_data:
            #print 'found "add tank" in query data'
            if (query_tank not in build_list):
                #print 'appending '+query_tank.name
                build_list.append(query_tank)
                build_colour.append(query_tank_colour)
                build_id.append(query_tank_id)
            else:
                print(query_tank+' already added')
            return
        if 'reset batt' in query_data:
            sql.write_tank_col(tank_data['name'][i], 'batt_status', 'OK')
        if 'reset alert' in query_data:
            #print tank.name +' ' +tank.statusFlag
            #print 'resetting all on callback individually'
            sql.write_tank_col(tank_data['name'][i], 'tank_status', 'OK')
            #print tank.statusFlag
            bot.answerCallbackQuery(query_id, text='Alert now reset')
            bot.sendMessage(target_id, query_tank +' reset to OK')
            return
        if 'fetch graph' in query_data:
            bot.sendMessage(target_id, query_tank +' would like to send you some graphs. Which would you like?', reply_markup=g.format_keys(query_tank))
            return
        elif query_data == 'status':
            status_mess(query_tank, target_id)
            return
    if query_data == 'help':
        bot.sendMessage(target_id, 'Send "/help" for more info', reply_markup=h.format_keys())
        return
    if 'add tank build' in query_data:
        if vers == None:
            bot.sendMessage(target_id, 'Please select a data type to plot (Voltage or Volume) by clicking the approriate button above')
        #print 'period in build = '+str(dur)+' '+sql_span
        # create a dict with required into for plotting
        build_dict = {'line_colour':build_colour, 'name':build_list, 'id':build_id}
        send_graph(target_id, plot.plot_tank_list(build_dict, dur, sql_span, vers))
        #clear variables
        build_id = []
        build_colour = []
        build_list = [] # finished build, so empty list
        return
    if 'hours' in query_data:
        #print 'added ' +query_data +' to options'
        sql_span = 'hours'
        return
    if 'days' in query_data:
        #print 'added ' +query_data +' to options'
        sql_span = 'days'
        return
    if 'voltage' in query_data:
        #print 'added ' +query_data +' to options'
        vers = 'batt'
        return
    if 'volume' in query_data:
        #print 'added ' +query_data +' to options'
        vers = 'water'
        return
    if query_data == 'status':
        status_mess('all', target_id)
        return
    if query_data == '1' or '3' or '7':
        #print query_data
        conv = str(query_data)
        in_tank_name = msg['message']['text'].split(' ')[0]
        #print 'tank is '+in_tank_name
        print(tank_data)
        if in_tank_name in tank_data['name']:
            i = tank_data['name'].index(in_tank_name)
            vers = 'water'
            send_graph(target_id, plot.plot_tank_raw(tank_data['name'][i], tank_data['id'][i], tank_data['line_colour'][i], query_data, 'days', vers))
            vers = None
            return

def status_mess(tag, chat_id):
    if tag == 'all':
        data = 'Tank water status:\n'
        bad = []
        tanks_list = sql.get_all_tanks()
        for x in tanks_list['name']:
            index = tanks_list['name'].index(x)
            data = data +tanks_list['name'][index] +' is ' +tanks_list['level_status'][index] +'\n'
            if tanks_list['level_status'][index] == 'bad':
                bad.append(tanks_list['name'][index])
        message = bot.sendMessage(chat_id, data, reply_markup=st.format_keys(bad))
    else:
        tank_stuff = sql.get_tank(tag, 'tank')
        message = bot.sendMessage(chat_id, tank_stuff['name']+' is '+tank_stuff['level_status'], reply_markup=st.format_keys(tank_stuff))

def battstatus_mess(chat_id):
    data = 'Tank battery status:\n'
    bad = []
    tanks_list = sql.get_all_tanks()
    for x in tanks_list['name']:
        index = tanks_list['name'].index(x)
        data = data +tanks_list['name'][index] +' is ' +tanks_list['batt_status'][index] +'\n'
        if tanks_list['level_status'][index] == 'low':
            bad.append(x)
    message = bot.sendMessage(chat_id, data, reply_markup=battst.format_keys(bad))

#TOKEN = creds.testbotAPIKey
TOKEN = creds.botAPIKey
botID = creds.bot_ID
bot = telepot.Bot(TOKEN)

# #start the message bot
# MessageLoop(bot, {'chat': on_chat_message, 'callback_query': on_callback_query}).run_as_thread()
# print('Listening ...')
