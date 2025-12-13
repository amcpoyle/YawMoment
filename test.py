from Car import Car
# throwaway file to test different aspects of the code
car = Car("PR38", "VehicleParameters.xlsx")
car.load_data()
print(car.car_params['cgHeight'])
