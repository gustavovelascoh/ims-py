#!/usr/bin/python3
import sensor
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import time
from sklearn.cluster import DBSCAN
import argparse
import os


cwd = os.getcwd()
description_str='Process scene using specified parameters'
parser = argparse.ArgumentParser(description=description_str)
parser.add_argument('laser_list',
                    metavar='L',
                    type=int,
                    nargs='+',
                    help="List of scanners to use. (Available 1, 2, 3, 5, 7, 8)")
parser.add_argument('--sds', action='store_true', help="Save data stats")
args = parser.parse_args()

print("laser_list %s",args.laser_list)
print("sds %s",args.sds)
# Clusters to save
clus_save = range(1,20000, 250)

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

# MODIFY HERE: Select Laser scanners to use
use_laser = args.laser_list
# use_laser = [1, 2, 3, 5, 7, 8]
# use_laser = [1, 8]

dir_path = "scene_" + "".join([str(x) for x in use_laser])
        
if not os.path.exists(dir_path):
    os.makedirs(dir_path)

sds_filename=dir_path + "/data.log"
scene_filename=dir_path + "/scene.log"

if args.sds:
    with open(sds_filename, '+w') as out:
        data_log="Frame   Clusters\n"
        out.write(data_log)

#Add laser sensors to Scene
for laser_n in use_laser:
    laser_sensors[laser_n].set_src_path(lms_files[laser_n])
    scene.add_sensor(laser_sensors[laser_n])
    
for range_sensor in scene.sensors["range"]:
    range_sensor.load()    

#lms1.set_src_path("possi.lms3")
#lms1.load()
process_log="Range sensors in the scene: %d" % len(scene.sensors["range"]) + "\n"

print("Range sensors in the scene: %d" % len(scene.sensors["range"]))

#exit()

theta = np.arange(0, 180.5, 0.5)
theta = theta * np.pi / 180.0

last = 0

xos = []
yos = []
angs = []

# Extract origins
for range_sensor in scene.sensors["range"]:
    xos.append(float(range_sensor.dataset["calib_data"]["sx"]))
    yos.append(float(range_sensor.dataset["calib_data"]["sy"]))
    angs.append(float(range_sensor.dataset["calib_data"]["ang"]))

# MODIFY HERE: Select whether to plot process or not
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
scene.set_roi(roi)

blob_list = []
blob_count = 1

tstart = time.time()
while not last:
    #print("Frame %d" % nf)
    data_log = ("%05d   " % nf)
    
    #plt.pause(1)
    # Preprocessing
    data, last, ts = scene.preprocess_data()
    
#     if (nf > 10):
#         exit()
         
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
#     data = np.array([x,y]).transpose()
#     print(data)
#     print("shape data: %s" % (str(np.shape(data))))
#     exit()
#     data = sensor.apply_roi(data, roi)
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
    
    clusters_data = {"raw": data,
                       "db": db,
                       "frame": nf,
                       "ts": ts,
                       "lasers": use_laser,
                       }
    
    unique_labels = set(labels)
    temp_blob_list = []
    
    for k in unique_labels:
        if k != -1:
            class_member_mask = (labels == k)
            
            if (sum(class_member_mask) >= db.min_samples):
                blob = sensor.Blob(data[class_member_mask],
                                      ts,
                                      nf,
                                      blob_count)
                blob.get_features()
                temp_blob_list.append(blob)
                blob_count += 1
    
    blob_list.append(temp_blob_list)
    
    print("blobs %s" % [b.mean for b in blob_list[nf-1]])
    
    if nf > 4:
        print(blob_list)
        exit()
    
    #print('Estimated number of clusters: %d' % n_clusters_)
    data_log += str(n_clusters_) + "\n"
    
    if args.sds:
        with open(sds_filename, '+a') as out:            
            out.write(data_log)
    
    if plot_process:
        unique_labels = set(labels)
        #colors = plt.cm.Jet(np.linspace(0, 1, len(unique_labels)))
        colors = ['b', 'g', 'r', 'm']
        colors = colors*50
        
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
        #ax.draw_a rtist(imgplot)
        #ax.draw_artist(lasers_pts)
        #fig.canvas.blit(ax.bbox)
        #fig.canvas.restore_region(background)
        fig.canvas.draw()
    
    if nf in clus_save:
        
        import pickle
        
        #dir_path = "scene_" + "".join([str(x) for x in use_laser])
        
        clusters_data = {"raw": data,
                        "db": db,
                        "frame": nf,
                        "ts": ts,
                        "lasers": use_laser,
                        }
        output_file = dir_path + "/" + format(nf,'05') + ".clus"        
        fo = open(output_file, "wb")
        pickle.dump(clusters_data, fo, pickle.HIGHEST_PROTOCOL)
    
    nf+=1   
    
    #input()
    if nf == 22000:
        break

process_log += 'FPS: %s ' % ((nf-1)/(time.time()-tstart))
#print('FPS:' , (nf-1)/(time.time()-tstart))
print(process_log)
with open(scene_filename, '+w') as out:
    out.write(process_log)

