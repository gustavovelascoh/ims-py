'''
Created on Mar 30, 2017

@author: gustavo
'''
from models.sensor import Sensor
from models.sensor import Laser
from models.blob import Blob
from models.leg import Leg
import numpy as np
from sklearn.cluster import DBSCAN
from models.occupancygrid import OccupancyGrid


class Scene():
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
        self.generate_legs(self.config_data["legs"])
            
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
    
    def add_meas_to_grid(self, range_sensor):
        d_x = float(range_sensor.calib_data["sx"])
        d_y = float(range_sensor.calib_data["sy"])
        
        x = range_sensor.x_nobg
        y = range_sensor.y_nobg
        
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
            range_sensor.remove_bg()
            range_sensor.calibrate()
            
            self.add_meas_to_grid(range_sensor)
            #print(len(range_sensor.x_nobg))
            #print(range_sensor.x_nobg)
            if x is not None:
                #print("x %s" % x)
                #print("xnbg %s" % range_sensor.x_nobg)
                x = np.concatenate((x, range_sensor.x_nobg))
                y = np.concatenate((y, range_sensor.y_nobg))
            else:
                x = range_sensor.x_nobg
                y = range_sensor.y_nobg
        
        self.occ_grid.update()
        #print(self.occ_grid.grid)
            
        #print("ts_array: %s, span: %s" % (ts_array,(max(ts_array)-min(ts_array))))
        self.ts = max(ts_array)
        x = x/100
        y = y/100
        
        data = np.array([x,y]).transpose()
        
        if self.roi:
            data = self._apply_roi(data, self.roi)
                
        return data, last, self.ts       
    
    def set_roi(self, roi):
        self.roi = roi
        self.occ_grid = OccupancyGrid(**self.roi, cell_size=0.2)
        
    @staticmethod
    def _apply_roi(data, roi):
        data = data[data[:,0] >= roi["xmin"]]
        data = data[data[:,0] <= roi["xmax"]]
        
        data = data[data[:,1] >= roi["ymin"]]
        data = data[data[:,1] <= roi["ymax"]]
        return data
    
    def get_clusters(self):
        
        self.data, self.last, self.ts = self.preprocess_data()
        
        dbscan_params = {'eps':0.3, 'min_samples':5}
        self.db = DBSCAN(**dbscan_params).fit(self.data)
        core_samples_mask = np.zeros_like(self.db.labels_, dtype=bool)
        core_samples_mask[self.db.core_sample_indices_] = True
        labels = self.db.labels_
        
        # Number of clusters in labels, ignoring noise if present.
        n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
        
        return n_clusters_
        
    def get_blobs(self):
        
        self.get_clusters()
        
        labels = self.db.labels_
        unique_labels = set(labels)
        self.blob_list = []
        
        for k in unique_labels:
            if k != -1:
                class_member_mask = (labels == k)
                
                if (sum(class_member_mask) >= self.db.min_samples):
                    blob = Blob(self.data[class_member_mask],
                                          self.ts,
                                          self.nf,
                                          self.blob_count)
                    try:
                        blob.get_features()
                        self.blob_list.append(blob)
                        self.blob_count += 1
                        
                        for leg in self.legs:
                            leg.check_item(blob)
                    except ZeroDivisionError:
                        pass
                        
        self.legs_state = []
        self.legs_areas = []
        
        # print(self.legs)
        for leg in self.legs:
            self.legs_state.append(leg.get_state())
            self.legs_areas.append(leg.bbox.area)
            leg.clear()
        
        return self.blob_list
    
    def process_blobs(self):
        
        self.curr_blobs = self.get_blobs()
        
#         if len(self.prev_blobs) > 0:
#             self.find_blobs_matches()            
#         
#         # self.update_blob_hist()
#         
#         self.update_blob_prev()
#         #print(self.prev_blobs)
        
        return self.curr_blobs

    def find_blobs_matches(self):
        
        d_mat = np.zeros((len(self.prev_blobs), len(self.curr_blobs)))
            
        for i, blob in enumerate(self.curr_blobs):
            for j, p_blob in self.prev_blobs.items():
                #print("%s, %s" % (j, p_blob))
                distance = blob.get_distance_from(p_blob)
                d_mat[int(j)][i] = distance
                
                if distance < 0.5:
                    if p_blob.id not in self.blobs_graph.keys():
                        self.blobs_graph[p_blob.id] = [blob.id]
                    #else:
                    #    matches_dict[p_blob.id].append(blob.id)
                        
                    #blob.set_connection_from(p_blob)
        
        np.set_printoptions(precision=2)
        #print(d_mat)
        #print("Graph: %s" % self.blobs_graph)
    
    def update_blob_hist(self):
        
        keys_to_remove = []
        blobs_to_hist = {}
        
        for k, v in self.prev_blobs:
            live_time = self.ts - v.ts
            if live_time > self.BLOB_TIMEOUT:
                # self.hist_blobs.append(b)
                keys_to_remove.append(k)
                blobs_to_hist[k]=v
        
        self.hist_blobs.update(blobs_to_hist)
        
        for k in keys_to_remove:
            del self.prev_blobs[k]
    
    def update_blob_prev(self):
        curr_dict = {}
        for i, v in enumerate(self.curr_blobs):
            curr_dict[v.id] = v
        
        self.prev_blobs.update(curr_dict)
            
    
# class Blob():
#     def __init__(self, data, ts, nf, blob_id):
#         self.data = data
#         self.ts = ts
#         self.nf = nf
#         self.id = blob_id
#         self.next_blobs = []
#         self.prev_blobs = []
#         self.vel = None
#         self.ang = None
#         
#     def get_features(self):
#         xy = self.data
#         bbox = np.array([min(xy[:,0:1]), min(xy[:,1:2]),max(xy[:,0:1]), max(xy[:,1:2])])
#         self.area = (bbox[2]-bbox[0])*(bbox[3]-bbox[1])
#         self.dens = len(xy)/self.area
#         self.bbox = bbox
#         self.mean = xy.mean(axis=0)
#         
#     def get_distance_from(self, blob):
#         return abs(np.linalg.norm(self.mean - blob.mean))
#     
#     def set_connection_from(self, blob):
#         self.prev_blobs = blob.prev_blobs + [blob.id]
#         blob.next_blobs.append(self.id)
#         
#         self.vel = self.get_distance_from(blob)/(self.ts - blob.ts)
#         self.ang = self._angle_between(self.mean, blob.mean)
#     
#     def add_connection_to(self, blob):
#         self.next_blobs.append(blob.id)
# 
#     @staticmethod
#     def _unit_vector(vector):
#         """ Returns the unit vector of the vector.  """
#         return vector / np.linalg.norm(vector)
# 
#      
#     def _angle_between(self, v1, v2):
#         v1_u = self._unit_vector(v1)
#         v2_u = self._unit_vector(v2)
#         return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))
    