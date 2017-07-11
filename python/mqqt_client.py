import time
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import threading

broker = 'localhost'

class tanks:
    name = ""
    topic = ""
    diam = ""
    max_dist = ""
    invalid_min = ""
    max_dist = ""
    invalid_max = (max_dist + 20)
    min_vol = ""
    def volume(self):
        #litres (measurements in cm)
        vol_calc = (diam / 2 * 3.14 * max_dist)/1000
        actual_vol = (vol_calc - (diam / 2 * 3.14 * msg.payload/1000))
        t = threading.Timer(600.0, sendAlert, [self])
        if actual_vol < min_vol:
            t.start() #don't send too many emails! consider making sure it only gets done once somehow?
        else:
            t.cancel()
        return actual_vol
    
n = tanks()
n.name = "noels"
n.topic = "tank/noels"
n.diam = "200"
n.max_dist = "100"
n.invalid_min = "30"
n.min_vol = "150"

t = tanks()
t.name = "top"
t.topic = "tank/top"
t.diam = "250"
t.max_dist = "214"
t.invalid_min = "40"
t.min_vol = "200"

s = tanks()
s.name = "sals"
s.topic = "tank/sals"
s.diam = "170"
s.max_dist = "73"
s.invalid_min = "30"
s.min_vol = "150"


top 44, 214
sal 30, 73

sal = "tank/sals"
top = "tank/top"

#tank limits
noel_low = "90"
sal_low = "65"
top_low = "190"

#sensible value range for tanks


# The callback for when the client receives a CONNACK response from the server.
# http://www.steves-internet-guide.com/subscribing-topics-mqtt-client/
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe([(noel,1),(sal, 1),(top, 1)])

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+' '+str(msg.payload))
    #allowed_passthrough_msg = ['Turn Off Boiler', 'Turn On Boiler', 'Increase SetPoint', 'Decrease SetPoint']
    if str(msg.payload) in allowed_passthrough_msg:
	port.write('\r\n'+str(msg.payload)+'\r')
        print 'Sent ' + msg.payload + ' to serial port.'

#parse mesesages from subscriptions and do somthing with them


#################### Email #####################################
# http://stackabuse.com/how-to-send-emails-with-gmail-using-python/
msg = "parsed message"

def sendAlert(msg):
    dest = "best.nose@gmail.com"
    gmail.user = "best.nose@gmail.com"
    gmail_pass = "app specific p/w"
    
    sent_from = gmail.user
    to = dest
    subject = "Farm water tank alert"

    try:
        server = smtplib.SMTP_SSL)'smtp.gmial.com', 465)
        server.ehlo()
        server.login(gmail.user, gmail_pass)
        server.sendmail(sent_from, to, msg)
        server.close()
        print 'Email sent'
    except:
        print 'Something went wrong'


auth = {'username':"esp", 'password':"heating"}

if __name__ == "__main__":
    client = mqtt.Client()
    client.username_pw_set(username='esp', password='heating')
    
    #mqtt.userdata_set(username='esp',password='heating')
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(broker, 1883, 60)

    # Blocking call that processes network traffic, dispatches callbacks and
    # handles reconnecting.
    # Other loop*() functions are available that give a threaded interface and a
    # manual interface.
    # client.loop_forever()
    client.loop_start()
    while True:
        #for debugging enable printing of serial port data
        rcv = readlineCR(port)
        #print rcv

