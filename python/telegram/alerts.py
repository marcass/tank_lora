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

"""
$ python3.5 tank_alert.py <token>
prev 'Lover.py' from https://github.com/nickoala/telepot/blob/master/examples/callback/lover.py

"""

#propose_records = telepot.helper.SafeDict()  # thread-safe dict

class Tanks:
    def __init__(self, name, min_vol):
        self.name = name
        self.min_vol = min_vol 
        self.waterTop = "tank/water/" +self.name
        self.statusFlag = 'OK'
    
t = Tanks("top",   200)
n = Tanks("noels", 150)
s = Tanks("sals",  150)
x = Tanks("test",  150)

tank_dict = {}
for tank in [t,n,s,x]:
    tank_dict[waterTop] = tank

class Tank_alert(telepot.helper.ChatHandler):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[
                   InlineKeyboardButton(text='Fixed', callback_data='reset_alert'),
                   InlineKeyboardButton(text='Stop alerts for tank', callback_data='stop alerts'),
               ]])

    def __init__(self, *args, **kwargs):
        super(Tank_alert, self).__init__(*args, **kwargs)

        # Retrieve from database
        #global propose_records
        #if self.id in propose_records:
            #self._count, self._edit_msg_ident = propose_records[self.id]
            #self._editor = telepot.helper.Editor(self.bot, self._edit_msg_ident) if self._edit_msg_ident else None
        #else:
            #self._count = 0
            #self._edit_msg_ident = None
            #self._editor = None

    def _alert(self):
        self._count += 1
        sent = self.sender.sendMessage(tank.name +'is below threshold water level', reply_markup=self.keyboard)
        self._editor = telepot.helper.Editor(self.bot, sent)
        self._edit_msg_ident = telepot.message_identifier(sent)

    #def _cancel_last(self):
        #if self._editor:
            #self._editor.editMessageReplyMarkup(reply_markup=None)
            #self._editor = None
            #self._edit_msg_ident = None

    def on_callback_query(self, msg):
        query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')

        if query_data == 'reset_alert':
            #self._cancel_last()
            tank.statusFlag = 'OK'
            if t:
                t.cancel()
            self.sender.sendMessage(tank.name +' tank monitor reset')
            self.close()
        else if query_data == 'stop alerts':
            tank.statusFlag = 'STOP'
            self.sender.sendMessage(tank.name +' alerts have been stopped')
            self.close()

    #def on__idle(self, event):
        #self.sender.sendMessage('Fix the tank!')
        #self.close()


TOKEN = sys.argv[1]

bot = telepot.DelegatorBot(TOKEN, [
    include_callback_query_chat_id(
        pave_event_space())(
            per_chat_id(types=['private']), create_open, Tank_alert, timeout=10),
])
MessageLoop(bot).run_as_thread()
print('Listening ...')

#mqtt callbacks
def timeout():
    print 'Resetting alert for ' +tank.name
    tank.statusFlag = 'OK'

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe([(t.waterTop, 0), (n.waterTop, 0), (s.waterTop, 0)])

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+' '+str(msg.payload))
    top_split = msg.topic('/')
    tank = tank_dict[(top_split[-1])]
    print tank
    if msg.payload < tank.min_vol:
        print tank +' under thresh'
        if tank.statusFlag == 'OK':
            tank.statusFlag = 'New alert'
            t = Timer(4 * 60 * 60, timeout)
            t.start()
            send = Tank_alert._alert # send alert with button for canceling status
        #do nothing if not previously OK
    else if msg.payload > tank.min_vol:
        tank.statusFlag = 'OK' # might need a timer for hyusterisis in here
    else if tank.statusFlag = 'STOP':
        #no alerts requested by user for this tank so send message allowing them to be started again

if __name__ == "__main__":
    #subscribe to broker and test for messages below alert values
    client = mqtt.Client()
    client.username_pw_set(username='esp', password='heating')
    #mqtt.userdata_set(username='esp',password='heating')
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("houseslave", 1883, 60)
    client.loop_start()


    while 1:
        time.sleep(10)
