import unittest
from datetime import datetime, timedelta
import sys
import pandas as pd
import json

sys.path.insert(1, '/Users/krai/truck_delivery_system/truck_system/Components')
sys.path.insert(2, '/Users/krai/truck_delivery_system/truck_system')

from Truck import Truck
from TruckOrder import TruckOrder
from TruckTransportationPlan import TruckTransportationPlan
from WarehouseShippingRequest import WarehouseShippingRequest
from ReceiverShippingRequest import ReceiverShippingRequest
from TruckDeliverySystem import TruckDeliverySystem


class MyPOCTest(unittest.TestCase):
    def subtract_minutes_from_timestamp(self, timestamp, minutes):
        dt = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
        new_dt = dt - timedelta(minutes=minutes)
        new_timestamp = new_dt.strftime("%Y-%m-%d %H:%M:%S")
        return new_timestamp
    
    def calculate_departure_time(self, delivery_interval, truck_count, travel_time):
        # Truck Processing Time Outbound
        TPT_out = 5

        # Truck Processing Time Inbound
        TPT_in = 5

        # Calculation
        depature_time_upper_bound = self.subtract_minutes_from_timestamp(delivery_interval[1], ((TPT_in + TPT_out) * truck_count + travel_time))
        depature_time_lower_bound = self.subtract_minutes_from_timestamp(delivery_interval[0], (travel_time + (TPT_out * truck_count)))

        return [depature_time_lower_bound, depature_time_upper_bound]
    
    def is_latitude(self, value):
        return -90 <= value <= 90
    
    def is_longitude(self, value):
        return -180 <= value <= 180

    def test_normal_case(self):
        
        # test variables
        receiver_id = 1
        warehouse_id = 2
        truck_order_list = [["Box Truck", 3, "WHA1S1"], ["Flatbed Truck",3,"WHA1S2"]]

        truck_count = 0
        for i in range(len(truck_order_list)):
            truck_count += truck_order_list[i][1]
        
        delivery_time_interval = ["2010-11-04 10:00:00","2010-11-04 12:00:00"]

        travel_time = 30
        receiver_approval_manager_id = 12345
        warehouse_approval_manager_id = 23456
        
        # create WarehouseShippingRequest
        wh_ship_req= WarehouseShippingRequest(1, receiver_id, warehouse_id, delivery_time_interval, [TruckOrder(truck_order_list[0][0],truck_order_list[0][1],truck_order_list[0][2]), TruckOrder(truck_order_list[1][0],truck_order_list[1][1],truck_order_list[1][2])], ["Apple", "Banana"], receiver_approval_manager_id)
        
        # create ReceiverShippingRequest
        rc_ship_req = ReceiverShippingRequest(1, receiver_id, warehouse_id, [TruckOrder(truck_order_list[0][0],truck_order_list[0][1],truck_order_list[0][2]), TruckOrder(truck_order_list[1][0],truck_order_list[1][1],truck_order_list[1][2])], ["Apple", "Banana"], warehouse_approval_manager_id)
        
        # create TruckDeliverySystem
        tds = TruckDeliverySystem(warehouse_id, receiver_id, travel_time , [TruckOrder(truck_order_list[0][0],truck_order_list[0][1],truck_order_list[0][2]), TruckOrder(truck_order_list[1][0],truck_order_list[1][1],truck_order_list[1][2])], wh_ship_req, rc_ship_req)
        truck_plan = tds.generateDeliveryPlan()

        # formatting output
        truck_plan_list = []
        for truck_transportation_plan in truck_plan['delivery_plan']:
            truck_plan_list.append(json.loads(truck_transportation_plan.jsonVersion()))

        df = pd.DataFrame(truck_plan_list)
        print(df)

        # truck.getTruckID(),
        # truck.getTruckType(),
        # truck.getTruckLocation(),
        # driver_id,
        # self.warehouse_id,
        # self.receiver_id,
        # receiver_location,
        # receiver_lat,
        # receiver_lng,
        # truck_delivery_time_interval,
        # route_id,
        # [depature_time_lower_bound, depature_time_upper_bound],
        # self.shipping_request_for_receiver.getWarehouseManagerId(),
        # self.shipping_request_for_warehouse.getReceiverManagerId()

        # Validating Output

        # truck ID == not null
        truck_id_has_null = df['TruckID'].isnull().any()
        self.assertEqual(truck_id_has_null, False)

        # truck ID == all int
        truck_id_is_int = df['TruckID'].dtype in ['int', 'int64']
        self.assertEqual(truck_id_is_int, True)

        # truck type + count == same as truck order
        truck_order_grouped_df = df.groupby('TruckType').size().reset_index(name='Count')
        truck_order_grouped_dict = truck_order_grouped_df.set_index('TruckType')['Count'].to_dict()

        truck_order_dict = {}
        for i in range(len(truck_order_list)):
            truck_order_dict.update({truck_order_list[i][0]:truck_order_list[i][1]})

        self.assertEqual(truck_order_grouped_dict, truck_order_dict)

        # truck location == not null
        truck_location_has_null = df['TruckLocation'].isnull().any()
        self.assertEqual(truck_location_has_null, False)

        # truck location == string
        truck_location_is_string = df['TruckLocation'].dtype == 'object'
        self.assertEqual(truck_location_is_string, True)

        # driver ID == not null
        driver_id_has_null = df['DriverID'].isnull().any()
        self.assertEqual(driver_id_has_null, False)

        # driver ID == int
        driver_id_is_int = df['DriverID'].dtype in ['int', 'int64']
        self.assertEqual(driver_id_is_int, True)

        # warehouse_id == not null
        warehouse_id_has_null = df['WarehouseID'].isnull().any()
        self.assertEqual(warehouse_id_has_null, False)
        
        # warehouse_id == same 
        all_warehouse_id_value_same = df['WarehouseID'].eq(df['WarehouseID'].iloc[0]).all()
        self.assertEqual(all_warehouse_id_value_same, True)
        self.assertEqual(df['WarehouseID'].iloc[0], warehouse_id)

        # receiver_id == not null
        receiver_id_has_null = df['ReceiverID'].isnull().any()
        self.assertEqual(receiver_id_has_null, False)
        
        # receiver_id == same 
        all_receiver_id_value_same = df['ReceiverID'].eq(df['ReceiverID'].iloc[0]).all()
        self.assertEqual(all_receiver_id_value_same, True)
        self.assertEqual(df['ReceiverID'].iloc[0], receiver_id)

        print(df.columns.tolist())

        # receiver_lat == not null
        receiver_lat_has_null = df['ReceiverLatitude'].isnull().any()
        self.assertEqual(receiver_lat_has_null, False)

        # receiver_lat == [-90, 90]
        all_receiver_lat_value_same = df['ReceiverLatitude'].eq(df['ReceiverLatitude'].iloc[0]).all()
        self.assertEqual(all_receiver_lat_value_same, True)
        
        receiver_lat_is_latitude_column = df['ReceiverLatitude'].apply(self.is_latitude).all()
        self.assertEqual(receiver_lat_is_latitude_column, True)

        # receiver_lng == not null
        receiver_lng_has_null = df['ReceiverLongitude'].isnull().any()
        self.assertEqual(receiver_lng_has_null, False)

        # receiver_lng == [-180,180]
        all_receiver_lat_value_same = df['ReceiverLatitude'].eq(df['ReceiverLatitude'].iloc[0]).all()
        self.assertEqual(all_receiver_lat_value_same, True)
        
        receiver_lng_is_latitude_column = df['ReceiverLatitude'].apply(self.is_longitude).all()
        self.assertEqual(receiver_lng_is_latitude_column, True)

        # truck_delivery_time_interval == same
        delivery_time_cols = df['TruckDeliveryTimeInterval']
        delivery_time_cols_all_same = (delivery_time_cols.apply(tuple) == delivery_time_cols.apply(lambda x: tuple(x))).all()
        self.assertEqual(delivery_time_cols_all_same, True)

        self.assertEqual(delivery_time_cols.iloc[0], delivery_time_interval)
        
        # route_id == not null
        route_id_has_null = df['ReceiverLongitude'].isnull().any()
        self.assertEqual(route_id_has_null, False)

        # route_id == int
        route_id_has_null = df['DriverID'].dtype in ['int', 'int64']
        self.assertEqual(route_id_has_null, True)

        # depature_time == specify based on formula
        departure_time_cols = df['TruckDepartureTimeInterval']
        departure_time_cols_all_same = (departure_time_cols.apply(tuple) == departure_time_cols.apply(lambda x: tuple(x))).all()
        self.assertEqual(departure_time_cols_all_same, True)

        departure_time_value = self.calculate_departure_time(delivery_time_interval, truck_count, travel_time)
        self.assertEqual(departure_time_cols.iloc[0], departure_time_value)

        # shipping_request_for_receiver == null
        warehouse_approval_manager_id_is_null = df['WarehouseApprovalManagerID'].isnull().any()
        self.assertEqual(warehouse_approval_manager_id_is_null, False)

        # warehouse_approval_manager_id == same
        warehouse_approval_manager_id_value_all_same = df['WarehouseApprovalManagerID'].eq(df['WarehouseApprovalManagerID'].iloc[0]).all()
        self.assertEqual(warehouse_approval_manager_id_value_all_same, True)
        self.assertEqual(df['WarehouseApprovalManagerID'].iloc[0], warehouse_approval_manager_id)

        # shipping_request_for_warehouse == null
        receiver_approval_manager_id_has_null = df['ReceiverApprovalManagerID'].isnull().any()
        self.assertEqual(receiver_approval_manager_id_has_null, False)

        # shipping_request_for_warehouse == same
        receiver_approval_manager_id_value_all_same = df['ReceiverApprovalManagerID'].eq(df['ReceiverApprovalManagerID'].iloc[0]).all()
        self.assertEqual(receiver_approval_manager_id_value_all_same, True)
        self.assertEqual(df['ReceiverApprovalManagerID'].iloc[0], receiver_approval_manager_id)



if __name__ == '__main__':
    unittest.main()