import telepot
import creds
from telepot.loop import MessageLoop

def handle(msg):
    print msg
    text = msg['text']
    print text

bot = telepot.Bot(creds.botAPIKey)
MessageLoop(bot, handle).run_as_thread()

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

tank_list = [t, n, s, x]
tank_status_dict = {}

for x in tank_list:
    tank_status_dict[x] = x.statusFlag
    
def status_mess():
    for tank_status in [t,n,s,x]:
        a = tank_status
        print a.name +'is ' +a.statusFlag
