import struct
from matplotlib import pyplot as plt
from analyse_results import load_results_file
from analyse_results import max_window, avg_round 


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


plt.subplot(3,1,1)
plt.plot(laser_data)
plt.plot(video_data)
plt.plot(gt_data)
plt.legend(["laser","video","gt"])

plt.subplot(3,1,2)
plt.plot(laser_data)
plt.plot(gt_data)
plt.plot(avg_round(laser_data),'k')
plt.legend(["laser","gt","laserw3"])

plt.subplot(3,1,3)
plt.plot(video_data)
plt.plot(gt_data)
plt.plot(avg_round(video_data),'k')
plt.legend(["video","gt","videow3"])

plt.show()
