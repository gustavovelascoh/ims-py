'''
Created on Mar 29, 2018

@author: gustavo
'''
import argparse
from models.sensor import Laser
from models.sensor import pol2cart
from models.subscriber import Subscriber
import time
import json
import numpy as np

description_str='Subscribe to laser data in polar coordinates and transform \
                it into cartesian coordinates referenced to global system.\n\
                Subscribes to channel ims/laser/NAME/CHANNEL and publishes to \
                channel ims/laser/NAME/CHANNEL/cart'
parser = argparse.ArgumentParser(description=description_str)

name_help = "Name of laser. Used for channels and variables in redis"
parser.add_argument('name',
                    metavar='NAME',
                    help=name_help)

channel_help = "channel within laser namespace. e.g. raw, no_bg"
parser.add_argument('channel',
                    metavar='CHANNEL',
                    help=channel_help)

args = parser.parse_args()

print(args)

print(args.name)

LASER_CHANNEL = args.name+"/"+args.channel
POLAR_DATA_CHANNEL = "ims/laser/"+ LASER_CHANNEL
CART_DATA_CHANNEL = POLAR_DATA_CHANNEL + "/cart"
LASER_MODEL_VAR = "laser." + args.name + ".calib_data"
DEFAULT_THETA = np.arange(0, 180.5, 0.5)

class Laser_Pol2Cart():
    def __init__(self):
        self.s = Subscriber({POLAR_DATA_CHANNEL: self.polar_data_handler})
    
        self.CALIB_DATA = json.loads(self.s.r.hget("ims", LASER_MODEL_VAR).decode("utf-8"))
        self.d_th = float(self.CALIB_DATA["ang"])
        self.d_x = float(self.CALIB_DATA["sx"])
        self.d_y = float(self.CALIB_DATA["sy"])
    
    
    def polar_data_handler(self, msg):
        data_str = msg["data"].decode("utf-8")
        #print(data_str)
        data = json.loads(data_str)
        
        rho = np.array(data["data"])
        
        theta = []
        
        if "theta" in data.keys():
            theta = np.array(data["theta"])
        else:
            theta = DEFAULT_THETA
        
        theta = theta * np.pi / 180.0
        phi = theta + self.d_th
        
        cart_data={}        
        cart_data["x"], cart_data["y"] = pol2cart(rho, phi)
        
        #print("R:%s, P:%s, %s, %s" % (rho,phi, cart_data["x"], cart_data["y"]))
        cart_data["x"] = (cart_data["x"] + self.d_x*100).tolist()
        cart_data["y"] = (cart_data["y"] + self.d_y*100).tolist()
        cart_data["ts"] = data["ts"]
        
        self.s.r.publish(CART_DATA_CHANNEL, json.dumps(cart_data))

l = Laser_Pol2Cart()
l.s.run()

while True:
    time.sleep(0.001)

