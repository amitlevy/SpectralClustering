import numpy as np
import mykmeanssp as ckmeans

# Our implementation of the Kmeans++ initialization for the Kmeans algorithm

def k_means_pp(T, K, N, d, MAX_ITER):           
    np.random.seed(0)
    
    observations = T

    indexes = np.arange(N)
    if K == 1:
        print("k = 1, clustering is meaningless")
        return [indexes]
    
    centeroid_indexes = [np.random.choice(indexes)]
    centeroids = [observations[centeroid_indexes[0]].tolist()]
    min_D_arr = np.array(np.power(observations - np.array(centeroids[0]), 2).sum(axis=1))
    for k in range(1, K):
        if k != 1:
            currD = np.array(np.power(observations - np.array(centeroids[-1]), 2).sum(axis=1))
            min_D_arr = np.minimum(min_D_arr, currD)
        factor = sum(min_D_arr)
        weights = min_D_arr/factor
        centeroid_indexes.append(np.random.choice(indexes, p=weights))
        centeroids.append(observations[centeroid_indexes[k]].tolist())
    
    obs_inds_per_clusters = ckmeans.ckmeans(K, N, d, MAX_ITER, observations.tolist(), centeroids)
    return obs_inds_per_clusters


