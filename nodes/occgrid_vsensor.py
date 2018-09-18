'''
Created on Jun 19, 2018

@author: gustavo
'''
import json
import time
from models.subscriber import Subscriber
import numpy as np
import cv2


class OccGridVsensor():
    def __init__(self, in_ch="", out_ch=""):
        self.out_ch = out_ch
        
        self.s = Subscriber({in_ch: self.__occgrid_cb})
        
        self.get_config()
        self.s.run()
    
    def __occgrid_cb(self, msg):
        data_str = msg["data"].decode("utf-8")
        data = json.loads(data_str)
        
        grid = np.array((data["grid"]))
        
        for i, vs in enumerate(self.vsens):
            #print(vs)
            #if 2 in vs.keys():
            #print(i, grid[vs["idx"][1]:vs["idx"][3],
            #              vs["idx"][0]:vs["idx"][2]])
            
            vs["occ"] = np.sum(grid[vs["idx"][1]:vs["idx"][3],
                          vs["idx"][0]:vs["idx"][2]] > 0.0) / vs["area"]
            
               
        data["vsens"]=self.vsens
        
        vsens_msg = {}
        vsens_msg["ts"] = data["ts"]
        vsens_msg["data"] = self.vsens
        vsens_msg["curr_ts"] = time.time()
        self.print_occ_csv(vsens_msg) 
        self.s.r.publish("ims/occgrid/vsens/img", json.dumps(data))
        
    def get_config(self):
        full_cfg_str = self.s.r.hget("ims", "config").decode("utf-8")
        full_cfg = json.loads(full_cfg_str)
        
        self.roi = full_cfg["map"]["roi"]
        
        self.xmin = self.roi["xmin"]
        self.ymin = self.roi["ymin"]
        self.xmax = self.roi["xmax"]
        self.ymax = self.roi["ymax"]
        self.cell_size = 0.5
        
        dx = self.xmax-self.xmin
        dy = self.ymax-self.ymin
        
        self.cols = int(np.ceil(dx/self.cell_size)) + 1
        self.rows = int(np.ceil(dy/self.cell_size)) + 1
        
        self.legs_cfg = full_cfg["legs"]
        
        self.vsens = []
        
        for leg in self.legs_cfg:
            id_str = leg["id"]

            vsens_pts = leg["vsens"]["0"]
            vsens_dict = {id_str: vsens_pts }
            vsens_dict["idx"] = self.vsens_idx(vsens_pts)
            vsens_dict["area"] = self.get_area(vsens_dict["idx"])
            print("cols: {0}, row:{1}".format(self.cols, self.rows))
            print(vsens_dict)
            #vsens_dict["area"] = self.get_area(vsens_pts)
            vsens_dict["last_occ"] = 0
            self.vsens.append(vsens_dict)
    
    def vsens_idx(self, vsens_pts):
        idx = []
        a,b = self.point2index(vsens_pts[0], vsens_pts[1])        
        c,d = self.point2index(vsens_pts[2], vsens_pts[3])
        
        idx.append(a)
        idx.append(d)
        idx.append(c)
        idx.append(b)
        
        return idx
        
    
    def point2index(self, x, y):
        col = np.ceil((x - self.xmin)/self.cell_size - 0.5)
        row = self.rows - np.ceil((y - self.ymin)/self.cell_size - 0.5)
        return int(col), int(row)

    def grid2img(self, grid):
        grid_img = grid# * 255

        try:
            grid_img = np.stack((grid_img,
                                     grid_img,
                                     grid_img),axis =2)

        except Exception as e:
            print(e)

        return grid_img
    
    def get_area(self, idx):
        return (idx[2] - idx[0]) * (idx[3] - idx[1])

    def print_occ_csv(self, msg):
        
        print("%s, %s, %s, %s, %s, %s, %s" % (msg["ts"],
                                              msg["data"][0]["occ"],
                                              msg["data"][1]["occ"],
                                              msg["data"][2]["occ"],
                                              msg["data"][3]["occ"],
                                              msg["data"][4]["occ"],
                                              msg["data"][5]["occ"],
                                              ))
        
        
if __name__ == "__main__":
    
    import argparse
    
    description_str='Subscribe to occgrid to vsensor state'
    parser = argparse.ArgumentParser(description=description_str)
    parser.add_argument('ich',
                        metavar='ICH',
                        help="Input channel")
    parser.add_argument('och',
                        metavar='OCH',
                        help="Output channel")
    args = parser.parse_args()
    
    cv = OccGridVsensor(in_ch=args.ich, out_ch=args.och)