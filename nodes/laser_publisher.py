#!/usr/bin/python3
'''
Created on Mar 14, 2018

@author: gustavo
'''
import argparse
from models.sensor import Laser
from models.subscriber import Subscriber
import time
import json

description_str='Read dataset file and publish data to redis'
parser = argparse.ArgumentParser(description=description_str)
parser.add_argument('name',
                    metavar='NAME',
                    help="Name of laser. Used for channels and variables in redis")
parser.add_argument('dataset', help="dataset file")
args = parser.parse_args()

print(args)

print(args.name)


offset = 0

def ctrl_hdlr(msg):
    global offset
    data = json.loads(msg["data"].decode("utf-8"))
    offset = data["offset"]
#def get_offset():
#    offset_b = subs.r.hget("ims","ts.offset")
#    return float(offset_b.decode("utf-8")) if offset_b else None

ctrl_channel = "ims/run"
output_channel = "ims/laser/"+args.name+"/raw"

laser_scanner = Laser(Laser.SUBTYPE_SINGLELAYER, name=args.name)
laser_scanner.set_src_path(args.dataset)
laser_scanner.load()




subs = Subscriber({ctrl_channel: ctrl_hdlr})
subs.run()

pend = 0
pub = 0

last_scan = False

while not last_scan:
    
    #offset_b = subs.r.hget("ims","ts.offset")
    #offset = float(offset_b.decode("utf-8")) if offset_b else None
    
    if offset != 0:
        if not pend:
            last_scan = laser_scanner.read_scan()
        curr_ts = time.time()
        
        if laser_scanner.ts/1000.0 <= curr_ts-offset:
            pub +=1
            print("%s publish raw %s %s" % (pub, laser_scanner.ts/1000.0, curr_ts-offset))
            message = {"ts": offset + laser_scanner.ts/1000.0,
                       "data": laser_scanner.scan}
            subs.r.publish(output_channel, json.dumps(message))
            pend = 0
        else:
            pend = 1
            time.sleep(0.005)
            print("pend")
    else:
        time.sleep(0.005)
        pend = 0
        #print("no off")
    
    