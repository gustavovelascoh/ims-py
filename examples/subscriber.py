'''
Created on Mar 21, 2018

@author: gustavo
'''
import time
import json
from models.subscriber import Subscriber

CHANNEL = "test_channel"
MSG_MAX_DELAY_SECS = 0.5

def msg2json(msg):
    data_str=msg['data'].decode("utf-8")
    data = json.loads(data_str)
    return data

def is_valid(json_msg):
    msg_ts = json_msg['ts']
    curr_ts = time.time()    
    d_ts = curr_ts - msg_ts
    print("curr_ts: %s, msg_ts: %s, delta: %s" % (curr_ts, msg_ts, d_ts))
    return True if (d_ts <= MSG_MAX_DELAY_SECS) else False

def cb(msg):

    json_msg = msg2json(msg)    
    if is_valid(json_msg):    
        print("Valid msg %s, processing..." % msg['data'].decode("utf-8"))
        time.sleep(2)
    else:
        print("Old msg... skipped")


s = Subscriber({CHANNEL: cb})
s.run()

while True:
    time.sleep(0.001)
    
del s
    