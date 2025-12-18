import numpy as np
def Pacejka4_Model(P, X):
    x1 = X[0] # slip
    x2 = X[1] # fz
    d1 = P[0]
    d2 = P[1]
    b = P[2]
    c = P[3]

    d = (d1 + d2/1000*x2)*x2

    fy = d*np.sin(c*np.atan(b*x1))
    return fy
