'''
Created on Mar 29, 2018

@author: gustavo
'''
import argparse
from models.sensor import Laser
from models.subscriber import Subscriber
import time

description_str='Subscribe to raw laser and publish no background data'
parser = argparse.ArgumentParser(description=description_str)
parser.add_argument('name',
                    metavar='NAME',
                    help="Name of laser. Used for channels and variables in redis")
args = parser.parse_args()

print(args)

print(args.name)

RAW_DATA_CHANNEL = "ims/laser/"+args.name+"/raw"
NO_BG_DATA_CHANNEL = "ims/laser/"+args.name+"/no_bg"
BG_MODEL_VAR = "laser." + args.name + ".bg_model"