from Car import Car
import numpy as np

def main():
    car = Car("PR38", "VehicleParameters.xlsx")
    car.load_data()
    
    # TODO: could put all this stuff in xlsx file to make it easier to change with GUI
    tire = [car.car_params['lmuy']*2.7309, car.car_params['lmuy']*-0.275, 8.5, 1.8]
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


if __name__ == "__main__":
    main()
