
import sys
sys.path.insert(1, '/Users/krai/truck_delivery_system/truck_delivery_system/Components')

from Truck import Truck
from TruckOrder import TruckOrder
from TruckTransportationPlan import TruckTransportationPlan
from WarehouseShippingRequest import WarehouseShippingRequest
from ReceiverShippingRequest import ReceiverShippingRequest

from datetime import datetime, timedelta



class TruckDeliverySystem:
    def __init__(self, warehouse_id, receiver_id, travel_time, truck_info, shipping_request_for_warehouse, shipping_request_for_receiver):
        
        # non-negative integer - example:  12345
        self.warehouse_id = warehouse_id
        
        # non-negative integer - example:  12345
        self.receiver_id = receiver_id

        # HH:MM:SS - example: 02:00:15 
        self.travel_time = travel_time
        
        # TruckOrder: object
            # truck_type
            # number_of_truck
            # truck_location
        # list[TruckOrder] - example: self.truck_info = { 
        # "truck_order_1":{
        #     "truck_type": "box_truck"
        #     "number_of_truck": 3
        #     "truck_location": warehouse_A_section_1    
        # }, {...}, {...}, {...}
        self.truck_info = truck_info
        
        # WarehouseShippingRequest: object
            #  shipment_request_for_warehouse_id: int,
            #  receiver_id: int,
            #  warehouse_id: int,
            #  delivery_time_interval: list[time],
            #  requested_trucks: list[truck],
            #  requested_goods: list[good],
            #  timestamp: time,
            #  warehouse_approval_status: str,
            #  warehouse_approval_manager_id: int,
            #  receiver_manager_id: int
        self.shipping_request_for_warehouse = shipping_request_for_warehouse


        # ReceiverShippingRequest: object
            #  shipment_request_for_receiver_id: int,
            #  receiver_id: int,
            #  warehouse_id: int,
            #  requested_trucks: list[truck],
            #  requested_goods: list[good],
            #  timestamp: time,
            #  receiver_approval_status: str,
            #  receiver_approval_manager_id: int,
            #  warehouse_manager_id: int
        self.shipping_request_for_receiver = shipping_request_for_receiver


        # Truck Processing Time Outbound
        self.TPT_out = 5

        # Truck Processing Time Inbound
        self.TPT_in = 5

    def subtract_minutes_from_timestamp(self, timestamp, minutes):
        dt = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
        new_dt = dt - timedelta(minutes=minutes)
        new_timestamp = new_dt.strftime("%Y-%m-%d %H:%M:%S")
        return new_timestamp
    
    def generateDeliveryPlan(self):

        # Get Truck Values
        truck_assigned_id = 1
        truck_list = []
        for truck_order in self.truck_info:
            no_of_truck = truck_order.getNumberOfTruck()
            truck_type =  truck_order.getTruckType()
            truck_location = truck_order.getTruckLocation()
            for i in range (no_of_truck):
                truck_list.append(Truck(truck_assigned_id, truck_type, truck_location))
                truck_assigned_id += 1

        
        # Get Receiver Location
        receiver_location = "Receiver A"
        receiver_lat = 45.5678
        receiver_lng = 123.2341

        # Get Route Values
        # query from receiver vs warehouse table
        route_id = 1

        # Generating Departure Time
        truck_delivery_time_interval = self.shipping_request_for_warehouse.getDeliveryTimeInterval()
        depature_time_upper_bound = self.subtract_minutes_from_timestamp(truck_delivery_time_interval[1], ((self.TPT_in + self.TPT_out) * len(truck_list) + self.travel_time))
        depature_time_lower_bound = self.subtract_minutes_from_timestamp(truck_delivery_time_interval[0], (self.travel_time + (self.TPT_out* len(truck_list))))

        #    "delivery_plan": [
            # {
            #     truck_id: int,
            #     truck_type: str,
            #     truck_location: str,
            #     driver_id: int,
            #     receiver_id: int,
            #     receiver_location: str, 
            #     receiver_lat: float,
            #     receiver_lng: float,
            #     truck_delivery_time_interval,
            #     route_id: int,
            #     truck_depature_time_interval: list[time],
            #     warehouse_approval_manager_id: int,
            #     receiver_approval_manager_id: int
            # }, {...}, {...}, {...}
        # ]"

        truck_delivery_plan = []
        driver_id = 1
        for truck in truck_list:
            temp_ttp = TruckTransportationPlan(
                truck.getTruckID(),
                truck.getTruckType(),
                truck.getTruckLocation(),
                driver_id,
                self.warehouse_id,
                self.receiver_id,
                receiver_location,
                receiver_lat,
                receiver_lng,
                truck_delivery_time_interval,
                route_id,
                [depature_time_lower_bound, depature_time_upper_bound],
                self.shipping_request_for_receiver.getWarehouseManagerId(),
                self.shipping_request_for_warehouse.getReceiverManagerId()
                )
            
            truck_delivery_plan.append(temp_ttp)
            driver_id += 1

            
   
        return {"delivery_plan":truck_delivery_plan}


# t = Truck(1,"dudu","warehouseA")
# print(t.getTruckType())


# "{
#  receiver_id: int,
#  warehouse_id: int,
#  delivery_time_interval: list[time],
#  requested_trucks: list[truck],
#  requested_goods: list[good],
#  receiver_manager_id: int
# }"
wh_ship_req= WarehouseShippingRequest(1,1,2, ["2010-11-04 10:00:00","2010-11-04 12:00:00"], [TruckOrder("Box Truck",3,"WHA1S1"), TruckOrder("Flatbed Truck",3,"WHA1S2")], ["Apple", "Banana"], 12345)

# "{
#  warehouse_id: int,
#  receiver_id: int,
#  delivered_trucks: list[truck],
#  delivered_goods: list[good],
#  warehouse_manager_id: int
# }"
rc_ship_req = ReceiverShippingRequest(1,1, 2, [TruckOrder("Box Truck",3,"WHA1S1"), TruckOrder("Flatbed Truck",3,"WHA1S2")], ["Apple", "Banana"], 23456)


# "{
#  warehouse_id: int,
#  receiver_id: int,
#  travel_time: list[time],
#  truck_info: dict[TruckOrder],
#  shipping_request_for_warehouse: object (WarehouseShippingRequest),
#  shipping_request_for_receiver: object (ReceiverShippingRequest)
# }"
tds = TruckDeliverySystem(2, 1, 30, [TruckOrder("Box Truck",3,"WHA1S1"), TruckOrder("Flatbed Truck",3,"WHA1S2")], wh_ship_req, rc_ship_req)
truck_plan = tds.generateDeliveryPlan()
for truck in truck_plan['delivery_plan']:
    truck.printValues()
    print("\n")