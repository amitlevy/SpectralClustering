import numpy as np
from aux_functions import CHECK_DIV_ZERO

# This module contains our QR algorithm implementation, 
# and all of the neccesary help functions

EPSILON = 0.0001

# This is the Modified Gram-Schmidt Algorithm, but it is transposed. Same speed, but more convenient.
def calculateQR(A, n):  
    U = np.copy(A)
    U = U.transpose()
    R = np.zeros((n,n))
    Q = np.zeros((n,n))
    for i in range(n):
        R[i][i] = np.linalg.norm(U[i])
        CHECK_DIV_ZERO(R[i][i],"The Modified Gram-Schmidt Algorithm")
        Q[i] = U[i]/(R[i][i])
        R[i+1:n, i] = np.dot(Q[i],U[i+1:n].T)
        if i < n:
            U[i+1:n] -= np.matmul(R[i+1:n,i][np.newaxis].T,Q[i][np.newaxis])

    Q = Q.transpose()
    R = R.transpose()
    return Q,R

def QR_iteration(A, n):
    Ab = np.copy(A)
    Qb = np.identity(n)
    for i in range(n):
        Q,R = calculateQR(Ab, n)
        Ab = np.matmul(R,Q)
        QbQ = np.matmul(Qb,Q)
        if (np.absolute(np.absolute(Qb)-np.absolute(QbQ)) < EPSILON).all():
            print("i:",i)
            return Ab,Qb
        Qb = QbQ
    return Ab,Qb