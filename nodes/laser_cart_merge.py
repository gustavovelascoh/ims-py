'''
Created on May 7, 2018

@author: gustavo
'''
import argparse

description_str='Subscribe to diferent laser channels with cartesian data, \
                merge it and publishes it into a new channel'
parser = argparse.ArgumentParser(description=description_str)

chs_help = "List of channels with cartesian data"
parser.add_argument('--input-channels','-ichs',
                    nargs='+',
                    metavar='ICH',
                    help=chs_help)

och_help = "Channel with merged data"
parser.add_argument('--output-channel','-och',
                    metavar='OCH',
                    help=och_help)

ts_help = "timeslot in milliseconds"
parser.add_argument('--timeslot','-ts',
                    metavar='TS',
                    help=ts_help)

args = parser.parse_args()


from models.subscriber import Subscriber
import time
import json

class LaserCartMerge():
    def __init__(self, channels_list, output_channel, ts=30):
        
        self.ts = ts
        self.ts_secs = self.ts / 1000.0
        self.output_channel = output_channel
        ch_dict = {}
        for ch in channels_list:
            ch_dict[ch] = self.data_handler
            
        self.s = Subscriber(ch_dict)
        self.data_buffer = {}
        self.data4merging = {}
        self.busy = False
        self.merged_data = {}
    
    def data_handler(self, msg):
        while self.busy:
            time.sleep(0.005)
                    
        channel = msg["channel"].decode("utf-8")
        data_str = msg["data"].decode("utf-8")
        # TODO: store data in buffer
        self.data_buffer[channel] = json.loads(data_str)
    
    def run_subscriber(self):
        self.s.run()
        
    def loop(self):
        while True:
            time.sleep(self.ts_secs)
            
            if self.data_buffer:        
                self.merge_data()
                self.publish_data()
        
    
    def merge_data(self):
        
        self.busy = True        
        self.data4merging = self.data_buffer
        self.busy = False
        
        print("d4m %s" % self.data4merging.keys())
        
        self.merged_data = {'x': [], 'y': [], 'ts': []}
        for data in self.data4merging.values():
            #print(data)
            self.merged_data['x'] += data['x']
            self.merged_data['y'] += data['y']
            self.merged_data['ts'] += [data['ts']]
        
        print("md ts %s" % self.merged_data['ts'])
        
        if len(self.merged_data['ts']) > 1:
            self.merged_data['ts'] = min(self.merged_data['ts'])
        
        print("md lens x:%s" % (len(self.merged_data['x'])))
        
    def publish_data(self):
        self.s.r.publish(self.output_channel, json.dumps(self.merged_data))
        
lcm = LaserCartMerge(args.input_channels, args.output_channel)
lcm.run_subscriber()
lcm.loop()
