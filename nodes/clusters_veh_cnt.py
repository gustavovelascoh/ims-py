'''
Created on Jun 13, 2018

@author: gustavo
'''
import json
import time
from models.subscriber import Subscriber
import numpy as np



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
        
        self.check_overlap(bbox_list)
        
        #for x in self.vsens:
            #print(x)
        
        vsens_msg = {}
        vsens_msg["ts"] = data["ts"]
        vsens_msg["frame"] = data["frame"]
        vsens_msg["data"] = self.vsens
        vsens_msg["curr_ts"] = time.time()
        
        print(vsens_msg)
        self.s.r.publish("ims/legs/state", json.dumps(vsens_msg))
        
    def get_legs_config(self):
        full_cfg_str = self.s.r.hget("ims", "config").decode("utf-8")
        full_cfg = json.loads(full_cfg_str)
        
        self.legs_cfg = full_cfg["legs"]
        
        self.vsens = []
        
        for leg in self.legs_cfg:
            id_str = leg["id"]

            vsens_pts = leg["vsens"]["0"]
            vsens_dict = {id_str: vsens_pts }
            vsens_dict["pts"] = vsens_pts
            vsens_dict["area"] = self.get_area(vsens_pts)
            vsens_dict["last_occ"] = 0
            self.vsens.append(vsens_dict)
        
    def get_area(self, vsens):
        return (vsens[2] - vsens[0]) * (vsens[3] - vsens[1])    
    
    def generate_bbox(self, clusters):
        
        bbox_list = []
        
        for c in clusters:
            bbox = [min(c["x"])/100.0, min(c["y"])/100.0,
                    max(c["x"])/100.0, max(c["y"])/100.0]
            bbox = np.array(bbox)
            bbox = np.ceil(bbox*50)/50
            
            bbox_list.append(bbox.tolist())
        
        return bbox_list
    
    def check_overlap(self, bbox_list):
        
        #print(self.vsens, bbox_list)
        
        for vs in self.vsens:
            vs["occpts"] = None
            for bb in bbox_list:
                overlap = self.find_overlap(vs["pts"], bb)
                
                if overlap:
                    if vs["occpts"]:
                        vs["occpts"] = self.update_occupancy(vs["occpts"], overlap)
                    else:
                        vs["occpts"] = overlap
            
            if vs["occpts"] is None:
                vs["occ"] = vs["last_occ"]
            else:
                vs["occ"] = self.get_area(vs["occpts"])/vs["area"]
            
                print(vs["occ"])
        
        #print("**** %s" % (self.vsens))
                           
    def update_occupancy(self, curr, overlap):
        a = curr[0]
        b = curr[1]
        c = curr[2]
        d = curr[3]
        e = overlap[0]
        f = overlap[1]
        g = overlap[2]
        h = overlap[3]
        
        new_occ = [min([a,e]), min([b,f]),
                   max([c,g]), max([d,h])]
    
    def find_overlap(self,pts_a, pts_b):
        a = pts_a[0]
        b = pts_a[1]
        c = pts_a[2]
        d = pts_a[3]
        e = pts_b[0]
        f = pts_b[1]
        g = pts_b[2]
        h = pts_b[3]
        
        overlap = [max([a,e]), max([b,f]),
                   min([c,g]), min([d,h])]
        
        if overlap[0] > overlap[2] or overlap[1] > overlap[3]:
            overlap = None
            
        return overlap  

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
    