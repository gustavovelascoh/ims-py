import sensor
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import time
from sklearn.cluster import DBSCAN


clus_save = range(1,10000, 500)

img=mpimg.imread('image.bmp')

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


scene = sensor.Scene()

lms1 = sensor.Laser(sensor.Laser.SUBTYPE_SINGLELAYER)
lms2 = sensor.Laser(sensor.Laser.SUBTYPE_SINGLELAYER)
lms3 = sensor.Laser(sensor.Laser.SUBTYPE_SINGLELAYER)
lms5 = sensor.Laser(sensor.Laser.SUBTYPE_SINGLELAYER)
lms7 = sensor.Laser(sensor.Laser.SUBTYPE_SINGLELAYER)
lms8 = sensor.Laser(sensor.Laser.SUBTYPE_SINGLELAYER)

laser_sensors = [0, lms1, lms2, lms3, 0, lms5, 0, lms7, lms8]
lms_files = ["", "possi.lms1","possi.lms2","possi.lms3",
             "", "possi.lms5", "", "possi.lms7","possi.lms8"]

use_laser = [1, 2, 3, 5, 7, 8]
# use_laser = [1, 8]

for laser_n in use_laser:
    laser_sensors[laser_n].set_src_path(lms_files[laser_n])
    scene.add_sensor(laser_sensors[laser_n])
    
for range_sensor in scene.sensors["range"]:
    range_sensor.load()    

#lms1.set_src_path("possi.lms3")
#lms1.load()

print("Range sensors in the scene: %d" % len(scene.sensors["range"]))

#exit()

theta = np.arange(0, 180.5, 0.5)
theta = theta * np.pi / 180.0

last = 0

xos = []
yos = []
angs = []

for range_sensor in scene.sensors["range"]:
    xos.append(float(range_sensor.dataset["calib_data"]["sx"]))
    yos.append(float(range_sensor.dataset["calib_data"]["sy"]))
    angs.append(float(range_sensor.dataset["calib_data"]["ang"]))

plot_process = False

if plot_process:
    fig = plt.figure(figsize=(30/3,22.5/3))
    #ax = fig.add_subplot(111, projection='polar')
    ax = fig.add_subplot(111)
    print(ax)
    #ax.set_rmax(6000)
    
    imgplot = ax.imshow(img, extent=limits, aspect='auto')
    print(imgplot)

    # xos = [0, 23.7, 13.12, 12.68, -8.62, -2.2]
    # yos = [-21.4, 15.6, 26.7, -21.74, 17.1, 22.56]
    # angs = [0.150098, -3.344051, -4.174827, -0.059341, 3.679154, -1.933825]
    
    
    lasers_pts, = ax.plot(xos,yos, '.', markerfacecolor='g', markeredgecolor='k', markersize=10)
    plt.ylim(ymin=-25,ymax=32)
    plt.xlim(xmin=-30,xmax=40)
    
    fig.show()
    #fig.draw()
    fig.canvas.draw()
    #fig.canvas.manager.show()
    background = fig.canvas.copy_from_bbox(ax.bbox)
    rdata, = ax.plot(theta)
#print(rdata)
#rdata, = ax.plot(theta, theta, color='b',linestyle='None', marker='.',linewidth=2)
nf = 1

roi={"ymin":-24,"ymax":30,"xmin":-30,"xmax":40}

