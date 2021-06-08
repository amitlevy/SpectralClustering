import numpy as np
import sys

# Those are all spectral clustering related functions

def calc_weighted_adjacency(X, n):
    M = np.fromfunction(np.vectorize(lambda i,j: np.linalg.norm(X[i]-X[j])), (n,n), dtype=int)
    W = np.exp(-0.5*M)
    np.fill_diagonal(W,0)
    return W
    
def calc_L_norm(W, n):
    D = np.diag(W.sum(axis=1))
    Dp12 = np.diag(np.power(np.diag(D),(-(1/2))))
    L_norm = np.identity(n) - np.linalg.multi_dot([Dp12,W,Dp12])  
    return L_norm
 
def calc_K_and_T(Ab, Qb, n, true_k, Random):
    np.seterr(divide='raise')
    eigens = np.diag(Ab).copy()
    sorted_indexes = np.argsort(eigens)
    deltas = [abs(eigens[sorted_indexes[i]]-eigens[sorted_indexes[i+1]]) for i in range(n-1)]
    K = np.argmax(deltas[:(n//2)])+1
    if not Random:
        K = true_k
        print("Not using eigengap huristic, chosen k is: ", K)
    else:
        print("Using eigengap huristic, chosen k is: ", K)
    U = Qb[:, sorted_indexes[:K]]
    factor = np.array(np.power(np.power(U, 2).sum(axis=1), 0.5))
    try:
        T = np.transpose(np.transpose(U)/factor)
    # numpy can raise the following error because of the seterr line:
    except FloatingPointError: 
        sys.exit("FATAL: Devision by zero during calculation of T.")

    return K, T