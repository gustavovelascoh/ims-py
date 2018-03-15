import pickle
import numpy as np



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
    bg_removed = False
    
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
        
        self.ts_0 = self.dataset["scans"][0]["ms"]
    
    def read_scan(self):
        #print(len(self.dataset["scans"]))
        self.bg_removed = False
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
        self.bg_removed = True
    
    def calibrate(self):
        
        d_th = float(self.calib_data["ang"])
        d_x = float(self.calib_data["sx"])
        d_y = float(self.calib_data["sy"])
        
        if not self.bg_removed:
            self.data_nobg = self.scan
            self.theta_nobg = self.raw_theta +d_th
        
        else:#print(self.theta_nobg)
            self.theta_nobg += d_th
        #print(self.theta_nobg)
        
        self.x_nobg, self.y_nobg = pol2cart(self.data_nobg, self.theta_nobg)
        self.x_nobg += d_x*100
        self.y_nobg += d_y*100


        
        
        
    
            
            
        
    