tstart = time.time()
while not last:
    print("Frame %d" % nf)
    
    #plt.pause(1)
    x = None
    y = None
    #y = []
    
    for range_sensor in scene.sensors["range"]:
        last = range_sensor.read_scan()
        range_sensor.remove_bg()
        range_sensor.calibrate()
        #print(len(range_sensor.x_nobg))
        #print(range_sensor.x_nobg)
        if x != None:
            #print("x %s" % x)
            #print("xnbg %s" % range_sensor.x_nobg)
            x = np.concatenate((x, range_sensor.x_nobg))
            y = np.concatenate((y, range_sensor.y_nobg))
        else:
            x = range_sensor.x_nobg
            y = range_sensor.y_nobg
        
        #print(range_sensor.ts)
            
        
    #print("new x %s " % x)
    #print(lms1.scan)
    #dir(lms1.scan)
    #laser_data = lms1.scan["data"]
    x = x/100
    y = y/100
    
    #print(lms1.scan.data)
    #print("len data %d" % len(lms1.scan.data))
    
    # For plotting raw data
    # theta = lms1.raw_theta
    # laser_data = lms1.scan
    
    # For plotting no bg data (uncalibrated)
    #theta = lms1.theta_nobg
    #laser_data = lms1.data_nobg
    #print(len(laser_data))
    #if 
    #x=range_sensor.x_nobg
    #y=range_sensor.y_nobg
    
    #ax = plt.subplot(111)
    if plot_process:
        ax.clear()
    #rdata.set_xdata(theta)
    #rdata.set_ydata(laser_data)
    #rdata.set_data(theta, laser_data)
    #rdata, = ax.plot(theta, laser_data, color='b',linestyle='None', marker='.',linewidth=2)
    #rdata, = ax.plot(x, y,color='b',linestyle='None', marker='.',linewidth=2)
    # rdata, = ax.plot(False)
    #rdata.set_data(theta, laser_data)
    #print(rdata)
    #rdata.set_xdata(theta)
    #rdata.set_ydata(laser_data)
    #rdata.set_linestyle('None')
    #rdata.set_color('g')
    #rdata.set_marker('.')
    #ax.grid(False)
    #ax.set_yticklabels([])
    

        plt.ylim(ymin=roi["ymin"],ymax=roi["ymax"])
        plt.xlim(xmin=roi["xmin"],xmax=roi["xmax"])
    
    #ax.draw_artist(rdata)
    #fig.canvas.blit(ax.bbox)
    #fig.canvas.draw()
    
    #ax.set_rmax(2.0)
    #plt.ylim(ymin=-10)
    #plt.show(block=last)
    
    #fig.canvas.restore_region(background)

    # redraw just the points
    #ax.draw_artist(rdata)

    # fill in the axes rectangle
    #fig.canvas.blit(ax.bbox)
    
    #rdata.set_linestyle('None')
    #rdata.set_color('b')
    #rdata.set_marker('.')
    #ax.grid(False)
    #ax.set_yticklabels([])
    
    
    
    
    #print("shape x: %s, shape y: %s" % (str(np.shape(x)), str(np.shape(y))))
    data = np.array([x,y]).transpose()
    #print(data)
#print("shape data: %s" % (str(np.shape(data))))
    data = sensor.apply_roi(data, roi)
    #data.transpose()
    #print(x.reshape(1,-1))
    #print(data)
    #print("shape data: %s" % (str(np.shape(data))))
    #input()
    dbscan_params = {'eps':0.3, 'min_samples':5}
    db = DBSCAN(**dbscan_params).fit(data)
    core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
    core_samples_mask[db.core_sample_indices_] = True
    labels = db.labels_
#     print(db.labels_)
#     print(db.core_sample_indices_)
#     exit()
    
    # Number of clusters in labels, ignoring noise if present.
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
    
    print('Estimated number of clusters: %d' % n_clusters_)
    
    if plot_process:
        unique_labels = set(labels)
        #colors = plt.cm.Jet(np.linspace(0, 1, len(unique_labels)))
        colors = ['b', 'g', 'r', 'm']
        colors+= colors+colors
        colors+= colors+colors
        colors+= colors+colors
        colors+= colors+colors
        
        colors_final = colors[0:len(unique_labels)]
        
        for k, col in zip(unique_labels, colors_final):
            if k == -1:
                # Black used for noise.
                col = 'k'
    
            class_member_mask = (labels == k)
            
            
        
            xy = data[class_member_mask & core_samples_mask]
            #print("Size data %s" % str(np.shape(data)))
            #print("Size xy %s" % str(np.shape(xy)))
            #print(xy)
            ax.plot(xy[:, 0], xy[:, 1], '.', markerfacecolor=col,
                     markeredgecolor='k', markersize=10)
    
            xy = data[class_member_mask & ~core_samples_mask]
            ax.plot(xy[:, 0], xy[:, 1], '.', markerfacecolor=col,
                     markeredgecolor='k', markersize=4)
        
        #fig.title('Estimated number of clusters: %d' % n_clusters_)
        #plt.show()
        
        #exit()
        
        imgplot = ax.imshow(img, extent=limits, aspect='auto')
    # 
    #     xos = [0, 23.7, 13.12, 12.68, -8.62, -2.2]
    #     yos = [-21.4, 15.6, 26.7, -21.74, 17.1, 22.56]
    #     angs = [0.150098, -3.344051, -4.174827, -0.059341, 3.679154, -1.933825]
    #     
        ax.plot(xos,yos, '.', marker='v', markerfacecolor='g', markeredgecolor='k', markersize=10)
        #print(ax)
        #imgplot.set_data(img)
        #ax.draw_artist(imgplot)
        #ax.draw_artist(lasers_pts)
        #fig.canvas.blit(ax.bbox)
        #fig.canvas.restore_region(background)
        fig.canvas.draw()
    
    if nf in clus_save:
        
        import pickle
        
        cluster_data = {"raw": data,
                        "db": db,
                        "frame": nf,
                        "lasers": use_laser,
                        }
        output_file = format(nf,'05') + "_" + "".join([str(x) for x in use_laser]) + ".clus"
        
        fo = open(output_file, "wb")
        pickle.dump(cluster_data, fo, pickle.HIGHEST_PROTOCOL)
    
    nf+=1   
    
    #input()
    if nf == 12000:
        break

print('FPS:' , (nf-1)/(time.time()-tstart))

