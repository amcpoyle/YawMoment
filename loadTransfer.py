"""
Helper function for calculating load on each tire
"""
import numpy as np
def loadTransfer(Ax, Ay, downforce, drag, car_params):
    ft = car_params['LLTD']
    rt = 1 - ft
    weight = car_params['vehicleMass']*9.8
    
    a = car_params['a']
    b = car_params['b']
    
    # FL FR RL RR
    A = np.array([[1, -1, 1, -1],
                  [a, a, -b, -b],
                  [1, 1, 1, 1],
                  [1/ft, -1/ft, -1/rt, 1/rt]])


    b_mat = np.array([2*Ay*weight*car_params['cgHeight']/car_params['trackwidth'],
             -Ax*weight*car_params['cgHeight'] + downforce*(car_params['aeroDistr'] - car_params['weightDistr'])*car_params['length'], 
	     weight + downforce, 0])

    
    # load = np.linalg.solve(A, b_mat); # fz per tire [fl fr rl rr]
    load = np.linalg.solve(A, b_mat)

    return load
