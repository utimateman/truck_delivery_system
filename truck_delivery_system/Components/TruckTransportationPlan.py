import json

class TruckTransportationPlan:
    def __init__(self, truck_id, truck_type, truck_location, driver_id, receiver_id, receiver_location, receiver_lat, receiver_lng, truck_delivery_time_interval, route_id, truck_departure_time_interval, warehouse_approval_manager_id, receiver_approval_manager_id):
        self.truck_id = truck_id
        self.truck_type = truck_type
        self.truck_location = truck_location
        self.driver_id = driver_id
        self.receiver_id = receiver_id
        self.receiver_location = receiver_location
        self.receiver_lat = receiver_lat
        self.receiver_lng = receiver_lng
        self.truck_delivery_time_interval = truck_delivery_time_interval
        self.route_id = route_id
        self.truck_departure_time_interval = truck_departure_time_interval
        self.warehouse_approval_manager_id = warehouse_approval_manager_id
        self.receiver_approval_manager_id = receiver_approval_manager_id
    
    def getTruckId(self):
        return self.truck_id
    
    def getDriverId(self):
        return self.driver_id
    
    def getReceiverId(self):
        return self.receiver_id
    
    def getReceiverLocation(self):
        return self.receiver_location
    
    def getReceiverLat(self):
        return self.receiver_lat
    
    def getReceiverLng(self):
        return self.receiver_lng
    
    def getTruckDeliveryTimeInterval(self):
        return self.truck_delivery_time_interval
    
    def getRouteId(self):
        return self.route_id
    
    def getTruckDepartureTimeInterval(self):
        return self.truck_departure_time_interval
    
    def getEstimateArrivalTime(self):
        return self.estimate_arrival_time
    
    def getWarehouseApprovalManagerId(self):
        return self.warehouse_approval_manager_id
    
    def getReceiverApprovalManagerId(self):
        return self.receiver_approval_manager_id
    
    def printValues(self):
        print("Truck ID:", self.getTruckId())
        print("Truck Type:", self.truck_type)
        print("Truck Location:", self.truck_location)
        print("Driver ID:", self.getDriverId())
        print("Receiver ID:", self.getReceiverId())
        print("Receiver Location:", self.getReceiverLocation())
        print("Receiver Latitude:", self.getReceiverLat())
        print("Receiver Longitude:", self.getReceiverLng())
        print("Truck Delivery Time Interval:", self.getTruckDeliveryTimeInterval())
        print("Route ID:", self.getRouteId())
        print("Truck Departure Time Interval:", self.getTruckDepartureTimeInterval())
        print("Warehouse Approval Manager ID:", self.getWarehouseApprovalManagerId())
        print("Receiver Approval Manager ID:", self.getReceiverApprovalManagerId())

    def to_json(self):
        data = {
            "TruckID": self.getTruckId(),
            "TruckType": self.truck_type,
            "TruckLocation": self.truck_location,
            "DriverID": self.getDriverId(),
            "ReceiverID": self.getReceiverId(),
            "ReceiverLocation": self.getReceiverLocation(),
            "ReceiverLatitude": self.getReceiverLat(),
            "ReceiverLongitude": self.getReceiverLng(),
            "TruckDeliveryTimeInterval": self.getTruckDeliveryTimeInterval(),
            "RouteID": self.getRouteId(),
            "TruckDepartureTimeInterval": self.getTruckDepartureTimeInterval(),
            "WarehouseApprovalManagerID": self.getWarehouseApprovalManagerId(),
            "ReceiverApprovalManagerID": self.getReceiverApprovalManagerId()
        }
        return json.dumps(data)