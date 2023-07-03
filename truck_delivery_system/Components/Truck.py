class Truck:
    def __init__(self, truck_id, truck_type, truck_location):
        self.truck_id = truck_id
        self.truck_type = truck_type
        self.truck_location = truck_location

    def getTruckID(self):
        return self.truck_id
    
    def getTruckType(self):
        return self.truck_type
    
    def getTruckLocation(self):
        return self.truck_location