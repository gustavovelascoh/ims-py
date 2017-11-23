'''
Created on Mar 30, 2017

@author: gustavo
'''
import pyximport; pyximport.install()
import numpy as np
from models.sensor import Sensor
from models.sensor import Laser
#from models.blob_cy import Blob
from models.leg_cy import Leg

from sklearn.cluster import DBSCAN
from models.occupancygrid_cy import OccupancyGrid
from models import sensor


class SceneOcc():
    sensors = {Sensor.TYPE_IMAGE: [],
               Sensor.TYPE_RANGE: [],
               }
    roi = {}
    nf = 0
    ts = 0
    BLOB_TIMEOUT = 5000
    
    def __init__(self, config_file=None):
        
        if config_file is not None:
            import json

            with open(config_file) as file:
                self.config_data = json.load(file)
        else:
            raise Exception("No config file provided")
        self.legs = []
        
        self.import_range_sensors(self.config_data["range_sensors"])
        #self.generate_legs(self.config_data["legs"])
            
        self.blob_count = 0
        self.curr_blobs = []
        self.prev_blobs = {}
        self.hist_blobs = {}
        self.blobs_graph = {}
        
        self.legs_state = []
        
        #
    
    
    def generate_legs(self, legs_array):
        for leg_dict in legs_array:
            leg = Leg(id=leg_dict["id"],
                      type=leg_dict["type"],
                      heading=leg_dict["heading"],
                      bbox=leg_dict["bbox"],
                      lanes=leg_dict["lanes"])
            self.legs.append(leg)
        
    def import_range_sensors(self, sensor_list):
        for rs in sensor_list:
            if rs["subtype"] == "singlelayer":
                lms = Laser(Laser.SUBTYPE_SINGLELAYER)
                lms.set_src_path(rs["src_path"])
                self.add_sensor(lms)
                lms.load()
            else:
                raise NotImplementedError("type unsupported: %s" % rs["type"])
        print("Range sensors in the scene: %d" % len(self.sensors["range"]) + "\n")
        
    def add_sensor(self, sensor):
        self.sensors[sensor.type].append(sensor)
        
    def read_data(self):
        pass
    
    def add_meas_to_grid(self, range_sensor, method="raw"):
        if method == "no_bg":
            x = range_sensor.x_nobg
            y = range_sensor.y_nobg
            
        if method == "raw":
            x, y = sensor.pol2cart(range_sensor.scan,
                                   range_sensor.raw_theta)
        
        
        d_x = float(range_sensor.calib_data["sx"])
        d_y = float(range_sensor.calib_data["sy"])
        
        x = x/100
        y = y/100
        
        data = np.array([x,y]).transpose()
        
        #print("datalen pre ",(np.shape(data)))
        if self.roi:
            data = self._apply_roi(data, self.roi)
        #print("datalen post ",(np.shape(data)))   
        x = data[:,0]
        y = data[:,1]
        
        self.occ_grid.set_origin(d_x, d_y)
        self.occ_grid.add_meas(x, y)
    
    def preprocess_data(self):
        '''
        Preprocessing (Background removal, calibration, conversion 
        to cartesian coordinates and low-level fusion of multiple 
        range sensors. Also a roi is applied if it was configured)
        @type (np.array, Bool)
        @return (data, last, ts): xy np.array of points in scene_app (N x 2),
        True if is the last frame in sensor dataset, timestamp of the current frame 
        '''
        
        x = None
        y = None
        self.nf += 1
        ts_array = []
        
        for range_sensor in self.sensors["range"]:
            last = range_sensor.read_scan()
            ts_array.append(range_sensor.ts)
            #range_sensor.remove_bg()
            range_sensor.calibrate()
            
            self.add_meas_to_grid(range_sensor, "no_bg")
            #print(len(range_sensor.x_nobg))
            #print(range_sensor.x_nobg)
#             if x is not None:
#                 #print("x %s" % x)
#                 #print("xnbg %s" % range_sensor.x_nobg)
#                 x = np.concatenate((x, range_sensor.x_nobg))
#                 y = np.concatenate((y, range_sensor.y_nobg))
#             else:
#                 x = range_sensor.x_nobg
#                 y = range_sensor.y_nobg
        
        self.occ_grid.update()
        #print(self.occ_grid.grid)
            
        #print("ts_array: %s, span: %s" % (ts_array,(max(ts_array)-min(ts_array))))
        self.ts = max(ts_array)
        
        return last
#         x = x/100
#         y = y/100
#         
#         data = np.array([x,y]).transpose()
#         
#         if self.roi:
#             data = self._apply_roi(data, self.roi)
#                 
#         return data, last, self.ts
       
    
    def set_roi(self, roi):
        self.roi = roi
        self.occ_grid = OccupancyGrid(**self.roi, cell_size=0.3,method="velca")
        
    @staticmethod
    def _apply_roi(data, roi):
        data = data[data[:,0] >= roi["xmin"]]
        data = data[data[:,0] <= roi["xmax"]]
        
        data = data[data[:,1] >= roi["ymin"]]
        data = data[data[:,1] <= roi["ymax"]]
        return data
    
    def process_legs(self):
        
        self.legs_state = []
        self.legs_areas = []
        
        for leg_dict in self.config_data["legs"]:
            
            min_ind_r, min_ind_c = self.occ_grid.point2index(
                leg_dict["bbox"][0],
                leg_dict["bbox"][1]
                )
            max_ind_r, max_ind_c = self.occ_grid.point2index(
                leg_dict["bbox"][2],
                leg_dict["bbox"][3]
                )
            
            if (min_ind_r <= max_ind_r):
                ra = min_ind_r
                rb = max_ind_r
            else:
                rb = min_ind_r
                ra = max_ind_r
                
            if (min_ind_c <= max_ind_c):
                ca = min_ind_c
                cb = max_ind_c
            else:
                cb = min_ind_c
                ca = max_ind_c
            
            leg_grid = self.occ_grid_th[ra:rb,
                                        ca:cb]
            
            self.legs_state.append(np.sum(leg_grid))
            
    
    def process_frame(self):
        last = self.preprocess_data()
        self.occ_grid_th = self.occ_grid.get_grid(0.6)
        self.process_legs()
        print("legs_state: %s" % self.legs_state)
        return last
        
    