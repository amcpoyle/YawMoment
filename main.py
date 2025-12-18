from Car import Car
import numpy as np
from build_plot import build_plot
from forces import forces
import plotly.express as px
import pandas as pd
import matplotlib.pyplot as plt
def main(car_params, velocity):
   
    AxIn = 0

    v = velocity

    # some other variables that are calculated from vehicle params
    downforce = 0.5*car_params['rho']*car_params['refArea']*car_params['dfCoef']*(v**2)
    drag = 0.5*car_params['rho']*car_params['refArea']*car_params['dragCoef']*(v**2)

    # TODO: could put all this stuff in xlsx file to make it easier to change with GUI
    tire = [car_params['lmuy']*2.7309, car_params['lmuy']*-0.275, 8.5, 1.8]
    maxAlpha = np.deg2rad(20)
    kappa = [0,0,0,0] # TODO: no longitudinal slip
    deltaMax = np.deg2rad(11)
    betaMax = np.deg2rad(7)

    i = 1
    steps = 19
    sweep = 40
    tolerance = 0.0001
    k = 0
    tireFzMin = 1000

    # iterating through delta = steering wheel angle (-delta max to delta max)
    delta_range = np.linspace(-deltaMax, deltaMax, steps)
    beta_range = np.linspace(-betaMax, betaMax, sweep)

    # graph1_ay = []
    # graph1_yaw = []
    graph_ay = []
    graph_yaw = []
    graph_num = []
    graph_beta = []
    graph_delta = []

    for delta in delta_range:
        k = 1
        i = 1
        for beta in beta_range:
            AyIn = 2
            Ay = 1

            while abs(AyIn - Ay) > tolerance:
                AyInPrev = AyIn
                AyIn = 0.7*Ay + 0.3*AyInPrev

                # calculate all of our forces etc
                Ax, Ay, fx, fy, Y, tire_fx, tire_fy, tire_fz, drag, radius = forces(car_params, AxIn, AyIn, beta, delta, kappa, tire, v)

            print("Yaw: ", Y)
            graph_ay.append(Ay)
            graph_yaw.append(Y)
            graph_num.append(1)
            graph_beta.append(beta)
            graph_delta.append(delta)
    
    # graph2_ay = []
    # graph2_yaw = []
    for beta in beta_range:
        k = k + 1
        i = 1



        for delta in delta_range:
            AyIn = 2
            Ay = 0
            while abs(AyIn - Ay) > tolerance:
                AyInPrev = AyIn
                AyIn = 0.7*Ay+0.3*AyInPrev
                Ax, Ay, fx, fy, Y, tire_fx, tire_fy, tire_fz, drag, radius = forces(car_params, AxIn, AyIn, beta, delta, kappa, tire, v)
               

            graph_ay.append(Ay)
            graph_yaw.append(Y)
            graph_num.append(2)
            graph_beta.append(beta)
            graph_delta.append(delta)



    # build the data structure
    graph_df = pd.DataFrame({'ay': graph_ay, 'yaw': graph_yaw, 'graph_num': graph_num, 'beta': graph_beta, 'delta': graph_delta})

    print('max Ay: ', max(graph_df['ay']))
    print("max yaw: ", max(graph_df['yaw']))

    return graph_df
    # generate the plot
    # fig = build_plot(graph_df)
    # html = fig.to_html(include_plotlyjs="cdn", full_html=False)
    # return fig
    # fig.show()
    
# if __name__ == "__main__":
#     main()
