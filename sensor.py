import pickle
import numpy as np
from sklearn.cluster import DBSCAN


def pdk(a,level=0):
    t=''.join(['.' for x in range(0,level)])
    if isinstance(a,dict):
        for k in a.keys():
            print("%s %s:"%(t,k))
            pdk(a[k],level+1)

def pol2cart(rho, phi):
    x = rho * np.cos(phi)
    y = rho * np.sin(phi)
    return(x, y)


class Sensor():
    TYPE_IMAGE = "image"
    TYPE_RANGE = "range"
    
    SRC_TYPE_DATASET = "Dataset"
    SRC_TYPE_STREAM = "Stream"
    
    src_type = ''
    src_subtype = ''
    src_path = ''
    
    def __init__(self,sensor_type):
        self.type = sensor_type

    def set_src_type(self, src_type):
        self.src_type = src_type
        
    def set_src_path(self, src_path):
        self.src_path = src_path
    
    def load_src(self):
        f = open(self.src_path, "rb")         

class Camera(Sensor):
    SUBTYPE_BW = "Black/White"
    SUBTYPE_RGB = "RGB"
   
    def __init__(self, camera_type):
        self.subtype = camera_type
        super().__init__(Sensor.TYPE_IMAGE)


class Laser(Sensor):
    SUBTYPE_SINGLELAYER = "Single layer"
    SUBTYPE_MULTILAYER = "Multilayer"
    scan = None
    ts = None
    
    def __init__(self, laser_type):
        self.subtype = laser_type
        super().__init__(Sensor.TYPE_RANGE)
    
    def load(self):
        f = open(self.src_path,"rb")
        self.dataset = pickle.load(f)
        
#         pdk(self.dataset)
#         ang_range:
#         bg_model:
#         . ms:
#         . data:
#         range_unit:
#         scans:
#         ang_res:
#         calib_data:
#         . sy:
#         . ang:
#         . sx:
        
        self.raw_theta = np.arange(0, 180.5, 0.5)
        self.raw_theta = self.raw_theta * np.pi / 180.0
        
        self.bg_data = np.array(self.dataset["bg_model"]["data"])
        self.calib_data = self.dataset["calib_data"]
        print(self.calib_data)
    
    def read_scan(self):
        #print(len(self.dataset["scans"]))
        self.scan = np.array(self.dataset["scans"][0]["data"])
        self.ts = self.dataset["scans"][0]["ms"]
        #print(self.scan)
        del self.dataset["scans"][0]
        
        if self.dataset["scans"]:
            return False
        else:
            return True
        #print(self.scan)
    def remove_bg(self):
        
        bg_delta = abs(self.bg_data - self.scan)
        
        self.data_nobg = self.scan[bg_delta > 15]
        self.theta_nobg = self.raw_theta[bg_delta > 15]
    
    def calibrate(self):
        
        d_th = float(self.calib_data["ang"])
        d_x = float(self.calib_data["sx"])
        d_y = float(self.calib_data["sy"])
        
        #print(self.theta_nobg)
        self.theta_nobg += d_th
        #print(self.theta_nobg)
        
        self.x_nobg, self.y_nobg = pol2cart(self.data_nobg, self.theta_nobg)
        self.x_nobg += d_x*100
        self.y_nobg += d_y*100

class Scene():
    sensors = {Sensor.TYPE_IMAGE: [],
               Sensor.TYPE_RANGE: [],
               }
    roi = {}
    
    
    def __init__(self):
        pass
    
    def add_sensor(self, sensor):
        self.sensors[sensor.type].append(sensor)
        
    def read_data(self):
        pass
    
    def preprocess_data(self):
        '''
        Preprocessing (Background removal, calibration, conversion 
        to cartesian coordinates and low-level fusion of multiple 
        range sensors. Also a roi is applied if it was configured)
        @type (np.array, Bool)
        @return (data, last, ts): xy np.array of points in scene (N x 2),
        True if is the last frame in sensor dataset, timestamp of the current frame 
        '''
        
        x = None
        y = None
        
        ts_array = []
        
        for range_sensor in self.sensors["range"]:
            last = range_sensor.read_scan()
            ts_array.append(range_sensor.ts)
            range_sensor.remove_bg()
            range_sensor.calibrate()
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
            
        #print("ts_array: %s, span: %s" % (ts_array,(max(ts_array)-min(ts_array))))
        ts = max(ts_array)
        x = x/100
        y = y/100
        
        data = np.array([x,y]).transpose()
        
        if self.roi:
            data = self._apply_roi(data, self.roi)
                
        return data, last, ts       
    
    def set_roi(self, roi):
        self.roi = {"ymin":-24,"ymax":30,"xmin":-30,"xmax":40}
        
    @staticmethod
    def _apply_roi(data, roi):
        data = data[data[:,0] >= roi["xmin"]]
        data = data[data[:,0] <= roi["xmax"]]
        
        data = data[data[:,1] >= roi["ymin"]]
        data = data[data[:,1] <= roi["ymax"]]
        return data
    
    def get_clusters(self):
        
        data, last, ts = self.scene.preprocess_data()
        
        dbscan_params = {'eps':0.3, 'min_samples':5}
        db = DBSCAN(**dbscan_params).fit(data)
        core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
        core_samples_mask[db.core_sample_indices_] = True
        labels = db.labels_
        
        # Number of clusters in labels, ignoring noise if present.
        n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
        
        
    
class Blob():
    def __init__(self, data, ts, nf, blob_id):
        self.data = data
        self.ts = ts
        self.nf = nf
        self.id = blob_id
        self.next_blobs = []
        self.prev_blobs = []
        
    def get_features(self):
        xy = self.data
        bbox = np.array([min(xy[:,0:1]), min(xy[:,1:2]),max(xy[:,0:1]), max(xy[:,1:2])])
        self.area = (bbox[2]-bbox[0])*(bbox[3]-bbox[1])
        self.dens = len(xy)/self.area
        self.bbox = bbox
        self.mean = xy.mean(axis=0)
        
    def get_distance_from(self, blob):
        return abs(self.mean - blob.mean)
    
    def set_connection_from(self, blob):
        self.prev_blobs.append(blob)
        blob.next_blobs.append(self.id)
        
        self.vel = self.get_distance_from(blob)/(self.ts - blob.ts)
        self.ang = self._angle_between(self.mean, blob.mean)
    
    def add_connection_to(self, blob):
        self.next_blobs.append(blob.id)

    @staticmethod
    def _unit_vector(vector):
        """ Returns the unit vector of the vector.  """
        return vector / np.linalg.norm(vector)

     
    def _angle_between(self, v1, v2):
        v1_u = self._unit_vector(v1)
        v2_u = self._unit_vector(v2)
        return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))
        
        
        
    
            
            
        
    