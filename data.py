from sklearn.datasets import make_blobs
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

# All of the IO related functions
# includes: data generation, creation of text files and creation of plot

def generate_data(n,k,d):
    print("Generating data points")
    X, y = make_blobs(n_samples=n, centers=k, n_features=d)
    write_out_data(X, y, d)
    print("Done generating data points")
    return X, y

def write_out_data(X, y, d):
    print("Saving data to file: \"data.txt\"")
    write_out = np.concatenate((X, np.array([y]).T), axis=1)
    fmt = ['%.8f' for i in range(d)]
    fmt.append('%d')
    try:
        with open("./data.txt", 'w') as fout:
            np.savetxt(fout, write_out, fmt=fmt, delimiter=',')
            fout.close()
        print("\"data.txt\" created")
    except IOError:
        print("Could not open file: \"data.txt\"")
    return
    
def write_out_clusters(obs_inds_per_clusters_spectral, obs_inds_per_clusters_kmeans, K):
    print("Saving final clusters to file: \"clusters.txt\"")
    clusters = obs_inds_per_clusters_spectral + obs_inds_per_clusters_kmeans
    try:
        with open("./clusters.txt", 'w') as f:
            f.write(str(K) + '\n')
            for line in clusters:
                for i in range(len(line)-1):
                    f.write(str(int(line[i])) + ',')
                f.write(str(int(line[-1])) + '\n')
            f.close()
        print("\"clusters.txt\" created")
    except IOError:
        print("Could not open file: \"clusters.txt\"")
        
        
def plot_points(X, clusters_spec, clusters_kmeans, n, true_k, K, jaccard_spec, jaccard_kmeans, d): 
    print("Plotting clusters to file: \"clusters.pdf\"")
    heights = [3, 1]

    fig = plt.figure(constrained_layout=False)
    gs = fig.add_gridspec(2, 2, height_ratios=heights, left=0.05, right=0.95)
    
    ax1 = fig.add_subplot(gs[-1, :])
    ax1.margins(0.05)          
    ax1.text(0, -0.08, 'Data was generated from the values:\n n = ' + str(n) + ' , k = ' + str(true_k) + '\n The k that was used for both algorithms is ' + str(K) + '\n The Jaccard measure for Spectral Clustering: ' + str(jaccard_spec) + '\n The Jaccard measure for K-means: ' + str(jaccard_kmeans), fontsize=14, horizontalalignment='center')
    ax1.axis('off')
    
    if d == 2:
        ax2 = fig.add_subplot(gs[0, 0])
        ax2.scatter(X.T[0], X.T[1], c=clusters_spec, cmap='gist_rainbow')
        ax3 = fig.add_subplot(gs[0, 1])
        ax3.scatter(X.T[0], X.T[1], c=clusters_kmeans, cmap='gist_rainbow')
    elif d == 3:
        ax2 = fig.add_subplot(gs[0, 0], projection='3d')
        ax2.scatter(X.T[0], X.T[1], X.T[2], c=clusters_spec, cmap='gist_rainbow')
        ax3 = fig.add_subplot(gs[0, 1], projection='3d')
        ax3.scatter(X.T[0], X.T[1], X.T[2], c=clusters_kmeans, cmap='gist_rainbow')
    ax2.set_title('Normalized Spectral Clustering')
    ax3.set_title('K-means')
    
    try:
        plt.savefig("./clusters.pdf")
        print("\"clusters.pdf\" created")
    except IOError:
        print("Could not open file: \"clusters.pdf\"")