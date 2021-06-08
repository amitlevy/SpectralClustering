# Auxilery functions for cluster manipulation

def from_index_to_clusters(lables, true_k):
    l = [[] for i in range(true_k)]
    for i in range(len(lables)):
        l[lables[i]].append(i)
    return l 

def from_clusters_to_index(clusters, n):
    l = [0 for i in range(n)]
    for i in range(len(clusters)):
        for ind in clusters[i]:
            l[int(ind)] = i
    return l

def create_pairs(clusters):
    s = []
    for l in clusters:
        for i in range(len(l)):
            for j in range(i+1, len(l)):
                s.append((l[i], l[j]))
    return set(s)