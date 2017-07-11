import serial
import time
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import smtplib

###########  MQTT ############################################################
broker = 'localhost'

# Harvest data from port
def readlineCR(port):
    rv = ""
    while True:
        ch = port.read()
        rv += ch
        if ch=='\r':# or ch=='':
            if 'MQTT' in rv:
                print rv
                received = rv[6:]
                received_splited = received.split('/')
                topic = '/'.join(received_splited[:-1])
                payload = received_splited[-1]
                print topic, payload
                publish.single(topic, payload, auth=auth, hostname=broker, retain=True)
            return rv


auth = {'username':"tank", 'password':"level"}
port = serial.Serial("/dev/arduino", baudrate=9600, timeout=3.0)
#port = serial.Serial("/dev/ttyUSB0", baudrate=9600, timeout=3.0)

##################  EMAIL   #####################################
gmail_user = 'best.nose@gmail.com'  
gmail_password = 'P@ssword!'

sent_from = gmail_user  
to = 'best.nose@gmail.com' 
subject = 'Farm water level alert'  
msg = 'Parse message here'

try:  
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(gmail_user, gmail_password)
    server.sendmail(sent_from, to, msg)
    server.close()
    print 'Email sent!'
except:  
   print 'Something went wrong...'


#####################  MAIN  ######################################
if __name__ == "__main__":
    client = mqtt.Client()
    client.username_pw_set(username='esp', password='heating')
    
    #mqtt.userdata_set(username='esp',password='heating')
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("houseslave", 1883, 60)

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
