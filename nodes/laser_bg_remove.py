'''
Created on Mar 29, 2018

@author: gustavo
'''

from models.subscriber import Subscriber
import numpy as np
import json
import time

DEFAULT_THETA = np.arange(0, 180.5, 0.5)

class LaserBgRemove():
    def __init__(self, in_ch="", out_ch="", bg_model_var=""):
        self.s = Subscriber({in_ch: self.__raw_data_cb})
        self.bg_model_var = bg_model_var
        self.out_ch = out_ch
        
        self.get_bg_model()
        
        self.s.run()
        
        
    def __raw_data_cb(self, msg):        
        data_str = msg["data"].decode("utf-8")
        data_dict = json.loads(data_str)
        data = data_dict["data"]
        msg_nobg = self.remove_bg(data)
        msg_nobg["ts"] = data_dict["ts"]
        msg_nobg["frame"] = data_dict["frame"]
        msg_nobg["curr_ts"] = time.time()
        self.s.r.publish(self.out_ch, json.dumps(msg_nobg))
    
    def get_bg_model(self):
        bg_b = self.s.r.hget("ims", self.bg_model_var)
        self.bg_model = json.loads(bg_b.decode("utf-8"))
        self.bg_data = self.bg_model["bg_model"]
    
    def remove_bg(self, data):
        data_arr = np.array(data)
        bg_delta = np.abs(np.array(self.bg_data) - data_arr)
        
        data_nobg = data_arr[bg_delta > 15]
        theta_nobg = DEFAULT_THETA[bg_delta > 15]
        
        msg_nobg = {"data": data_nobg.tolist(),
                    "theta": theta_nobg.tolist()}
        return msg_nobg
    
if __name__ == "__main__":
    
    import argparse
    
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
    
    bgrem = LaserBgRemove(RAW_DATA_CHANNEL,
                          NO_BG_DATA_CHANNEL,
                          BG_MODEL_VAR)
    
    
    