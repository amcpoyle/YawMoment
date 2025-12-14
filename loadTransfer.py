"""
Helper function for calculating load on each tire
"""

def load(Ax, Ay, downforce, drag, vehicle):
    ft = vehicle.car_params['LLTD']
    rt = 1 - ft

    A = np.array([[1, -1, 1, -1],
                  [a, a, -b, -b],
                  [1, 1, 1, 1],
                  [1/ft, -1/ft, -1/rt, 1/rt]])

    b_mat = [2*Ay*vehicle.car_params['vehicleMass']*vehicle.car_params['cgHeight']/vehicle.car_params['trackwidth'],
             -Ax*vehicle.car_params['vehicleMass']*vehicle.car_params['cgHeight'] + downforce*(vehicle.car_params['aeroDistr'] - vehicle.car_params['weightDistr'])*vehicle.car_params['length'], vehicle.car_params['vehicleMass'] + downforce, 0]

    
