#!/usr/bin/python3

# note that module name has changed from Tkinter in Python 2 to tkinter in Python 3
import tkinter as tk
from models import sensor
import numpy as np
import time
from sklearn.cluster import DBSCAN
from gui import viewer
from gui.frames import Legs
from gui.frames import DatasetConfig
import threading
import matplotlib
from models import scene
import json

matplotlib.use('TkAgg')

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
        
        self.dataset_path = DatasetPath(self)
        self.range_sensors = RangeSensors(self) 
              
        button_frame = tk.Frame(self)
        button = tk.Button(button_frame, text="Create Scene",
                           command=self._create_scene)
        button.pack(side="left")
        button_frame.pack(side="top")
        
        self.dsc_frame = DatasetConfig(self)
        self.dsc_frame.pack()
        self.legs_frame = Legs(self)
        self.legs_frame.pack()
                
        self.viewer = viewer.Viewer(self)
        self.viewer.pack()
        
        viewer_toolbar_frame = tk.Frame(self)
        
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
        
        colors_list = ['blue', 'red', 'green', 'purple']
        
        for b in blob_list:
            
            c_id = b.id
            
            if len(b.prev_blobs) != 0:
                c_id = min(b.prev_blobs)
                print("c_id: %d, prev: %s" % (c_id, b.prev_blobs))
                       
            self.viewer.plot(b.data[:,0], b.data[:,1], linestyle=' ',
                             marker='.', color=colors_list[(c_id-1)%4])
            self.viewer.plot([b.bbox[0],b.bbox[2]],[b.bbox[1], b.bbox[3]],linestyle='-', marker='x', color=colors_list[(c_id-1)%4])
        
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
        
#         with open(dataset_cfg_file) as data_file:    
#             self.cfg_data = json.load(data_file)
#         
#         
#         print("legs info %s" % self.cfg_data["legs"])
#         
#         self.legs_frame.add_rows(self.cfg_data["legs"])
#         
#         l=[0,0,0,0,0,0,0,0,0]
#         l[1] = self.range_sensors.l1.get()
#         l[2] = self.range_sensors.l2.get()
#         l[3] = self.range_sensors.l3.get()
#         l[5] = self.range_sensors.l5.get()
#         l[7] = self.range_sensors.l7.get()
#         l[8] = self.range_sensors.l8.get()                
#         # map_scale = 5.13449       
        
        self.scene = scene.Scene(dataset_cfg_file)
        
#         lms1 = sensor.Laser(sensor.Laser.SUBTYPE_SINGLELAYER)
#         lms2 = sensor.Laser(sensor.Laser.SUBTYPE_SINGLELAYER)
#         lms3 = sensor.Laser(sensor.Laser.SUBTYPE_SINGLELAYER)
#         lms5 = sensor.Laser(sensor.Laser.SUBTYPE_SINGLELAYER)
#         lms7 = sensor.Laser(sensor.Laser.SUBTYPE_SINGLELAYER)
#         lms8 = sensor.Laser(sensor.Laser.SUBTYPE_SINGLELAYER)
#         
#         laser_sensors = [0, lms1, lms2, lms3, 0, lms5, 0, lms7, lms8]
#         lms_files = ["", "possi.lms1","possi.lms2","possi.lms3",
#                  "", "possi.lms5", "", "possi.lms7","possi.lms8"]
#         
#         # MODIFY HERE: Select Laser scanners to use
#         print(l)
#         use_laser = [x for x in range(0,9) if l[x] == 1]
#         print(use_laser)
#         # use_laser = [1, 2, 3, 5, 7, 8]
#         # use_laser = [1, 8]        
#         #Add laser sensors to Scene
#         for laser_n in use_laser:
#             print(laser_sensors[laser_n])
#             laser_sensors[laser_n].set_src_path(self.dataset_path.dataset_path +
#                                                 '/' + lms_files[laser_n])
#             self.scene.add_sensor(laser_sensors[laser_n])
#             
#         for range_sensor in self.scene.sensors["range"]:
#             range_sensor.load()    
#         
#         #lms1.set_src_path("possi.lms3")
#         #lms1.load()
        process_log="Range sensors in the scene: %d" % len(self.scene.sensors["range"]) + "\n"
        
        print(process_log)
        
        #exit()
        
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
        
            
        # xos = [0, 23.7, 13.12, 12.68, -8.62, -2.2]
        # yos = [-21.4, 15.6, 26.7, -21.74, 17.1, 22.56]
        # angs = [0.150098, -3.344051, -4.174827, -0.059341, 3.679154, -1.933825]
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
        self.viewer.draw_img(self.dataset_path.dataset_path +
                                                '/' +'image.bmp', limits)        
        self.viewer.plot(xos,yos, marker='o', linestyle=' ', 
                         markerfacecolor='g', markeredgecolor='k',
                         markersize=10)
        self.viewer.save_background()
        
#         img=mpimg.imread(self.dataset_path.dataset_path +
#                                                 '/' +'image.bmp')
#         self.ax.clear()
#         imgplot = self.ax.imshow(img, extent=limits, aspect='auto')
#         
#         lasers_pts, = self.ax.plot(xos,yos, '.', markerfacecolor='g', markeredgecolor='k', markersize=10)
#         plt.ylim(ymin=-25,ymax=32)
#         plt.xlim(xmin=-30,xmax=40)
#         
#         nf = 1
# 
#         roi={"ymin":-24,"ymax":30,"xmin":-30,"xmax":40}
#         self.scene.set_roi(roi)
#         
#         self.canvas.show()
#         self.background = self.fig.canvas.copy_from_bbox(self.ax.bbox)
#         
#         data, last, self.ts = self.scene.preprocess_data()
#         plt.ylim(ymin=roi["ymin"],ymax=roi["ymax"])
#         plt.xlim(xmin=roi["xmin"],xmax=roi["xmax"])
#         
#         self.plot_data, = self.ax.plot(data[:,0], data[:,1], 'b. ')
#         self.canvas.show()
        
        
if __name__ == "__main__":
    main = tk.Tk()
    main.wm_title("Intersection Management System")
    # Code to add widgets will go here...
    SceneApp(main).pack(side="top", fill="both", expand="True")
    
    tk.mainloop()
    