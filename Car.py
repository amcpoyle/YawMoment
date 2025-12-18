import pandas as pd
import numpy as np

class Car:
    car_params = {'cgHeight': None, 'length': None, 'trackwidth': None, 'a': None, 'b': None,
                  'weightDistr': None, 'rearToe': None, 'frontToe': None, 'vehicleMass': None,
                  'LLTD': None, 'rho': None, 'copHeight': None, 'aeroDistr': None, 'dragCoef': None,
                  'dfCoef': None, 'refArea': None, 'lmuy': None, 'vehicleName': None}
    # input constants for our tire model
    def __init__(self, data_path):
        self.data_path = data_path

    def load_data(self):
        car_df = pd.read_excel(self.data_path) # parameter name, value, description, unit format
        # assign parameters from csv file
        # TODO: I can make it so that we just start with an empty dictionary
        # car_params = {} and fill values from the excel file
        for cp in Car.car_params.keys():
            value = car_df[car_df['ParameterName'] == cp]['Value']
            if (cp == 'rearToe') | (cp == 'frontToe'):
                value = np.deg2rad(value.iloc[0])
                Car.car_params[cp] = value
            else:
                Car.car_params[cp] = value.iloc[0]
