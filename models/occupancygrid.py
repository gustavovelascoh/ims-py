'''
Created on Oct 2, 2017

@author: gustavo
'''
import numpy as np

class OccupancyGrid(object):
    '''
    classdocs
    '''


    def __init__(self, xmin, ymin, xmax, ymax, cell_size=0.3):
        '''
        Constructor
        '''
        self.xmin = xmin
        self.ymin = ymin
        self.cell_size = cell_size
        
        dx = xmax-xmin
        dy = ymax-ymin
        
        self.cols = np.ceil(dx/cell_size) + 1
        self.rows = np.ceil(dy/cell_size) + 1
        
        self.grid=0.5*np.ones((self.rows, self.cols))
        print((np.shape(self.grid)))
        
    def point2index(self, x, y):
        col = np.ceil((x - self.xmin)/self.cell_size - 0.5)
        row = np.ceil((y - self.ymin)/self.cell_size - 0.5)
        return int(col), int(row)
    
    def set_origin(self, xo, yo):
        self.xo = xo
        self.yo = yo
        
        self.col_o, self.row_o = self.point2index(xo, yo)
        self.mark_fill(xo, yo)
    
    def mark_fill(self, col, row, val=0.9):       
        self.grid[row,col] = val
    
    def mark_empty(self, col, row):
        if (self.grid[row,col]== 0.5):
            self.grid[row,col] = 0.1
    def update(self, xs, ys, xo=None, yo=None):
        self.mark_fill(self.col_o, self.row_o)
        for x, y in zip(xs, ys):
            x_c, y_r = self.point2index(x, y)
            lop = self.get_line((self.col_o, self.row_o),
                                (x_c, y_r))
            
            xe, ye = lop[-1]
            for c, r in lop[1:-1]:
                self.mark_empty(c, r)
            self.mark_fill(xe, ye)
            
            
            
    def add_point_set(self, xs, ys):
        
        dxs = xs - self.xo
        dys = ys - self.yo
        
        m = dys/dxs
        print("m: ", m)
        b = ys - m*xs
        
        for x, y, mc, bc in zip(xs, ys, m, b):
            
            x_c, y_r = self.point2index(x, y)
            
            print((self.col_o, self.row_o), (x_c, y_r))
            lop = self.get_line((self.col_o, self.row_o), (x_c, y_r))
            print(lop)
            
            for xx,yy in lop[1:-2]:
                if (self.grid[xx,yy]== 0.5):
                    self.grid[xx,yy] = 0.1
            
            self.mark_fill(x, y)
            
            xt_0 = x if x < self.xo else self.xo
            xt_1 = x if x > self.xo else self.xo

            xt = np.ogrid[xt_0:xt_1:0.5*self.cell_size]
            yt = mc*xt + bc
            
            for xe, ye in zip(xt, yt):
                self.mark_empty(xe, ye)
    
    def get_line(self, start, end):
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
        print(x1, x2 + 1)
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
        
        
        
        
        