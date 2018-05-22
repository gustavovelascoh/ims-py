'''
Created on May 13, 2018

@author: gustavo
'''
import tkinter as tk
from models.publisher import Publisher
from gui.control_bar import ControlBar
from gui.scene_config_viewer import SceneConfigViewer
import json
import time


class ImsMain(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.master = master
        
        self.pub = Publisher()
        self.offset = None
        
        s = SceneConfigViewer(self.master)
        s.pack()        
        control_bar = ControlBar(self.master,
                                 start_cb=self._start,
                                 stop_cb=self._stop)
        control_bar.pack()
      
    
    def _start(self):
        self.loop = True
        if self.offset is None:
            
            ts_min_b = self.pub.r.hget("ims","laser.t0_min")
            ts_min = float(ts_min_b.decode("utf-8"))
            self.offset = time.time()-ts_min
            self.pub.r.hset("ims","ts.offset", self.offset)
            self.pub.publish("ims/run", json.dumps(
                {"offset":self.offset}
                ))
    
    def _stop(self):
        self.loop = False
        
        self.offset = None
        self.pub.r.hdel("ims","ts.offset")
        self.pub.publish("ims/run", json.dumps(
            {"offset":0}
            ))
    

if __name__ == "__main__":
    main = tk.Tk()
    main.wm_title("Intersection Management System")
    
    ctrl_bar = ImsMain(main)
    ctrl_bar.pack()
    
    tk.mainloop()
    