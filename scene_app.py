#!/usr/bin/python3

# note that module name has changed from Tkinter in Python 2 to tkinter in Python 3
import tkinter as tk
from models import sensor
import numpy as np
import time
from sklearn.cluster import DBSCAN
from gui import viewer
from gui import frames
import threading
import matplotlib
from models import scene
import json

matplotlib.use('TkAgg')

dataset_cfg_file = "possi_123578.imscfg"
dataset_cfg_file = "possi_123.imscfg"

class RangeSensors(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.l1 = tk.IntVar()
        self.l2 = tk.IntVar()
        self.l3 = tk.IntVar()
        self.l5 = tk.IntVar()
        self.l7 = tk.IntVar()
        self.l8 = tk.IntVar()
        
        self.l = [tk.IntVar(),
                  tk.IntVar(),
                  tk.IntVar(),
                  tk.IntVar(),
                  tk.IntVar(),
                  tk.IntVar()]
        
        self.master = master
        
        l = tk.Label(self, text="Available Laser scanners")
        l.pack(side="top")
        
        c1 = tk.Checkbutton(self, text="Laser 1", variable=self.l1)
        c1.pack(side="left")
        c2 = tk.Checkbutton(self, text="Laser 2", variable=self.l2)
        c2.pack(side="left")
        c3 = tk.Checkbutton(self, text="Laser 3", variable=self.l3)
        c3.pack(side="left")
        c4 = tk.Checkbutton(self, text="Laser 5", variable=self.l5)
        c4.pack(side="left")
        c5 = tk.Checkbutton(self, text="Laser 7", variable=self.l7)
        c5.pack(side="left")
        c6 = tk.Checkbutton(self, text="Laser 8", variable=self.l8)
        c6.pack(side="left")
        
        self.pack(side="top")

class DatasetPath(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        l = tk.Label(self, text="Set Dataset Path")
        l.pack(side="left")
        self.e = tk.Entry(self)
        self.e.pack(side="left")
        button = tk.Button(self, text="Browse", command=self.select_folder, 
                           width=10)
        button.pack(side="left")
        
        self.pack(side="top")
        ims_path="/home/gustavo/devel/personal/python/ims-py/possi"
        self.dataset_path = ims_path
        
    def select_folder(self):
        ims_path="/home/gustavo/devel/python/ims/possi"
        self.dataset_path = ims_path
        self.dataset_path = tk.filedialog.askdirectory(initialdir=ims_path)
        print("FOLDER OK -> %s" % self.dataset_path)
        self.e.insert(0, self.dataset_path)
        
class SceneApp(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.master = master
                
        self.dsc_frame = frames.DatasetConfig(self, self._create_scene)
        self.dsc_frame.pack()
        
        info_frame = tk.Frame(self)
        info_frame.pack()
        
        self.legs_frame = frames.Legs(info_frame)
        self.legs_frame.pack(side="left",padx=50)
        self.rs_frame = frames.RangeSensors(info_frame)
        self.rs_frame.pack(side="left",padx=50)
        self.cam_frame = frames.Cameras(info_frame)
        self.cam_frame.pack(side="left",padx=50, expand=True)
        
        viewer_frame = tk.Frame(self)
        viewer_frame.pack(side="left")
                
        self.viewer = viewer.Viewer(viewer_frame)
        self.viewer.pack()
        
        viewer_toolbar_frame = tk.Frame(viewer_frame)
        
        self.date_label = tk.Label(viewer_toolbar_frame, text="time: NA")
        self.date_label.pack(side="left")
        nbutton = tk.Button(viewer_toolbar_frame, text="Next",
                           command=self._next_frame)
        nbutton.pack(side="left")
        lbutton = tk.Button(viewer_toolbar_frame, text="Loop",
                           command=self._loop)
        lbutton.pack(side="left")
        sbutton = tk.Button(viewer_toolbar_frame, text="Stop",
                           command=self._stop)
        sbutton.pack(side="left")
        viewer_toolbar_frame.pack(side="top")
        
        self.legs_state_frame = frames.LegsState(self)
        self.legs_state_frame.pack(side="left")
        
        self.loop = False
        self.first_frame = True
        self.last_ts = 0
        self.frame_cnt = 0
        self.processing_time_avg = 0
        self.plotting_time_avg = 0
        self.total_time_avg = 0
        self.elapsed_time = 0
        
    def _loop(self):
        self.loop = True
        t1 = threading.Thread(target=self._loop_thread)
        t1.start()
        
        
            
    def _loop_thread(self):
        while self.loop:
            if not self.first_frame:
                if self.last_ts == 0:
                    self.last_ts = self.ts              
                diff = self.ts - self.last_ts
                self.last_ts = self.ts
                time.sleep((diff/1000.0)-self.elapsed_time)
#                 print("Elapsed ts %s" % (self.ts - self.last_ts))
            else:
                self.first_frame = False                
            self._next_frame()
    
    def _stop(self):
        self.loop = False
        
    def _next_frame(self):
        
        '''
        start_time = time.time()
        data, last, self.ts = self.scene.preprocess_data()
        p_proc_time = time.time() - start_time
        self.frame_cnt += 1
        self.processing_time_avg = ((self.processing_time_avg * (self.frame_cnt-1) + p_proc_time)/self.frame_cnt) 
        proc_fps = (1/self.processing_time_avg)
        print("Processing: %s, Avg: %s, FPS: %4.4f" % (p_proc_time,
                                                        self.processing_time_avg,
                                                        proc_fps))
                    
        plot_time = time.time()
        self.viewer.plot(data[:,0], data[:,1], linestyle=' ', marker='.', color='blue')
        self.viewer.update()
        p_plot_time = time.time() - plot_time
        
        self.plotting_time_avg = ((self.plotting_time_avg * (self.frame_cnt-1) + p_plot_time)/self.frame_cnt) 
        plot_fps = (1/self.plotting_time_avg)
        total_time = self.plotting_time_avg+self.processing_time_avg
        self.total_time_avg = ((self.total_time_avg * (self.frame_cnt-1) + p_plot_time)/self.frame_cnt)
        total_fps = 1/self.total_time_avg
        print("Plotting: %s, Avg: %s, FPS: %4.4f" % (p_plot_time,
                                                         self.plotting_time_avg,
                                                         plot_fps ))
        print("Total: %s, Avg: %s, FPS: %4.4f" % (p_plot_time+p_proc_time,
                                                      total_time,
                                                      total_fps))
        '''
        
        start_time = time.time()
        # blob_list = self.scene.get_blobs()
        blob_list = self.scene.process_blobs()
        
        status = []
        occupancy_levels = [("empty", 0.2),
             ("low", 2.0),
             ("medium", 5.0),
             ("high", 13.0),
             ("very high", 100.0)]
        
        for idx, status in enumerate(self.scene.legs_state):
            lvl_val = round(status*100, 2)
            lvl_str = str(lvl_val)
            
            for k, v in occupancy_levels:
                if lvl_val < v:
                    lvl_str = k + " (" + lvl_str + ")"
                    break
            
            self.legs_state_frame.status_labels[idx].config(text=lvl_str)
            
            
        
        #print(status)        
        
        self.ts = self.scene.ts
        p_proc_time = time.time() - start_time
        self.frame_cnt += 1
        self.processing_time_avg = (
            (self.processing_time_avg * (self.frame_cnt-1) + p_proc_time) /
            self.frame_cnt) 
        proc_fps = (1/self.processing_time_avg)
#         print("Processing: %s, Avg: %s, FPS: %4.4f" % (p_proc_time,
#                                                         self.processing_time_avg,
#                                                         proc_fps))
                    
        plot_time = time.time()
        
        colors_list = ['blue']
        # colors_list = ['blue', 'red', 'green', 'purple']
        
        len_colors_list = len(colors_list)
        
        for b in blob_list:
            
            c_id = b.id
            b_color=colors_list[(c_id-1)%len_colors_list]
            
            if len(b.prev_blobs) != 0:
                c_id = min(b.prev_blobs)
                print("c_id: %d, prev: %s" % (c_id, b.prev_blobs))
                       
#             self.viewer.plot(b.data[:,0], b.data[:,1], linestyle=' ',
#                              marker='.', color=colors_list[(c_id-1)%len_colors_list])
            minx, miny = b.bbox.minxy
            self.viewer.plot_box(minx, miny, b.bbox.width, b.bbox.height, edgecolor=b_color)
            
            self.viewer.plot([b.bbox.minxy[0],b.bbox.maxxy[0]],[b.bbox.minxy[1], b.bbox.maxxy[1]],linestyle='-', marker='x', color=b_color)
        
        self.viewer.update()  
        p_plot_time = time.time() - plot_time
        
        self.plotting_time_avg = (
            (self.plotting_time_avg * (self.frame_cnt-1) + p_plot_time) /
            self.frame_cnt) 
        plot_fps = (1/self.plotting_time_avg)
        total_time = self.plotting_time_avg+self.processing_time_avg
        self.total_time_avg = (
            (self.total_time_avg * (self.frame_cnt-1) + p_plot_time)/
            self.frame_cnt)
        total_fps = 1/self.total_time_avg
#         print("Plotting: %s, Avg: %s, FPS: %4.4f" % (p_plot_time,
#                                                          self.plotting_time_avg,
#                                                          plot_fps ))
#         print("Total: %s, Avg: %s, FPS: %4.4f" % (p_plot_time+p_proc_time,
#                                                       total_time,
#                                                       total_fps))
        
        label_str = "Frame # %d \n" % (self.scene.nf)
        label_str += "avg(proc/plot/total): %4.2f/%4.2f/%4.2f" % (
            self.processing_time_avg,
            self.plotting_time_avg,
            self.total_time_avg)
        label_str += "\n FPS(proc/plot/total): %4.2f/%4.2f/%4.2f" % (proc_fps,
                                                     plot_fps,
                                                     total_fps)
        self.date_label.config(text=label_str)
    
    def _create_scene(self):
        self.scene = scene.Scene(dataset_cfg_file)
        
        self.legs_frame.add_rows(self.scene.config_data["legs"])
        self.legs_state_frame.add_rows(self.scene.config_data["legs"])
        self.rs_frame.add_rows(self.scene.config_data["range_sensors"])
        self.cam_frame.add_rows(self.scene.config_data["cameras"])

        process_log="Range sensors in the scene: %d" % len(self.scene.sensors["range"]) + "\n"
        
        print(process_log)
                
        theta = np.arange(0, 180.5, 0.5)
        theta = theta * np.pi / 180.0
        
        last = 0
        
        xos = []
        yos = []
        angs = []
        
        # Extract origins
        for range_sensor in self.scene.sensors["range"]:
            xos.append(float(range_sensor.dataset["calib_data"]["sx"]))
            yos.append(float(range_sensor.dataset["calib_data"]["sy"]))
            angs.append(float(range_sensor.dataset["calib_data"]["ang"]))
        #print(l)
        
        map_scale = self.scene.config_data["map"]["scale"]
        max_x = self.scene.config_data["map"]["max_x"]
        max_y = self.scene.config_data["map"]["max_y"]
        d_x = self.scene.config_data["map"]["d_x"]
        d_y = self.scene.config_data["map"]["d_y"]
        
        limits = np.concatenate((
                             ((np.array([0,max_x])/map_scale)+d_x),
                             ((np.array([0,max_y])/map_scale)+d_y)
                             ))
        
        roi = self.scene.config_data["map"]["roi"]
        self.scene.set_roi(roi)
        self.viewer.set_roi(roi)
        self.viewer.draw_img(self.scene.config_data["map"]["image_path"], limits)        
        self.viewer.plot(xos,yos, marker='o', linestyle=' ', 
                         markerfacecolor='g', markeredgecolor='k',
                         markersize=10)
        
        for leg in self.scene.config_data["legs"]:
    
            minx = leg['bbox'][0]
            miny = leg['bbox'][1]
            dx = leg['bbox'][2] - minx
            dy = leg['bbox'][3] - miny
            color = "purple" if leg["type"] == "departure" else "cyan"
            
            self.viewer.plot_box(minx, miny, dx, dy, edgecolor=color)
        
        self.viewer.save_background()
                
        
if __name__ == "__main__":
    main = tk.Tk()
    main.wm_title("Intersection Management System")
    # Code to add widgets will go here...
    SceneApp(main).pack(side="top", fill="both", expand="True")
    
    tk.mainloop()
    