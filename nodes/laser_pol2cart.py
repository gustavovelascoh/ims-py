'''
Created on Mar 29, 2018

@author: gustavo
'''
import argparse
from models.sensor import Laser
from models.sensor import pol2cart
from models.subscriber import Subscriber
import time
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
                    help=name_help)

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
    
        self.CALIB_DATA = dict(self.s.r.hget("ims", LASER_MODEL_VAR))
        self.d_th = self.CALIB_DATA["ang"]
        self.d_x = self.CALIB_DATA["sx"]
        self.d_y = self.CALIB_DATA["sy"]
    
    
    def polar_data_handler(self, msg):
        data = dict(msg["data"].decode("utf-8"))
        
        rho = np.array(data["data"])
        
        theta = []
        
        if "theta" in data.keys():
            theta = np.array(data["theta"])
        else:
            theta = DEFAULT_THETA
        
        phi = theta + self.d_th
        
        cart_data={}        
        cart_data["x"], cart_data["y"] = pol2cart(rho, phi)
        cart_data["x"] += self.d_x
        cart_data["y"] += self.d_y
        cart_data["ts"] = data["ts"]
        
        self.s.p.publish(CART_DATA_CHANNEL, cart_data)

l = Laser_Pol2Cart()
l.s.run()

while True:
    time.sleep(0.001)

