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


def polar_data_handler(msg):
    data = dict(msg["data"].decode("utf-8"))
    
    rho = np.array(data["data"])
    
    if "theta" in data.keys():
        theta = np.array(data["theta"])
    else:
        theta = DEFAULT_THETA

