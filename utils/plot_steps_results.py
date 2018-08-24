import struct
from matplotlib import pyplot as plt
from analyse_results import load_results_file
from analyse_results import max_window, avg_round, count_cars, get_flow_bin, get_flow


LASER_FILE = "laser_results.csv"
VIDEO_FILE = "video_results_75_cbt.csv"
GT_FILE = "gt_results.csv"

laser_data = []
laser_data_raw = []
video_data = []
gt_data = []

laser_data = load_results_file(LASER_FILE)
gt_data = load_results_file(GT_FILE)
video_data = load_results_file(VIDEO_FILE)

gt_temp = gt_data[45:]
vid_temp = video_data[0:-45]
las_temp = laser_data[0:-45]

gt_data = gt_temp[10:]
video_data = vid_temp[0:-10]
laser_data = las_temp[0:-10]

laser_data = avg_round(laser_data)
video_data = avg_round(video_data)

lc = count_cars(laser_data)
gc = count_cars(gt_data)
vc = count_cars(video_data)

lf = get_flow(lc,300)
vf = get_flow(vc,300)
gf = get_flow(gc,300)

lfb = get_flow_bin(lc,300)
vfb = get_flow_bin(vc,300)
gfb = get_flow_bin(gc,300)

print(vf[0:100])

plt.subplot(3,1,1)
plt.plot(laser_data)
plt.plot(video_data)
plt.plot(gt_data)
plt.legend(["laser","video","gt"])

plt.subplot(3,1,2)
plt.plot(lc)
plt.plot(vc)
plt.plot(gc,'k')
plt.legend(["laser","video","ground_truth"])

plt.subplot(3,1,3)
plt.plot(lf,'b')
plt.plot(vf,'r')
plt.plot(gf,'k')
plt.plot(lfb,' xb')
plt.plot(vfb,' xr')
plt.plot(gfb,' xk')

plt.legend(["laser","video","gt"])

plt.show()
