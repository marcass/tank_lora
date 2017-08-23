import telepot
import telepot.helper
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from telepot.delegate import (
    per_chat_id, create_open, pave_event_space, include_callback_query_chat_id)
import telepot.api
import tanks
import creds

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
                if tank.statusFlag == 'bad':
                    keyboard = InlineKeyboardMarkup(inline_keyboard=[[
                            InlineKeyboardButton(text=tank.name+' reset', callback_data=tank.name+' reset alert'),
                                InlineKeyboardButton(text='Get ' +tank.name +' graph', callback_data=tank.name+' fetch graph'),
                                ]])
                else:
                    keyboard = InlineKeyboardMarkup(inline_keyboard=[[
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
                        ],[
                            InlineKeyboardButton(text='1 hour', callback_data='1h'),
                            InlineKeyboardButton(text='3 hour', callback_data='3h'),
                            InlineKeyboardButton(text='7 hour', callback_data='7h'),
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
        help_text = "This bot will alert you to low water levels in the farm tanks. Any message you send prefixed with a '/' will be replied to by the bot. Sending the following will give you a result:\n/status or /status [tank] (or click the status button) to get tank status(es)\n/vol [days] to build a graph with custom tank volumes in it over [days] eg, /vol 10 will give you last 10 daysof data from selected tanks\n/batt [days] will similarly give you the voltage of batteries over [days] for selected tanks\n/vl [days] [tank] will plot voltage data and volume data for the specified tank, eg /vl 1 top"
        if ('/help' in text) or ('/Help' in text) or ('/start' in text):
            message = bot.sendMessage(chat_id, help_text, reply_markup=h.format_keys())
        elif ('/status' in text) or ('/Status' in text):
            #hasKey = lambda text, tanks.tanks_by_name: any(k in text for k in tanks.tanks_by_name)
            if any(k in text for k in tanks.tanks_by_name):
                in_tank = tanks.tanks_by_name[text.split(' ')[-1]]
                status_mess(in_tank, chat_id)
            else:
                status_mess('all', chat_id)
        elif ('/vol' in text) or ('/Vol' in text):# or ('/batt' in text):
            vers = 'water'
            in_msg = text.split(' ')
            msg_error = 0
            if len(in_msg) == 2:
	        days = in_msg[1]
                if days.isdigit():
                    message = bot.sendMessage(chat_id, 'Click the button for each tank you would like then click the build button when done', reply_markup=b.format_keys(tanks.tank_list, vers))
                else:
                    msg_error = 1
            else:
                msg_error = 1
            if msg_error:
                message = bot.sendMessage(chat_id, "I'm sorry, I can't recognise that. Please type '/vol [number]', eg /vol 2")
        elif '/batt' in text:
            vers = 'batt'
            in_msg = text.split(' ')
            msg_error = 0
            if len(in_msg) == 2:
	        days = in_msg[1]
                if days.isdigit():
                    message = bot.sendMessage(chat_id, 'Click the button for each tank you would like then click the build button when done', reply_markup=b.format_keys(tanks.tank_list, vers))
                else:
                    msg_error = 1
            else:
                msg_error = 1
            if msg_error:
                message = bot.sendMessage(chat_id, "I'm sorry, I can't recognise that. Please type '/batt [number]', eg /batt 2")
        elif '/vl' in text:
            in_msg = text.split(' ')
            msg_error = 0
            if len(in_msg) == 3:
                if any(k in text for k in tanks.tanks_by_name):
                    in_tank = tanks.tanks_by_name[text.split(' ')[2]]                
                    print 'in_tank = '+in_tank.name
                    days = text.split(' ')[1]
                    if days.isdigit():
                        q_length = 'days'
                        plot_tank(in_tank, days, 'bi_plot', chat_id, q_length)
                    else:
                        msg_error = 1
                else:
                    msg_error = 1
            else:
                msg_error = 1
            if msg_error:
                message = bot.sendMessage(chat_id, "I'm sorry, I can't recognise that. Please type '/vl [days] [tank name]', eg /vl 1 top")
        else:
            message = bot.sendMessage(chat_id, "I'm sorry, I don't recongnise that request (=bugger off, that does nothing). " +help_text, reply_markup=h.format_keys())
    except KeyError:
        bot.sendMessage(chat_id, "There's been a cock-up. If you haven't just been added to the alert group please let Marcus know what you just did")

def on_callback_query(msg):
    global days
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
        if 'fetch graph' in query_data:
            bot.sendMessage(target_id, query_tank.name +' would like to send you some graphs. Which would you like?', reply_markup=g.format_keys(query_tank))
            return
        elif query_data == 'status':
            status_mess(query_tank, target_id)
            return
    if query_data == 'help':
        bot.sendMessage(target_id, 'Send "/help" for more info', reply_markup=h.format_keys())
        return
    if 'add tank build' in query_data:
        if 'batt' in query_data:
            vers = 'batt'
        else: #'water' in query_data:
            vers = 'water'
        #print 'days in build = '+days
        q_length = 'days'
        plot_tank(build_list, str(days), vers, target_id, q_length)
        build_list = [] # finished build, so empty list
        return
    else: #catch all else
        if query_data == 'status':
            status_mess('all', target_id)
        elif query_data == '1' or '3' or '7' or '1h' or '3h' or '7h':
            if 'h' in query_data:
                conv = list(query_data)[0]
                q_range = 'hours'
            else:
                conv = str(query_data)
                q_range = 'days'
            in_tank_name = msg['message']['text'].split(' ')[0]
            if tanks.tanks_by_name.has_key(in_tank_name):
                graph_tank = tanks.tanks_by_name[in_tank_name]
                plot_tank(graph_tank, conv, 'water', target_id, q_range)
                return
            else:
                plot_tank(tanks.tank_list, conv, 'water', target_id, q_range)
                #bot.sendMessage(creds.group_ID, 'There you go', reply_markup=h.format_keys())
                return


TOKEN = creds.botAPIKey
botID = creds.bot_ID
bot = telepot.Bot(TOKEN)
mess_loop = MessageLoop(bot, {'chat': on_chat_message, 'callback_query': on_callback_query}).run_as_thread()
print('Listening ...')
