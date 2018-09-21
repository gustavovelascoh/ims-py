import struct
from matplotlib import pyplot as plt
from analyse_results import load_results_file
from analyse_results import max_window, avg_round, count_cars, get_flow_bin, get_flow
import numpy as np


G = 150
TH = 0.5

LASER_FILE = "laser_results.csv"
VIDEO_FILE = "video_results_75_cbt.csv"
GT_FILE = "gt_results.csv"

laser_data = []
laser_data_raw = []
video_data = []
gt_data = []

t = np.arange(0,7118)

laser_data = load_results_file(LASER_FILE)
gt_data = load_results_file(GT_FILE)
video_data = load_results_file(VIDEO_FILE)

gt_temp = gt_data[45:]
vid_temp = video_data[0:-45]
las_temp = laser_data[0:-45]
t = t[0:-45]

gt_data = gt_temp[10:]
video_data = vid_temp[0:-10]
laser_data = las_temp[0:-10]
t = t[0:-10]

t = t/30

laser_data = avg_round(laser_data)
video_data = avg_round(video_data)

vl_avg = np.mean(np.stack((video_data,laser_data)), axis=0)
vl_max = np.max(np.stack((video_data,laser_data)), axis=0)

lc = count_cars(laser_data)
gc = count_cars(gt_data)
vc = count_cars(video_data)

vlac = count_cars(vl_avg)
vlmc = count_cars(vl_max)

lf = get_flow(lc,G)
vf = get_flow(vc,G)
gf = get_flow(gc,G)
vlacf = get_flow(vlac,G)
vlmcf = get_flow(vlmc,G)

vlfa = np.mean(np.stack((vf,lf)), axis=0)
vlfm = np.max(np.stack((vf,lf)), axis=0)

lfb = get_flow_bin(lc,G)
vfb = get_flow_bin(vc,G)
gfb = get_flow_bin(gc,G)
vlacfb = get_flow_bin(vlacf,G)
vlmcfb = get_flow_bin(vlmcf,G)
vlfafb = get_flow_bin(vlfa,G)
vlfmfb = get_flow_bin(vlfm,G)

#plot_var = "video"
plot_var = "all"

if plot_var == "video":
    plt.subplot(3,1,1)
    plt.plot(t, vf,'r')
    plt.plot(t, gf,'k')
    plt.title("Video vs Groundtruth Flow")
    plt.legend(["video","Groundtruth"])
    plt.xlabel("seconds")
    plt.ylabel("vehicles/second")

    plt.subplot(3,1,2)
    plt.plot(t[1800:3300], vf[1800:3300],'r')
    plt.plot(t[1800:3300], gf[1800:3300],'k')
    plt.title("Video vs Groundtruth Flow (Zoom in)")
    plt.legend(["video","Groundtruth"])
    plt.xlabel("seconds")
    plt.ylabel("vehicles/second")

    plt.subplot(3,1,3)
    plt.plot(t[1800:3300], vfb[1800:3300],'r')
    plt.plot(t[1800:3300], gfb[1800:3300]+1.2,'k')
    plt.title("Video vs Groundtruth Flow (Zoom in)")
    plt.legend(["video","Groundtruth"])
    plt.xlabel("seconds")
    plt.ylabel("flow status")

elif plot_var == "all":
    # plt.subplot(3,2,1)
    # plt.plot(t, laser_data,'b')
    # plt.plot(t, video_data,'r')
    # plt.plot(t, gt_data,'k')
    # plt.legend(["laser","video","gt"])
    # plt.title("Occupancy data")
    #
    # plt.subplot(3,2,2)
    # plt.plot(t, vf,'r')
    # plt.plot(t, gf,'k')
    # plt.title("Video vs Groundtruth Flow")

    plt.subplot(2,2,1)
    plt.plot(t, vlacf,'b')
    plt.plot(t, gf,'k')
    plt.title("Avg merge on Occupancy")
    plt.legend(["output","groundtruth"])
    plt.xlim([0, 236])
    plt.xlabel("seconds")
    plt.ylabel("vehicles/second")

    plt.subplot(2,2,2)
    plt.plot(t, vlmcf,'b')
    plt.plot(t, gf,'k')
    plt.title("Max merge on Occupancy")
    plt.legend(["output","groundtruth"])
    plt.xlim([0, 236])
    plt.xlabel("seconds")
    plt.ylabel("vehicles/second")

    plt.subplot(2,2,3)
    plt.plot(t, vlfa,'m')
    plt.plot(t, gf,'k')
    plt.title("Avg merge on Flow")
    plt.legend(["output","groundtruth"])
    plt.xlim([0, 236])
    plt.xlabel("seconds")
    plt.ylabel("vehicles/second")

    plt.subplot(2,2,4)
    plt.plot(t, vlfm,'m')
    plt.plot(t, gf,'k')
    plt.title("Max merge on Flow")
    plt.legend(["output","groundtruth"])
    plt.xlim([0, 236])
    plt.xlabel("seconds")
    plt.ylabel("vehicles/second")

plt.show()
