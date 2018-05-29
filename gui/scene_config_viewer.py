'''
Created on Feb 8, 2018

@author: gustavo
'''

import redis
import json
from gui.viewer import Viewer
import tkinter as tk
import numpy as np
import pickle

class SceneConfigViewer(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        
        r = redis.StrictRedis()
        
        config_b = r.hget("ims","config")
        path_b = r.hget("ims","base_path")
        
        if config_b is None:
            print("No IMS config found. exiting")
        
        #print("b ",config_b.decode("utf-8"))
        self.config = json.loads(config_b.decode("utf-8"))
        self.ims_path = path_b.decode("utf-8")
        
        #print(self.config)
        
        self.v = Viewer(self)
        self.v.pack()
        
        self.__generate_limits()
        
        self.v.draw_img(self.ims_path + "/" +self.config["map"]["image_path"], limits=self.limits)
        
        for int_bb in self.config["intersection"]:
            pts = int_bb["bbox"]
            self.v.plot_box(pts[0], pts[1], pts[2]-pts[0], pts[3]-pts[1],edgecolor="yellow")
        
        for leg_bb in self.config["legs"]:
            pts = leg_bb["bbox"]
            self.v.plot_box(pts[0], pts[1], pts[2]-pts[0], pts[3]-pts[1],edgecolor="blue")
    
        rs_src_list_str = ""
        rs_name_list_str = ""
        self.rs_config = []
        
        for rs in self.config["range_sensors"]:
            rs_src_list_str += rs["src_path"] + " "
            rs_name_list_str += rs["name"] + " "
            r.set("ims.rs."+rs["name"]+".src",rs["src_path"])
            
            f = open(rs["cfg_path"], "rb")
            self.rs_config.append(pickle.load(f))
        
        r.set("ims.rs_name_list", rs_name_list_str)
    
    def __plot_rs(self):
        
        for rs in self.rs_config:
            print("rs")
            pass    
            
    def __generate_limits(self):
        map_scale = self.config["map"]["scale"]
        max_x = self.config["map"]["max_x"]
        max_y = self.config["map"]["max_y"]
        d_x = self.config["map"]["d_x"]
        d_y = self.config["map"]["d_y"]
        
        self.limits = np.concatenate((
                             ((np.array([0,max_x])/map_scale)+d_x),
                             ((np.array([0,max_y])/map_scale)+d_y)
                             ))


if __name__ == "__main__":
    main = tk.Tk()
    main.wm_title("Scene config viewer")
    s = SceneConfigViewer(main)
    # Code to add widgets will go here...
    s.pack()#(side="top", fill="both", expand="True")
    
    tk.mainloop()
