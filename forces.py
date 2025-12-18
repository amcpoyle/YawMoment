import numpy as np
from loadTransfer import loadTransfer
from tireModel import Pacejka4_Model
from tireModelConstants import tireConstants

def forces(car_params, AxIn, AyIn, beta, delta, kappa, tire):
    v = car_params['v']
    radius = (v**2)/(AyIn*9.81)
    weight = car_params['vehicleMass']*9.8
    psi_dot = AyIn/v; # yaw rate


    # converting beta at rear to beta at cg
    beta = beta-psi_dot*car_params['b']/v


    downforce = 0.5*car_params['rho']*car_params['refArea']*car_params['dfCoef']*(v**2)
    drag = 0.5*car_params['rho']*car_params['refArea']*car_params['dragCoef']*(v**2)
    load = loadTransfer(AxIn, AyIn, downforce, drag, car_params)

    
    # TODO: 30 seems arbitrary?
    if any(i < 30 for i in load):
        print("warning: low load ", load)


    beta_vy = -v*np.tan(beta)

    yaw_vy_front = car_params['a']*psi_dot
    yaw_vy_rear = -car_params['b']*psi_dot

    vy_front = beta_vy + yaw_vy_front
    vy_rear = beta_vy + yaw_vy_rear

    alpha_rl = -np.atan(vy_rear/v) + car_params['rearToe'] # TODO: need to fix toe
    fy_rl = Pacejka4_Model(tire, [alpha_rl, load[2]])
    mz_rl = Pacejka4_Model(tireConstants.Mz, [alpha_rl, load[2]])
    

    alpha_rr = -(-np.atan(vy_rear/v) - car_params['rearToe'])
    fy_rr = Pacejka4_Model(tire, [alpha_rr, load[3]])
    mz_rr = Pacejka4_Model(tireConstants.Mz, [-alpha_rr, load[3]])
    fy_rr = -fy_rr # TODO: why

    ackermannToe = delta**2

    alpha_fl = -np.atan(vy_front/v) + delta + ackermannToe + car_params['frontToe']
    fy_fl = Pacejka4_Model(tire, [alpha_fl, load[0]])
    mz_fl = Pacejka4_Model(tireConstants.Mz, [alpha_fl, load[0]])
    
    alpha_fr = -np.atan(vy_front/v) + delta - ackermannToe - car_params['frontToe']
    fy_fr = Pacejka4_Model(tire, [alpha_fr, load[1]])
    mz_fr = Pacejka4_Model(tireConstants.Mz, [alpha_fr, load[1]])
    # fy_fr = -fy_fr


    fy_rear = fy_rl + fy_rr

    fx_rear = fy_rl*np.sin(car_params['rearToe']) + fy_rr*np.sin(car_params['rearToe'])

    fy_front = fy_fr*np.cos(delta - car_params['frontToe']) + fy_fl*np.cos(delta + car_params['frontToe'])
    fx_front = -fy_fl*np.sin(car_params['frontToe'] + delta) + fy_fr*np.sin(car_params['frontToe'] - delta)

    fy = fy_front + fy_rear
    fx = fx_rear + fx_front - drag

    fx_left = -fy_fl*np.sin(car_params['frontToe'] + delta) - fy_rl*np.sin(car_params['rearToe'])
    fx_right = fy_fr*np.sin(car_params['frontToe'] - delta) + fy_rr*np.sin(car_params['rearToe'])

    mz_total = mz_fr + mz_fl + mz_rr + mz_rl
    
    Ax = fx/weight
    Ay = fy/weight
    Y = fy_front*car_params['a'] - fy_rear*car_params['b'] + (fx_left - fx_right)*car_params['trackwidth'] - mz_total

    tire_fx = [0,0,0,0] # no longitudinal slip
    tire_fy = [fy_fl, fy_fr, fy_rl, fy_rr]
    tire_fz = np.transpose(load)

    steer_torque = ((fy_fl + fy_fr)*0.006 + mz_fr + mz_fl)/5.5

    return [Ax, Ay, fx, fy, Y, tire_fx, tire_fy, tire_fz, drag, radius] # TODO: matlab code switches radius for psi dot
