import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
from sklearn.decomposition import PCA

file_data = np.genfromtxt("../logs/possi_123578.imscfglegs_hist.log",
                        delimiter= "\t")

data = file_data[1:,1:]

print(data[0:5,:])

pca = PCA(n_components=2)
a = pca.fit(data).transform(data)

print(pca.explained_variance_ratio_)

comps = pca.components_


plt.figure()
plt.scatter(a[:, 0], a[:, 1])
plt.show()



dbscan_params = {'eps':0.03, 'min_samples':5}
db = DBSCAN(**dbscan_params).fit(data)

n_clusters_ = len(set(db.labels_)) - (1 if -1 in db.labels_ else 0)

print(db.labels_)
print(n_clusters_)
