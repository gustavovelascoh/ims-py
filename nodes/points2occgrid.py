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
    def __init__(self, in_ch="", out_ch="", src_name=""):
        
        self.out_ch = out_ch
        self.s= Subscriber({in_ch: self.__points_msg_cb})
        self.load_config()
        self.og = OccupancyGrid(**self.roi, cell_size=0.5, method="velca")
        
        self.og.set_origin(float(self.calib_data["sx"]),
                           float(self.calib_data["sy"]))            
        
        self.s.run()
    
    def __points_msg_cb(self,msg):
        data_str = msg["data"].decode("utf-8")
        data = json.loads(data_str)
        
        self.process_msg(data)
        
        print("type: %s, shape: %s" % (type(self.og.grid),
                                       np.shape(self.og.grid)))
        print(self.og.grid.tolist())
        out_msg = {}
        out_msg["ts"] = data["ts"]
        out_msg["curr_ts"] = time.time()
        out_msg["grid"] = self.og.grid.tolist()
        self.s.r.publish(self.out_ch, json.dumps(out_msg))

    def load_config(self):
        config = json.loads(self.s.r.hget("ims", "config").decode("utf-8"))
        self.roi = config["map"]["roi"]
        
        calib_data_var = "laser." + args.name + ".calib_data"
        calib_data_b = self.s.r.hget("ims", calib_data_var)
        
        self.calib_data = json.loads(calib_data_b.decode("utf-8"))
        
    def process_msg(self, msg):
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
    
    @staticmethod
    def _apply_roi(data, roi):
        data = data[data[:,0] >= roi["xmin"]]
        data = data[data[:,0] <= roi["xmax"]]
        
        data = data[data[:,1] >= roi["ymin"]]
        data = data[data[:,1] <= roi["ymax"]]
        return data
        
if __name__ == "__main__":
    
    import argparse
    
    description_str='Subscribe to cartesian data and generate occgrid'
    parser = argparse.ArgumentParser(description=description_str)
    parser.add_argument('name',
                        metavar='name',
                        help="Source Name")
    parser.add_argument('ich',
                        metavar='ICH',
                        help="Input channel")
    parser.add_argument('och',
                        metavar='OCH',
                        help="Output channel")
    args = parser.parse_args()
    
    p2c = Points2OccGrid(src_name=args.name, in_ch=args.ich, out_ch=args.och)
