import numpy as np
from matplotlib import pyplot as plt



data_1a = np.genfromtxt("../logs/possi_123578.imscfglegs_hist.log.nofilter",
                        delimiter= "\t")
data_1b = np.genfromtxt("../logs/possi_123578.imscfglegs_hist.log",
                        delimiter= "\t")
data_2a = np.genfromtxt("../logs/possi_123.imscfglegs_hist.log.nofilter",
                        delimiter= "\t")
data_2b = np.genfromtxt("../logs/possi_123578_90.imscfglegs_hist.log",
                        delimiter= "\t")

data_1b_norm = data_1b[:,1:] / np.max(data_1b[1:,1:],0)
data_2b_norm = data_2b[:,1:] / np.max(data_2b[1:,1:],0)

print(data_1a[1:10,:])
print(data_1b[1:10,:])

# plt.subplot(2,2,1)
# plt.plot(data_1a[:,1:])
# 
# plt.subplot(2,2,2)
plt.subplot(2,1,1)
plt.plot(data_1b_norm)

plt.subplot(2,1,2)
plt.plot(data_2b_norm)
# 
# plt.subplot(2,2,3)
# plt.plot(data_2a[:,1:])
# 
# plt.subplot(2,2,4)
# plt.plot(data_2b[:,1:])

plt.show()