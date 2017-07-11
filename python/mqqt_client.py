import serial
import time
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

broker = 'localhost'

# The callback for when the client receives a CONNACK response from the server.
# http://www.steves-internet-guide.com/subscribing-topics-mqtt-client/
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe([("tank/noels",0),("tank/sals", 0),("tank/top", 0)])

# The callback for when a PUBLISH message is received from the server.
#def on_message(client, userdata, msg):
#    print(msg.topic+' '+str(msg.payload))
#    allowed_passthrough_msg = ['Turn Off Boiler', 'Turn On Boiler', 'Increase SetPoint', 'Decrease SetPoint']
#    if str(msg.payload) in allowed_passthrough_msg:
#	port.write('\r\n'+str(msg.payload)+'\r')
#        print 'Sent ' + msg.payload + ' to serial port.'

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

