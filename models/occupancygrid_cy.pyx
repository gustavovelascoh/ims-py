'''
Created on Oct 2, 2017

@author: gustavo
'''
import numpy as np
from builtins import int
cimport numpy as np

cdef class OccupancyGrid(object):
    '''
    classdocs
    '''
    cdef public double xmin, ymin, xmax, ymax, cell_size, xo, yo
    cdef public int col_o, row_o, cols, rows
    cdef public str method
    cdef public double[:,:] grid, meas_grid
    cdef dict occ_val, emp_val

    def __init__(self, xmin, ymin, xmax, ymax,
                 cell_size=0.3,
                 method='logodd'):
        '''
        Constructor
        '''
        self.xmin = xmin
        self.ymin = ymin
        self.xmax = xmax
        self.ymax = ymax
        self.cell_size = cell_size
        self.method = method
        
        dx = xmax-xmin
        dy = ymax-ymin
        
        self.cols = int(np.floor(dx/cell_size)) + 1
        self.rows = int(np.floor(dy/cell_size)) + 1
        
        if method == 'logodd':
            self.meas_grid=np.zeros((self.rows, self.cols))
            self.grid=np.zeros((self.rows, self.cols))
        elif method == "velca":
            self.meas_grid = np.zeros((self.rows, self.cols))
            self.grid = 0.5*np.ones((self.rows, self.cols))
            
            self.occ_val = {"0.1": 0.4,
                       "0.4": 0.5,
                       "0.5": 0.6,
                       "0.6": 0.9,
                       "0.9": 0.9}
            
            self.emp_val = {"0.1": 0.1,
                       "0.4": 0.1,
                       "0.5": 0.4,
                       "0.6": 0.5,
                       "0.9": 0.6}
        #print((np.shape(self.grid)))
        
    def point2index(self, double x, double y):
        
        cdef int col = 0
        cdef int row = 0
        
        col = np.floor((x - self.xmin)/self.cell_size)
        row = self.rows - np.floor((y - self.ymin)/self.cell_size)
        return int(col), int(row)

    def points2indexes(self, np.ndarray[double, ndim=1] x, np.ndarray[double, ndim=1] y):
        
        cols = np.floor((x - self.xmin)/self.cell_size)
        rows = self.rows - np.floor((y - self.ymin)/self.cell_size)
        return cols.astype(int), rows.astype(int)
    
    def set_origin(self, double xo, double yo):
        self.xo = xo
        self.yo = yo
        
        self.col_o, self.row_o = self.point2index(xo, yo)
        #self.mark_fill(xo, yo)
    
    def mark_fill(self, int col, int row, val=0.1):
        if self.method == "logodd":
            if col < self.cols -1 and col > 0 and row < self.rows and row > 0:      
                self.meas_grid[row,col] = val
        elif self.method == "velca":
            if col < self.cols -1 and col > 0 and row < self.rows and row > 0:      
                self.meas_grid[row,col] = 1
    
    def mark_empty(self, int col, int row):
        #print(col, row)
        if self.method == "logodd":
            if col < self.cols and col > 0 and row < self.rows and row > 0:
                if (self.meas_grid[row,col]== 0):
                    self.meas_grid[row,col] = -0.9
        elif self.method == "velca":
            if col < self.cols and col > 0 and row < self.rows and row > 0:
                if (self.meas_grid[row,col]== 0):
                    self.meas_grid[row,col] = -1
            
    def add_meas(self, np.ndarray[double, ndim=1] xs, np.ndarray[double, ndim=1] ys, xo=None, yo=None):
        cdef int x_c, y_r, xe, ye, c, r
        self.mark_fill(self.col_o, self.row_o)
        
        cols, rows = self.points2indexes(xs, ys)
        
#         for x, y in zip(xs, ys):
#             x_c, y_r = self.point2index(x, y)
        for x_c, y_r in zip(cols, rows):
            lop = self.get_line((self.col_o, self.row_o),
                                (x_c, y_r))
            
            xe, ye = lop[-1]
            #print(lop)
            for c, r in lop[1:-1]:
                self.mark_empty(c, r)
            self.mark_fill(xe, ye)
            
    def update(self):
        
        cdef int i,j
        
        if self.method == "logodd":
            self.grid = np.array(self.meas_grid) + np.array(self.grid)           
            #q = np.sum(self.grid)
            #self.grid /= q
            self.meas_grid = np.zeros((self.rows, self.cols))
        elif self.method == "velca":
            

            for i,r in enumerate(self.meas_grid):
                for j,c in enumerate(r):
                    
                    curr_val = self.grid[i,j]
                    
                    if c == 1:
                        self.grid[i,j] = self.occ_val[str(curr_val)]
                    elif c == -1:
                        self.grid[i,j] = self.emp_val[str(curr_val)]
            #self.grid = self.meas_grid + self.grid           
            #q = np.sum(self.grid)
            #self.grid /= q
            self.meas_grid = np.zeros((self.rows, self.cols))

    
    def get_line(self,  start, end): 
        """Bresenham's Line Algorithm
        From:
        http://www.roguebasin.com/index.php?title=Bresenham%27s_Line_Algorithm#Python
        Produces a list of tuples from start and end
     
        >>> points1 = get_line((0, 0), (3, 4))
        >>> points2 = get_line((3, 4), (0, 0))
        >>> assert(set(points1) == set(points2))
        >>> print points1
        [(0, 0), (1, 1), (1, 2), (2, 3), (3, 4)]
        >>> print points2
        [(3, 4), (2, 3), (1, 2), (1, 1), (0, 0)]
        """
        
        cdef int x1, x2, y1, y2, dx, dy, is_steep, error, x, ystep, y
        # Setup initial conditions
        x1, y1 = start
        x2, y2 = end
        dx = x2 - x1
        dy = y2 - y1
     
        # Determine how steep the line is
        
        is_steep = abs(dy) > abs(dx)
     
        # Rotate line
        if is_steep:
            x1, y1 = y1, x1
            x2, y2 = y2, x2
     
        # Swap start and end points if necessary and store swap state
        swapped = False
        if x1 > x2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1
            swapped = True
     
        # Recalculate differentials
        dx = x2 - x1
        dy = y2 - y1
     
        # Calculate error
        error = int(dx / 2.0)
        ystep = 1 if y1 < y2 else -1
     
        # Iterate over bounding box generating points between start and end
        y = y1
        points = []
        #print(x1, x2 + 1)
        for x in range(x1, x2 + 1):
            coord = (y, x) if is_steep else (x, y)
            points.append(coord)
            error -= abs(dy)
            if error < 0:
                y += ystep
                error += dx
     
        # Reverse the list if the coordinates were swapped
        if swapped:
            points.reverse()
        return points
        
    def get_grid(self, double threshold):
        return (np.array(self.grid) > threshold) * 1.0
        
        
        
        