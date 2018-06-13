'''
Created on Jun 13, 2018

@author: gustavo
'''
import json
from models.subscriber import Subscriber
from scipy import cluster


class ClustersVehCnt():
    def __init__(self, in_ch="", out_ch=""):
        self.out_ch = out_ch
        
        self.s = Subscriber({in_ch: self.__clusters_cb})
        
        self.get_legs_config()
        self.s.run()
    
    def __clusters_cb(self, msg):
        data_str = msg["data"].decode("utf-8")
        data = json.loads(data_str)
                
        bbox_list = self.generate_bbox(data["data"])
        
    def get_legs_config(self):
        full_cfg_str = self.s.r.hget("ims", "config").decode("utf-8")
        full_cfg = json.loads(full_cfg_str)
        
        self.legs_cfg = full_cfg["legs"]
        
        self.vsens = []
        
        for leg in self.legs_cfg:
            id_str = leg["id"]

            vsens_pts = leg["vsens"]["0"]
            vsens_dict = {id_str: vsens_pts }
            vsens_dict["area"] = self.get_vsense_area(vsens_pts)
            self.vsens.append(vsens_dict)
        
    def get_vsense_area(self, vsens):
        return (vsens[2] - vsens[0]) * (vsens[3] - vsens[1])    
    
    def generate_bbox(self, clusters):
        
        bbox_list = []
        
        for c in clusters:
            bbox = [min(c["x"]), min(c["y"]),
                    max(c["x"]), max(c["y"])]
            bbox_list.append(bbox)
        
        return bbox_list
    
    def check_overlap(self, bbox_list):
        
        for bb in bbox_list:
            for vs in self.vsens:
                pass
                
    def update_occupancy(self):
        pass            

if __name__ == "__main__":
    
    import argparse
    
    description_str='Subscribe to clusters data to count vehicles'
    parser = argparse.ArgumentParser(description=description_str)
    parser.add_argument('ich',
                        metavar='ICH',
                        help="Input channel")
    parser.add_argument('och',
                        metavar='OCH',
                        help="Output channel")
    args = parser.parse_args()
    
    cvc = ClustersVehCnt(in_ch=args.ich, out_ch=args.och)
    