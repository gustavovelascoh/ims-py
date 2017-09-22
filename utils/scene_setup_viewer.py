'''
Created on Sep 21, 2017

@author: gustavo
'''



import matplotlib as mpl
import numpy as np

mpl.use('pgf')

def figsize(scale):
    fig_width_pt = 300                          # Get this from LaTeX using \the\textwidth
    inches_per_pt = 1.0/72.27                       # Convert pt to inch
    golden_mean = (np.sqrt(5.0)-1.0)/1.2           # Aesthetic ratio (you could change this)
    fig_width = fig_width_pt*inches_per_pt*scale    # width in inches
    fig_height = fig_width*golden_mean              # height in inches
    fig_size = [fig_width,fig_height]
    return fig_size

pgf_with_latex = {                      # setup matplotlib to use latex for output
    "pgf.texsystem": "pdflatex",        # change this if using xetex or lautex
    "text.usetex": True,                # use LaTeX to write all text
    "font.family": "serif",
    "font.serif": [],                   # blank entries should cause plots to inherit fonts from the document
    "font.sans-serif": [],
    "font.monospace": [],
    "axes.labelsize": 10,               # LaTeX default is 10pt font.
    "text.fontsize": 10,
    "legend.fontsize": 8,               # Make the legend/label fonts a little smaller
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
    "figure.figsize": (30/10,22.5/10),     # default fig size of 0.9 textwidth
    "pgf.preamble": [
        r"\usepackage[utf8x]{inputenc}",    # use utf8 fonts becasue your computer can handle it :)
        r"\usepackage[T1]{fontenc}",        # plots will be generated using this preamble
        ]
    }
mpl.rcParams.update(pgf_with_latex)

from models import scene

from matplotlib import pyplot as plt
import matplotlib.image as mpimg
from matplotlib.figure import Figure
import matplotlib.patches as patches

def savefig(filename):
    plt.savefig('{}.pgf'.format(filename))
    plt.savefig('{}.pdf'.format(filename))

scene = scene.Scene("/home/gustavo/devel/personal/python/ims-py/possi_123578.imscfg")

xos = []
yos = []
angs = []

# Extract origins of lasers
for range_sensor in scene.sensors["range"]:
    xos.append(float(range_sensor.dataset["calib_data"]["sx"]))
    yos.append(float(range_sensor.dataset["calib_data"]["sy"]))
    angs.append(float(range_sensor.dataset["calib_data"]["ang"]))

map_scale = scene.config_data["map"]["scale"]
max_x = scene.config_data["map"]["max_x"]
max_y = scene.config_data["map"]["max_y"]
d_x = scene.config_data["map"]["d_x"]
d_y = scene.config_data["map"]["d_y"]

limits = np.concatenate((
                     ((np.array([0,max_x])/map_scale)+d_x),
                     ((np.array([0,max_y])/map_scale)+d_y)
                     ))

roi = scene.config_data["map"]["roi"]
scene.set_roi(roi)

fig = Figure(figsize=(30/3,22.5/3))
ax = fig.add_subplot(111)

img = mpimg.imread(scene.config_data["map"]["image_path"])

#img = np.mean(img, 2)
print(np.shape(img))

img = img == 0

print(np.shape(img))


plt.plot(xos,yos, marker='o', linestyle=' ', 
                         markerfacecolor='b', markeredgecolor='k',
                         markersize=7)

ax = plt.gca()

for ind, ang in enumerate(angs):
    dy = 2.5*np.sin(ang+np.pi/2)
    dx = 2.5*np.cos(ang+np.pi/2)
    print("ang: %s, dx: %s, dy: %s" % (ang, dx, dy))
    ax.add_patch(
        patches.Arrow(
            xos[ind],
            yos[ind],
            dx,
            dy,
            width=3.0,
            color="blue"
            ))
    
    


ax.text(xos[0]-1, yos[0], "LMS1",
        horizontalalignment='right',
        verticalalignment='top', size='small')
ax.text(xos[1]+1, yos[1], "LMS2", size='small')
ax.text(xos[2]+1, yos[2], "LMS3",
        verticalalignment='top', size='small')
ax.text(xos[3]+1, yos[3], "LMS5",
        verticalalignment='top', size='small')
ax.text(xos[4]-1, yos[4], "LMS7",
        horizontalalignment='right', size='small')
ax.text(xos[5]-1, yos[5], "LMS8",
        horizontalalignment='right', size='small')

# Extract legs data
for leg in scene.config_data["legs"]:
    
    minx = leg['bbox'][0]
    miny = leg['bbox'][1]
    dx = leg['bbox'][2] - minx
    dy = leg['bbox'][3] - miny
    color = "green" if leg["type"] == "departure" else "red"
    
    patch = ax.add_patch(
             patches.Rectangle(
                (minx, miny),
                dx,
                dy,
                fill=False,      # remove background
                edgecolor=color,
                lw=2.0
             ) )
    
leg_idx = 1    
for leg in scene.legs:
    
    dx = 0
    dy = 0
    k = 1
    q = 0
    p = 1
    color = "green"
    
    if leg.type == "approach":
        k = -1
        p = 0
        q = 1
        color = "red"
    
    if leg.heading == 'N':
        dy = 5
    if leg.heading == 'S':
        dy = -5
    if leg.heading == 'E':
        dx = 5
    if leg.heading == 'W':
        dx = -5
    
    ax.add_patch(
        patches.Arrow(
            leg.bbox.center[0]-p*(k*dx),
            leg.bbox.center[1]-p*(k*dy),
            k*dx,
            k*dy,
            width=2.0,
            color=color
            ))
    
    ax.text(
        leg.bbox.center[0]+(dx/2),
        leg.bbox.center[1]+(dy/2),
        str(leg_idx),
        color = color,
        size="large",
        weight="bold",
        horizontalalignment='center',
        verticalalignment='center'
        )
    leg_idx += 1

imgplot = plt.imshow(img, aspect='auto', extent=limits)

#ax.show()
ax.set_title("Intersection Configuration", size='small')
ax.set_xlabel("x [m]", size='small')
ax.set_ylabel("y [m]", size='small')

savefig('intersection-config2')

plt.show()


