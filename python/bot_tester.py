import sys
#import paho.mqtt.client as mqtt
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

def handle(msg):
    print (msg)
    text = msg['text']
    print (text)

#bot = telepot.Bot(creds.botAPIKey)
#MessageLoop(bot, handle).run_as_thread()

class Tanks:
    def __init__(self, name, min_vol, url):
        self.name = name
        self.min_vol = min_vol 
        self.waterTop = "tank/water/" +self.name
        self.statusFlag = 'OK'
        self.url = url
    
t = Tanks("top",   200.0, 'https://thingspeak.com/channels/300940')
n = Tanks("noels", 150.0, 'https://thingspeak.com/channels/300940')
s = Tanks("sals",  150.0, 'https://thingspeak.com/channels/300940')
x = Tanks("test",  150.0, 'oops')

#tank_list = [t, n, s, x]
#tank_status_dict = {}

   
def status_mess():
    for tank_status in [t,n,s,x]:
        a = tank_status
        print a.name +'is ' +a.statusFlag

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

def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print msg
    text = msg['text']
    if '/help' or '/Help' in text:
        message = bot.sendMessage(creds.group_ID, 'Send /Status to see all tanks status', reply_markup=s.format_keys())
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
while 1:
    time.sleep(5)
