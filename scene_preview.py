import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from time import sleep
import matplotlib.patches as patches


img=mpimg.imread('possi/image.bmp')

# map_scale = 5.13449
map_scale = 4.1345
max_x = 300
max_y = 225
# d_x = -32.6
d_x = -30.2
# d_y = -31.8
d_y = -24

limits = np.concatenate((
                         ((np.array([0,max_x])/map_scale)+d_x),
                         ((np.array([0,max_y])/map_scale)+d_y)
                         ))



fig = plt.figure()
ax = fig.add_subplot(111)

imgplot = ax.imshow(img, extent=limits, aspect='auto')

xos = [0, 23.7, 13.12, 12.68, -8.62, -2.2]
yos = [-21.4, 15.6, 26.7, -21.74, 17.1, 22.56]
angs = [0.150098, -3.344051, -4.174827, -0.059341, 3.679154, -1.933825]

ax.plot(xos,yos, '.', markerfacecolor='b', markeredgecolor='k', markersize=10)


#plt.show()

import json

json_data=open("possi.legs").read()

data = json.loads(json_data)

for leg in data:
    
    minx = leg['bbox'][0]
    miny = leg['bbox'][1]
    dx = leg['bbox'][2] - minx
    dy = leg['bbox'][3] - miny
    
    color = "purple" if leg["type"] == "departure" else "cyan"
    
    ret = ax.add_patch(
         patches.Rectangle(
            (minx, miny),
            dx,
            dy,
            fill=False,      # remove background
            edgecolor=color
         ) )
    
    print (ret)
plt.show()
#sleep(15)
