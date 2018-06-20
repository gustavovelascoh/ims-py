'''
Created on Jun 16, 2018

@author: gustavo
'''
import json
import time
import numpy as np
from models.subscriber import Subscriber
from models.occupancygrid import OccupancyGrid

class Points2OccGrid():
    def __init__(self, in_ch=[], out_ch=""):
        
        self.out_ch = out_ch
        
        ch_dict = {}
        self.names_list = []
        for ch in in_ch:
            ch_dict[ch] = self.__points_msg_cb
            self.names_list.append(self.get_name(ch))
            
        print("Names List: %s" % self.names_list)
        
        self.s= Subscriber(ch_dict)
        self.load_config()
        self.og = OccupancyGrid(**self.roi, cell_size=0.5, method="velca")
        
                    
        
        self.s.run()
        self.data_buffer = {}
        self.out_msg = {'ts': 0, 'frame': 0}
    
    def __points_msg_cb(self,msg):
        data_str = msg["data"].decode("utf-8")
        data = json.loads(data_str)
        
        channel = msg["channel"].decode("utf-8")
        
        name = self.get_name(channel)
        self.data_buffer[name] = data
        
        
    
    def loop(self):
        while True:
            time.sleep(0.030)
            
            if self.data_buffer:        
                self.process_msg()
                self.publish_data()

    def load_config(self):
        config = json.loads(self.s.r.hget("ims", "config").decode("utf-8"))
        self.roi = config["map"]["roi"]
        
        self.calib_data = {}
        
        for laser_name in self.names_list:
            calib_data_var = "laser." + laser_name + ".calib_data"
            calib_data_b = self.s.r.hget("ims", calib_data_var)
            calib_data = json.loads(calib_data_b.decode("utf-8"))
            self.calib_data[laser_name] = calib_data
        
        
        
    def process_msg(self):
        
        self.data4merge = self.data_buffer
        self.data_buffer = {}
        
        self.out_msg = {'ts': [], 'frame': []}
        
        for name, msg in self.data4merge.items():
            #print(msg.keys())
            self.out_msg['ts'] += [msg['ts']]
            self.out_msg['frame'] += [msg['frame']]
            
            self.og.set_origin(float(self.calib_data[name]["sx"]),
                           float(self.calib_data[name]["sy"]))
            x = np.array(msg["x"])
            y = np.array(msg["y"])
            
            x = x/100
            y = y/100
            
            data = np.array([x,y]).transpose()
            
            if self.roi:
                data = self._apply_roi(data, self.roi)
            #print("datalen post ",(np.shape(data)))   
            x = data[:,0]
            y = data[:,1]
            
            self.og.add_meas(x,y)        
            self.og.update()
            
        if len(self.out_msg['ts']) > 1:
            self.out_msg['ts'] = min(self.out_msg['ts'])
            self.out_msg['frame'] = min(self.out_msg['frame'])
        else:
            self.out_msg['ts'] = self.out_msg['ts'][0]
            self.out_msg['frame'] = self.out_msg['frame'][0]
        
                
        #print("type: %s, shape: %s" % (type(self.og.grid),
                                       #np.shape(self.og.grid)))
        #print(self.og.grid.tolist())
    def publish_data(self):
        out_msg = {}
        out_msg["ts"] = self.out_msg['ts']
        out_msg["curr_ts"] = time.time()
        out_msg["grid"] = self.og.grid.tolist()
        self.s.r.publish(self.out_ch, json.dumps(out_msg))
    
    @staticmethod
    def _apply_roi(data, roi):
        data = data[data[:,0] >= roi["xmin"]]
        data = data[data[:,0] <= roi["xmax"]]
        
        data = data[data[:,1] >= roi["ymin"]]
        data = data[data[:,1] <= roi["ymax"]]
        return data
    @staticmethod
    def get_name(channel):
        x = channel.split('/')
        return x[2]
        
if __name__ == "__main__":
    
    import argparse
    
    description_str='Subscribe to cartesian data and generate occgrid'
    parser = argparse.ArgumentParser(description=description_str)
    parser.add_argument('-ich',
                        metavar='ICH',
                        nargs='+',
                        help="Input channel")
    parser.add_argument('-och',
                        metavar='OCH',
                        help="Output channel")
    args = parser.parse_args()
    
    p2c = Points2OccGrid(in_ch=args.ich, out_ch=args.och)
    p2c.loop()
