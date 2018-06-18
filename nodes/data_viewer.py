'''
Created on Jun 9, 2018

@author: gustavo
'''
from models.subscriber import Subscriber
from gui.viewer import Viewer
import json
import numpy as np
import tkinter as tk
from matplotlib.pyplot import grid


class DataViewer(tk.Frame):
    def __init__(self, master, channel="", datatype="points"):
        
        subs_dict = {}
        
        if datatype == "points":
            subs_dict = {channel: self.__points_cb}
        elif datatype == "grid":
            subs_dict = {channel: self.__array_cb}    
        
        self.s = Subscriber(subs_dict)
        
        
        tk.Frame.__init__(self, master)
        self.master = master
        self.v = Viewer(self.master)
        self.v.pack()
        
        self.get_config()
        
        if datatype == "points":
            self.v.set_roi(self.roi)
            self.v.draw_img(self.img_path, self.limits)
            self.v.save_background()
        elif datatype == "grid":
            pass
        
        self.s.run()
        
    def get_config(self):
        config_b = self.s.r.hget("ims","config")
        self.config = json.loads(config_b.decode("utf-8"))
        
        self.roi = self.config["map"]["roi"]
        
        map_scale = self.config["map"]["scale"]
        max_x = self.config["map"]["max_x"]
        max_y = self.config["map"]["max_y"]
        d_x = self.config["map"]["d_x"]
        d_y = self.config["map"]["d_y"]
        
        self.limits = np.concatenate((
                             ((np.array([0,max_x])/map_scale)+d_x),
                             ((np.array([0,max_y])/map_scale)+d_y)
                             ))
        
        self.img_path = self.config["map"]["image_path"]
    
    def __points_cb(self, msg):
        data_s = msg["data"].decode("utf-8")
        
        data = json.loads(data_s)
        
        x = np.array(data["x"])/100
        y = np.array(data["y"])/100
        
        self.v.plot(x,y,linestyle=' ', marker='.')
        self.v.update()
    
    def __array_cb(self, msg):
        data_s = msg["data"].decode("utf-8")
        data = json.loads(data_s)
        #print(data)
        grid = np.array(data["grid"])
        self.v.draw_array(grid, self.limits)

if __name__ == "__main__":
    import argparse
    
    
    description_str='Subscribe to a channel for incoming data to plot'
    parser = argparse.ArgumentParser(description=description_str)
    parser.add_argument('channel',
                        metavar='channel',
                        help="Channel to subscribe for data")
    parser.add_argument('datatype', help="type of data (points, array)")
    args = parser.parse_args()
    
    main = tk.Tk()
    main.wm_title(args.channel)
    
    dv = DataViewer(main, args.channel, args.datatype)
    tk.mainloop()
    
    