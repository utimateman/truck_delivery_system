class TruckOrder:
    def __init__(self, truck_type, number_of_truck, truck_location):
        self.truck_type = truck_type
        self.number_of_truck = number_of_truck
        self.truck_location = truck_location

    def getTruckType(self):
        return self.truck_type

    def getNumberOfTruck(self):
        return self.number_of_truck
    
    def getTruckLocation(self):
        return self.truck_location
        