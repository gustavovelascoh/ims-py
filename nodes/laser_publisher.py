'''
Created on Mar 14, 2018

@author: gustavo
'''
import argparse
from models.sensor import Laser
from models.subscriber import Subscriber

description_str='Read dataset file and publish data to redis'
parser = argparse.ArgumentParser(description=description_str)
parser.add_argument('name',
                    metavar='NAME',
                    help="Name of laser. Used for channels and variables in redis")
parser.add_argument('dataset', help="dataset file")
args = parser.parse_args()

print(args)

print(args.name)

def ctrl_hdlr(msg):
    print(msg)

ctrl_channel = "ims/run"
output_channel = "ims/laser/"+args.name+"/raw"

laser_scanner = Laser(Laser.SUBTYPE_SINGLELAYER)
laser_scanner.set_src_path(args.dataset)
laser_scanner.load()




subs = Subscriber({ctrl_channel: ctrl_hdlr})
subs.run()

while True:
    pass