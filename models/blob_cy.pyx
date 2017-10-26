'''
Created on May 7, 2017

@author: gustavo
'''
import numpy as np
cimport numpy as np
from math import ceil


cdef class Blob(object):
    '''
    classdocs
    '''
    cdef object data
    cdef public object bbox
    cdef object mean
    cdef public int ts, nf, id
    cdef double vel, ang, dens
    cdef public list next_blobs, prev_blobs

    def __init__(self,np.ndarray[double, ndim=2]  data, int ts, int nf, int blob_id):
        self.data = data
        self.ts = ts
        self.nf = nf
        self.id = blob_id
        self.next_blobs = []
        self.prev_blobs = []
        self.vel = 0.0
        self.ang = 0.0
        
    def get_features(self):
        cdef np.ndarray[double, ndim=2] xy
        xy = self.data
        bbox = np.array([min(xy[:,0:1]), min(xy[:,1:2]),max(xy[:,0:1]), max(xy[:,1:2])])
        self.bbox = BoundingBox((bbox[0], bbox[1]), (bbox[2], bbox[3]))        
        self.dens = len(xy)/self.bbox.area
        self.mean = xy.mean(axis=0)
        
    def get_distance_from(self, blob):
        return abs(np.linalg.norm(self.mean - blob.mean))
    
    def set_connection_from(self, blob):
        self.prev_blobs = blob.prev_blobs + [blob.id]
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
    
cdef class BoundingBox(object):
    
    cdef public double width, height, area, center_x, center_y
    cdef public double minx, miny, maxx, maxy
    
#     minxy = None
#     maxxy = None
#     width = None
#     height = None
#     area = None
#     center = None
    
    def __init__(self, minxy, maxxy):
        '''
        @param minxy: Tuple of min coordinate point of bounding box e.g. (0,0)
        @param maxxy: Tuple of max coordinate point of bounding box e.g. (2,5)
        '''
        
        #self.minxy = minxy
        #self.maxxy = maxxy
        self.minx = minxy[0]
        self.miny = minxy[1]
        self.maxx = maxxy[0]
        self.maxy = maxxy[1]
        
        dx = maxxy[0] - minxy[0]
        dy = maxxy[1] - minxy[1]
        
        dx_cm = dx * 100
        dy_cm = dy * 100
        
        grid_k = 50
        
        self.width = (ceil((dx_cm) / grid_k)*grid_k)/100
        self.height = (ceil((dy_cm) / grid_k)*grid_k)/100
        self.area = self.width * self.height
        self.center_x, self.center_y = (minxy[0]+(self.width/2), minxy[1]+(self.height/2))
    
    def is_in(self, point):
        '''
        Tests if a point is inside the bounding box
        @param point: tuple of coordinate point (x,y)
        @return: Boolean, True if point is inside bbox, False otherwise. 
        '''
        
        ret = False
        
        if point[0] >= self.minx and point[0] <= self.maxx:
            if point[1] >= self.miny and point[1] <= self.maxy:
                ret = True
            
        return ret
    
    def __str__(self):
        blob_str = "minxy: (%s,%s)"  % (self.minx, self.miny)
        blob_str += "maxxy: (%s,%s)"  % (self.maxx, self.maxy)
        return blob_str
    
    