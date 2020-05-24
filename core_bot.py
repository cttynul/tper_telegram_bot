import urllib2
import sys
import time
import re
import random
import traceback
import telepot
import datetime
from telepot.loop import MessageLoop
from telepot.delegate import per_chat_id, create_open, pave_event_space

SATELLITE_EMOJI = u'\U0001F4E1'.encode('utf-8')
CLOCK_EMOJI = u'\U0001F550'.encode("utf-8")

class User(telepot.helper.ChatHandler):
    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)

    def on_chat_message(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)

        msg = msg["text"]
        try:
                fermata, linea = msg.split(" ")
        except:
                fermata = msg
                linea = 0
        risultato = query_hellobus(fermata, linea)
        
        print(risultato)
        self.sender.sendMessage(risultato)


    def on__idle(self, event):
        #self.sender.sendMessage('Game expired. The answer is %d' % self._answer)
        self.close()

def query_hellobus(fermata, linea=0):
    time_now = datetime.datetime.now().strftime('%H%M')
    
    if linea != 0:
        url = "https://hellobuswsweb.tper.it/web-services/hello-bus.asmx/QueryHellobus?fermata=" + fermata + "&linea=" + linea + "&oraHHMM=" #+ str(time_now)
    else:
        url = "https://hellobuswsweb.tper.it/web-services/hello-bus.asmx/QueryHellobus?fermata=" + fermata + "&linea=" + "&oraHHMM=" #+ str(time_now)

    request = urllib2.Request(url)
    response = urllib2.urlopen(request)
    root = response.read()
    result = re.findall('.asmx">([^<]*)', str(root))
    print(result)
    return_value = ""
    for res in result:
        result = res.replace(", ", "_").strip()
        result1, result2 = result.split("_")

        if "Previsto" in result1:
            return_value += CLOCK_EMOJI + " " + result1.replace("TperHellobus:" , "") + "\n"
        else:
            return_value += SATELLITE_EMOJI + " " + result1.replace("TperHellobus:" , "").replace("DaSatellite", "da satellite") + "\n"

        if "Previsto" in result2:
            return_value += CLOCK_EMOJI + " " + result2.replace("TperHellobus:" , "") + "\n"
        else:
            return_value += SATELLITE_EMOJI + " " + result2.replace("TperHellobus:" , "").replace("DaSatellite", "da satellite") + "\n"

    return str(return_value)

TOKEN = "TOKENISASTRING"
OWNER_ID = 12345678

bot = telepot.DelegatorBot(TOKEN, [
    pave_event_space()(
        per_chat_id(), create_open, User, timeout=10),
])
MessageLoop(bot).run_as_thread()
print('Listening ...')

while 1:
        time.sleep(10)
