import argparse
import numpy as np
import random
import kmeans_pp as kmeans_pp
import sys
import data
import clusters_functions
import QR
import spectral_clustering
import aux_functions
    
# Amit Levy 212430730
# Michael Garbois 324957695

# This is the main file, and connects everything together.
# Note that the randomized choosing of k and n happens already in tasks.py,
# as that simplifies the code. (max n=350, max k=20)
# Explanation as to the way max_k and max_n were calculated:
# The way we calculcated the max k and max n is by keeping k constant at k=20 (because
# increasing k comes at the expense of n, and we preferred to choose a larger n and a smaller k, because
# a larger k hurts the results.)
# and increasing n until we reached 5 minutes. We did this at multiple times,
# and chose according to one of the slower runs. At times where the nova is less busy,
# the maximum n that can be run in 5 minutes increases to around 450.


d = random.choice([2,3])
print("Chosen dimension is d = {}.".format(d))
parser = argparse.ArgumentParser()
parser.add_argument("k", help="number of clusters", type=int)
parser.add_argument("n", help="number of observations", type=int)
parser.add_argument('--Random', dest='Random', action='store_true')
parser.add_argument('--no-Random', dest='Random', action='store_false')
parser.set_defaults(Random=True)

args = parser.parse_args()

true_k = args.k
n = args.n
Random = args.Random

if true_k >= n:
    sys.exit("FATAL: K is bigger than n, exiting program")
if true_k < 1:
    sys.exit("FATAL: K is smaller than 1")
 


print("Number of data points: ", n)
# Data Generation
X,lables = data.generate_data(n,true_k,d)

# Forming the weighted adjacency matrix W
W = spectral_clustering.calc_weighted_adjacency(X, n)

# Computing the normalized graph Laplacian L_norm
L_norm = spectral_clustering.calc_L_norm(W, n)
L_norm += np.identity(L_norm.shape[0]) # fix recommended in forum

# Determining k
Ab, Qb = QR.QR_iteration(L_norm, n)

K, T = spectral_clustering.calc_K_and_T(Ab, Qb, n, true_k, Random)

# Sending data to kmeans_pp.py for clusters initialization and clustering
print("****************************************************************")
print("Running spectral clustering...", flush=True)
obs_inds_per_clusters_spectral = kmeans_pp.k_means_pp(T, K, n, K, 300)
print("Done running spectral clustering")
print("Running kmeans++...", flush=True)
obs_inds_per_clusters_kmeans = kmeans_pp.k_means_pp(X, K, n, d, 300)
print("Done running kmeans++", flush=True)
print("****************************************************************")

# Writing out data
data.write_out_clusters(obs_inds_per_clusters_spectral, obs_inds_per_clusters_kmeans, K)

# Calculating Jaccard measure
l = clusters_functions.create_pairs(clusters_functions.from_index_to_clusters(lables, true_k))
jaccard_spec = aux_functions.jaccard(l, clusters_functions.create_pairs(obs_inds_per_clusters_spectral))
jaccard_kmeans = aux_functions.jaccard(l, clusters_functions.create_pairs(obs_inds_per_clusters_kmeans))

print("****************************************************************")
print("Spectral clustering jaccard measure: " + str(jaccard_spec))
print("Kmeans++ jaccard measure: " + str(jaccard_kmeans))
print("****************************************************************")

# Plotting data
data.plot_points(X, clusters_functions.from_clusters_to_index(obs_inds_per_clusters_spectral, n), clusters_functions.from_clusters_to_index(obs_inds_per_clusters_kmeans, n), n, true_k, K, aux_functions.round_sig(jaccard_spec, 3), aux_functions.round_sig(jaccard_kmeans, 3), d)
     
print("Done running!", flush=True)
    





