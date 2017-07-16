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

"""
$ python3.5 tank_alert.py <token>
prev 'Lover.py' from https://github.com/nickoala/telepot/blob/master/examples/callback/lover.py

"""

#propose_records = telepot.helper.SafeDict()  # thread-safe dict

class Tanks:
    def __init__(self, name, min_vol, url):
        self.name = name
        self.min_vol = min_vol 
        self.waterTop = "tank/water/" +self.name
        self.statusFlag = 'OK'
        self.url = url
    
t = Tanks("top",   200.0, 'https://thingspeak.com/channels/300940/charts/1?bgcolor=%23ffffff&color=%23d62020&dynamic=true&results=60&title=Top+tank&type=line&xaxis=Time&yaxis=Tank+volume+%28l%29')
n = Tanks("noels", 150.0, 'https://thingspeak.com/channels/300940/charts/2?bgcolor=%23ffffff&color=%23d62020&dynamic=true&results=60&title=Noel%27s+break+tank&type=line&xaxis=Time&yaxis=Volume+%28l%29')
s = Tanks("sals",  150.0, 'https://thingspeak.com/channels/300940/charts/3?bgcolor=%23ffffff&color=%23d62020&dynamic=true&results=60&title=Sal%27s+bush+break+tank&type=line&xaxis=Time&yaxis=Volume+%28l%29')
x = Tanks("test",  150.0, 'oops')

tank_dict = {}
for tank in [t,n,s,x]:
    tank_dict[tank.waterTop] = tank
    
for in_tank in [t,n,s,x]:
    tank_dict[in_tank.name] = in_tank

keyboard = InlineKeyboardMarkup(inline_keyboard=[[
                   InlineKeyboardButton(text='All OK now', callback_data='reset_alert'),
                   InlineKeyboardButton(text='Get graph', callback_data='fetch graph'),
               ]])

def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)

def on_callback_query(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    print('Callback Query:', query_id, from_id, query_data)
    print 'printing message now'
    asc_msg = ast.literal_eval(json.dumps(msg))
    pprint(asc_msg)
    chat_msg = asc_msg['message']['text']
    print chat_msg
    #tank_in_chat_msg = chat_msg.split(' ')[1:]
    in_tank_array = chat_msg.split(' ')[:1]
    in_tank = tank_dict[in_tank_array[0]]
    print 'identified tank is ' +in_tank.name
    if query_data == 'reset_alert':
        print in_tank.name +' ' +in_tank.statusFlag
        in_tank.statusFlag = 'OK'
        print in_tank.statusFlag
        #timer.cancel()
        bot.answerCallbackQuery(query_id, text='Alert now reset')
    elif query_data == 'fetch graph':
        graph = bot.sendMessage(creds.marcus_ID, in_tank.name +' tank is low ' +in_tank.url, reply_markup=keyboard)
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
    tank = tank_dict[msg.topic]
    print tank.name +' tank message incoming ' + 'minimum vol = ' +str(tank.min_vol) +' actual volume = ' +str(vol)
    if vol < tank.min_vol:
        print tank.name +' under thresh'
        if tank.statusFlag == 'OK':
            tank.statusFlag = 'New alert'
            #timer.start()
            send = bot.sendMessage(creds.marcus_ID, tank.name +' tank is low', reply_markup=keyboard)
            #send = bot.sendMessage(creds.marcus_ID, tank.name +' tank is low') # send alert with button for canceling status
        elif tank.statusFlag == 'New alert':
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
