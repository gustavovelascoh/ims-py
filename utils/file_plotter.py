import numpy as np
from matplotlib import pyplot as plt



data_1a = np.genfromtxt("../logs/possi_123578.imscfglegs_hist.log.nofilter",
                        delimiter= "\t")
data_1b = np.genfromtxt("../logs/possi_123578.imscfglegs_hist.log",
                        delimiter= "\t")
data_2a = np.genfromtxt("../logs/possi_123.imscfglegs_hist.log.nofilter",
                        delimiter= "\t")
data_2b = np.genfromtxt("../logs/possi_123.imscfglegs_hist.log",
                        delimiter= "\t")

print(data_1a[1:10,:])
print(data_1b[1:10,:])

plt.subplot(2,2,1)
plt.plot(data_1a[:,1:])

plt.subplot(2,2,2)
plt.plot(data_1b[:,1:])

plt.subplot(2,2,3)
plt.plot(data_2a[:,1:])

plt.subplot(2,2,4)
plt.plot(data_2b[:,1:])

plt.show()