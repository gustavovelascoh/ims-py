#!/usr/bin/python3

import tkinter as tk
from gui import frames
from gui import viewer
from models import scene_occ
import threading


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
                
        self.grid = viewer.Viewer(viewer_frame, figsize=(30/6,22.5/6))
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
        
    def _load_dataset(self):
        if self.dsc_frame.filename:
            self.scene = scene_occ.SceneOcc(self.dsc_frame.filename)
        else:
            print("NO FILE SELECTED")
            return
        pass
    
    def _next(self):
        pass
    
    def _loop(self):
        self.loop = True
        t1 = threading.Thread(target=self._loop_thread)
        t1.start()
    
    def _stop(self):
        pass
    
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
            self._next_frame()
        
if __name__ == "__main__":
    main = tk.Tk()
    main.wm_title("Intersection Management System")
    # Code to add widgets will go here...
    ImsApp(main).pack(side="top", fill="both", expand="True")
    
    tk.mainloop()