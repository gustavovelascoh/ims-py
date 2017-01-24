#!/usr/bin/python3

# note that module name has changed from Tkinter in Python 2 to tkinter in Python 3
import tkinter as tk
import sensor
import numpy as np
import time
from sklearn.cluster import DBSCAN
from gui import viewer
import threading
import matplotlib
matplotlib.use('TkAgg')


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
        button = tk.Button(self, text="Browse", command=self.select_folder, width=10)
        button.pack(side="left")
        
        self.pack(side="top")
        
    def select_folder(self):
        ims_path="/home/gustavo/devel/python/ims"
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
        
    def _loop(self):
        self.loop = True
        t1 = threading.Thread(target=self._loop_thread)
        t1.start()
        
        
            
    def _loop_thread(self):
        while self.loop:
            last_ts = self.ts
            start_time = time.time()
            #print("clear")
            data, last, self.ts = self.scene.preprocess_data()
            
            self.date_label.config(text="%s" % self.ts)
            print("Elapsed time %s" % (time.time() - start_time))
            print("Elapsed ts %s" % (self.ts - last_ts))
            diff = self.ts - last_ts
            time.sleep(0.1*diff/1000.0)
            plot_time = time.time()
            self.viewer.update_plot_data(data[:,0], data[:,1])
            print("Plotting time %s" % (time.time() - plot_time))
    
    def _stop(self):
        self.loop = False
        
    def _next_frame(self):
        #self.ax.clear()
        #self.canvas.show()
        #print("clear")
        data, last, self.ts = self.scene.preprocess_data()
        self.date_label.config(text="%s" % self.ts)
        self.viewer.update_plot_data(data[:,0], data[:,1])
    
    def _create_scene(self):
        l=[0,0,0,0,0,0,0,0,0]
        l[1] = self.range_sensors.l1.get()
        l[2] = self.range_sensors.l2.get()
        l[3] = self.range_sensors.l3.get()
        l[5] = self.range_sensors.l5.get()
        l[7] = self.range_sensors.l7.get()
        l[8] = self.range_sensors.l8.get()                
        # map_scale = 5.13449       
        
        self.scene = sensor.Scene()
        
        lms1 = sensor.Laser(sensor.Laser.SUBTYPE_SINGLELAYER)
        lms2 = sensor.Laser(sensor.Laser.SUBTYPE_SINGLELAYER)
        lms3 = sensor.Laser(sensor.Laser.SUBTYPE_SINGLELAYER)
        lms5 = sensor.Laser(sensor.Laser.SUBTYPE_SINGLELAYER)
        lms7 = sensor.Laser(sensor.Laser.SUBTYPE_SINGLELAYER)
        lms8 = sensor.Laser(sensor.Laser.SUBTYPE_SINGLELAYER)
        
        laser_sensors = [0, lms1, lms2, lms3, 0, lms5, 0, lms7, lms8]
        lms_files = ["", "possi.lms1","possi.lms2","possi.lms3",
                 "", "possi.lms5", "", "possi.lms7","possi.lms8"]
        
        # MODIFY HERE: Select Laser scanners to use
        print(l)
        use_laser = [x for x in range(0,9) if l[x] == 1]
        print(use_laser)
        # use_laser = [1, 2, 3, 5, 7, 8]
        # use_laser = [1, 8]        
        #Add laser sensors to Scene
        for laser_n in use_laser:
            print(laser_sensors[laser_n])
            laser_sensors[laser_n].set_src_path(self.dataset_path.dataset_path +
                                                '/' + lms_files[laser_n])
            self.scene.add_sensor(laser_sensors[laser_n])
            
        for range_sensor in self.scene.sensors["range"]:
            range_sensor.load()    
        
        #lms1.set_src_path("possi.lms3")
        #lms1.load()
        process_log="Range sensors in the scene: %d" % len(self.scene.sensors["range"]) + "\n"
        
        print("Range sensors in the scene: %d" % len(self.scene.sensors["range"]))
        
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
        print(l)
        
            
        # xos = [0, 23.7, 13.12, 12.68, -8.62, -2.2]
        # yos = [-21.4, 15.6, 26.7, -21.74, 17.1, 22.56]
        # angs = [0.150098, -3.344051, -4.174827, -0.059341, 3.679154, -1.933825]
        map_scale = 4.1345
        max_x = 300
        max_y = 225
        d_x = -30.2
        d_y = -24
        
        limits = np.concatenate((
                             ((np.array([0,max_x])/map_scale)+d_x),
                             ((np.array([0,max_y])/map_scale)+d_y)
                             ))
        
        roi={"ymin":-24,"ymax":30,"xmin":-30,"xmax":40}
        self.scene.set_roi(roi)
        self.viewer.set_roi(roi)
        self.viewer.draw_img(self.dataset_path.dataset_path +
                                                '/' +'image.bmp', limits)        
        self.viewer.plot(xos,yos, '.', markerfacecolor='g', markeredgecolor='k',
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
    