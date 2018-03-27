#!/usr/bin/python3

import tkinter as tk
import numpy as np
from gui import frames
from gui import viewer
from models import scene_occ
import threading
import pickle
from models.publisher import Publisher
import json
import redis
import time

class ImsApp(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.master = master
                
        self.dsc_frame = frames.DatasetConfig(self,
                                              self._load_dataset,
                                             "/home/gustavo")
        self.dsc_frame.pack()
        info_frame = tk.Frame(self)
        info_frame.pack()
        
        grid_frame = tk.Frame(self)
        grid_frame.pack(side="left")
        
        viewer_frame = tk.Frame(self)
        viewer_frame.pack(side="left")
                
        self.grid = viewer.Viewer(viewer_frame, figsize=(30/4,22.5/4))
        self.grid.pack()
        
        viewer_toolbar_frame = tk.Frame(viewer_frame)
        nbutton = tk.Button(viewer_toolbar_frame, text="Next",
                           command=self._next)
        nbutton.pack(side="left")
        lbutton = tk.Button(viewer_toolbar_frame, text="Loop",
                           command=self._loop)
        lbutton.pack(side="left")
        sbutton = tk.Button(viewer_toolbar_frame, text="Stop",
                           command=self._stop)
        sbutton.pack(side="left")
        viewer_toolbar_frame.pack(side="top")
        
        self.loop = False
        self.first_frame = True
        self.last_ts = 0
        self.frame_cnt = 0
        
        self.pub = Publisher()
        self.offset = None
        
    def _load_dataset(self):
        if self.dsc_frame.filename:
            self.scene = scene_occ.SceneOcc(self.dsc_frame.filename)
        else:
            print("NO FILE SELECTED")
            return
        
        map_scale = self.scene.config_data["map"]["scale"]
        max_x = self.scene.config_data["map"]["max_x"]
        max_y = self.scene.config_data["map"]["max_y"]
        d_x = self.scene.config_data["map"]["d_x"]
        d_y = self.scene.config_data["map"]["d_y"]
        
        self.limits = np.concatenate((
                             ((np.array([0,max_x])/map_scale)+d_x),
                             ((np.array([0,max_y])/map_scale)+d_y)
                             ))
        
        roi = self.scene.config_data["map"]["roi"]
        self.scene.set_roi(roi)
        
        self.ts = 0
        
        self.save_file = self.dsc_frame.rec_check
        print("save to file? %s" % self.save_file)
        
        self.plot = self.dsc_frame.plot_check
        print("plot? %s" % self.plot)
        
        if self.save_file:
            self.data_array = []
        
    
    def _next(self):
        last = self.scene.process_frame()
        
        self.frame_cnt += 1
        
        if self.plot:
            if np.mod(self.frame_cnt,10) == 0:
                xa = self.scene.occ_grid_th3
                self.grid.draw_array(xa, limits=self.limits)
        
        self.ts = self.scene.ts
        
        data = {"ts": self.ts, "legs_state": self.scene.legs_state}
        self.pub.publish("ims/legs/state_og", json.dumps(data))
        
        
        if self.save_file:
            #data = {"ts": self.ts, "legs_state": np.array(self.scene.legs_state)}
            #print(self.frame_cnt, data)
            self.data_array.append(data)
            #print(self.data_array)
            
        if last:
            self.loop = False
            
            if self.save_file:
                with open(self.dsc_frame.filename+".data","wb") as gf:
                    pickle.dump(self.data_array,gf)
            print("End of data")
        
    
    def _loop(self):
        self.loop = True
        if self.offset is None:
            
            ts_min_b = self.pub.r.hget("ims","laser.t0_min")
            ts_min = float(ts_min_b.decode("utf-8"))
            
            self.pub.r.hset("ims","ts.offset", time.time()-ts_min)
            self.offset = self.pub.r.hget("ims","ts.offset")
        
        t1 = threading.Thread(target=self._loop_thread)
        t1.start()
    
    def _stop(self):
        self.loop = False
        
        self.offset = None
        self.pub.r.hdel("ims","ts.offset")
    
    def _loop_thread(self):
        while self.loop:
            if not self.first_frame:
                if self.last_ts == 0:
                    self.last_ts = self.ts              
                diff = self.ts - self.last_ts
                self.last_ts = self.ts
                #time.sleep((diff/1000.0)-self.elapsed_time)
#                 print("Elapsed ts %s" % (self.ts - self.last_ts))
            else:
                self.first_frame = False
                
                
                                
            self._next()
        
if __name__ == "__main__":
    
    r = redis.StrictRedis()
    
    config_file = r.hget("ims", "config_file")
    
    if config_file is None:
        print("No IMS config file found. Select one in the GUI")
    else:
        config_file = config_file.decode("utf-8")
    
    main = tk.Tk()
    main.wm_title("Intersection Management System")
    # Code to add widgets will go here...
    ims = ImsApp(main)
    ims.pack(side="top", fill="both", expand="True")
    
    if config_file:
        ims.dsc_frame.filename = config_file
        ims._load_dataset()
        
        plot = r.hget("ims_app","plot")
        ims.plot = int(plot.decode("utf-8"))
    
    
    tk.mainloop()