import random
import names
import pandas as pd

class TestCaseGenerator:
    def __init__(self, warehouse_num, warehouse_parking_range, truck_num_range, warehouse_truck_processing_time, receiver_num, receiver_truck_processing_time):
        # Inputs for Generator

        # number of warehouse: int
        # range of number of parking in warehouse: [int:int]
        # range of truck in warehouse: [int:int]
        # range of inbound/outbound processing time: [int:int]

        # number of receiver: int
        # range of inbound/outbound processing time: [int:int]

        self.warehouse_num = warehouse_num
        self.warehouse_parking_range = warehouse_parking_range
        self.truck_num_range = truck_num_range
        self.warehouse_truck_processing_time = warehouse_truck_processing_time

        self.receiver_num = receiver_num
        self.receiver_truck_processing_time = receiver_truck_processing_time

    def generate_random_coordinates(self):
        # Generate a random latitude between -90 and 90
        latitude = random.uniform(-90, 90)
        
        # Generate a random longitude between -180 and 180
        longitude = random.uniform(-180, 180)
        
        return latitude, longitude

    def generatingDatabase(self):

        # ----- [ Database Design ] -----
        # Truck
        # truck_id | truck_type | truck_warehouse_location (location priority: int) | truck_parking_location | truck_priority


        # Warehouse
        # warehouse_id | location_id | warehouse_parklot_num | truck_capacity | inbound_processing_time | outbound_processing_time

        # Receiver
        # receiver_id | location_id | inbound_processing_time | outbound_processing_time

        # Employee
        # employee_id | name | position (driver/warhouse_manager/receiver_manager) | warehouse_id | receiver_id

        # Location
        # location_id | location_lat | location_lng 

        # Route
        # route_id | location_id_depart | location_id_arrive | travel_time | checkpoints 
         
        
        # ----- [ Initialize Variables ] -----
        # warehouse
        warehouse_id_list = []
        warehouse_location_id_list = []
        warehouse_parklot_num_list = []
        truck_capacity_list = []
        warehouse_inbound_processing_time = []
        warehouse_outbound_processing_time = []

        # receiver
        receiver_id_list = []
        receiver_location_id_list = []
        receiver_inbound_processing_time = []
        receiver_outbound_processing_time = []

        # location
        LOCATION_ID = 1
        location_id_list = []
        lat_list = []
        lng_list = []
        

        # truck
        TRUCK_ID = 1
        TRUCK_TYPES = ["Box Truck", "Flatbed Truck", "tractor Trailers", "Pickups"]
        TRUCK_PRIORITY = [4,3,2,1] # 4 = highest, 1 = lowest
        truck_id_list = []
        truck_type_list = []
        truck_priority_list = []
        truck_warehouse_location_list = []
        truck_parking_location_list = []


        # employee
        EMPLOYEE_ID = 1
        employee_id_list = []
        employee_name_list = []
        employee_position_list = []
        employee_warehouse_id_list = []
        employee_receiver_id_list = []

        # route
        ROUTE_ID = 1
        route_id_list = []
        location_id_depart = []
        location_id_arrive = []
        TRAVEL_TIME_RANGE = [30,300]
        travel_time_list = []
        checkpoints_list = []

        # ----- [ Spawn Warehouse and Friends ] -----
        for i in range(self.warehouse_num):
            # spawn warehouse_id
            WAREHOUSE_ID = i + 1
            warehouse_id_list.append(WAREHOUSE_ID)

            # spawn location
            warehouse_location_id_list.append(LOCATION_ID)
            LOCATION_ID += 1
            location_id_list.append(WAREHOUSE_ID)
            lat, lng = self.generate_random_coordinates()
            lat_list.append(lat)
            lng_list.append(lng)

            # spawn warehouse parklot
            warehouse_parklot_num = random.randint(self.warehouse_parking_range[0], self.warehouse_parking_range[1])
            warehouse_parklot_num_list.append(warehouse_parklot_num)

            # spawn truck
            truck_capacity = random.randint(self.truck_num_range[0], self.truck_num_range[1])
            truck_capacity_list.append(truck_capacity)

            for i in range(truck_capacity):
                truck_id_list.append(TRUCK_ID)
                truck_type_index = random.randint(0,len(TRUCK_TYPES)-1)
                truck_type_list.append(TRUCK_TYPES[truck_type_index])
                truck_priority_list.append(TRUCK_PRIORITY[truck_type_index])
                truck_warehouse_location_list.append(WAREHOUSE_ID)
                truck_parking_location_list.append(random.randint(1,warehouse_parklot_num))
                TRUCK_ID += 1

                # spawn driver
                employee_id_list.append(EMPLOYEE_ID)
                EMPLOYEE_ID += 1
                employee_name_list.append(names.get_full_name())
                employee_position_list.append('driver')
                employee_warehouse_id_list.append(WAREHOUSE_ID)
                employee_receiver_id_list.append(None)

                

            # spawn truck processing time for warehouse
            warehouse_inbound_processing_time.append(random.randint(1, self.warehouse_truck_processing_time[0]))
            warehouse_outbound_processing_time.append(random.randint(1, self.warehouse_truck_processing_time[1]))

            # spawn employee
            employee_id_list.append(EMPLOYEE_ID)
            EMPLOYEE_ID += 1
            employee_name_list.append(names.get_full_name())
            employee_position_list.append('warehouse_manager')
            employee_warehouse_id_list.append(WAREHOUSE_ID)
            employee_receiver_id_list.append(None)
            
        # ----- [ Spawn Receiver and Friends ] -----
        for i in range(self.receiver_num):
            # spawn receiver_id
            RECEIVER_ID = i + 1
            receiver_id_list.append(RECEIVER_ID)
            receiver_inbound_processing_time.append(random.randint(1, self.receiver_truck_processing_time[0]))
            receiver_outbound_processing_time.append(random.randint(1, self.receiver_truck_processing_time[1]))

            # spawn location
            receiver_location_id_list.append(LOCATION_ID)
            LOCATION_ID += 1
            location_id_list.append(RECEIVER_ID)
            lat, lng = self.generate_random_coordinates()
            lat_list.append(lat)
            lng_list.append(lng)

            # spawn employee
            employee_id_list.append(EMPLOYEE_ID)
            EMPLOYEE_ID += 1
            employee_name_list.append(names.get_full_name())
            employee_position_list.append('receiver_manager')
            employee_warehouse_id_list.append(None)
            employee_receiver_id_list.append(RECEIVER_ID)


        # ----- [ Spawn Route ] ------
        for i in range(self.warehouse_num):
            for j in range(self.receiver_num):
                route_id_list.append(ROUTE_ID)
                ROUTE_ID += 1
                location_id_depart.append(i+1)
                location_id_arrive.append(j+1)
                travel_time = random.randint(30,300)
                travel_time_list.append(travel_time)

                # route_id_list.append(ROUTE_ID)
                # ROUTE_ID += 1
                # location_id_depart.append(j+1)
                # location_id_arrive.append(i+1)
                # travel_time = random.randint(30,300)
                # travel_time_list.append(travel_time)

        
        # ----- [ Generate Pandas Dataframes ] -----
        warehouse_data = {
            'warehouse_id':warehouse_id_list,
            'location_id':warehouse_location_id_list,
            'warehouse_parklot_num': warehouse_parklot_num_list, 
            'truck_capacity':truck_capacity_list,
            'inbound_processing_time':warehouse_inbound_processing_time,
            'outbound_processing_time':warehouse_outbound_processing_time
        }


        truck_data = {
            'truck_id':truck_id_list,
            'truck_type':truck_type_list,
            'truck_warehouse_location':truck_warehouse_location_list,
            'truck_parking_location': truck_parking_location_list,
            'truck_priority':truck_priority_list
        }
        
        receiver_data = {
            'receiver_id': receiver_id_list,
            'location_id': receiver_location_id_list,
            'inbound_processing_time': receiver_inbound_processing_time,
            'outbound_processing_time': receiver_outbound_processing_time
        }

        employee_data = {
            'employee_id': employee_id_list,
            'name': employee_name_list,
            'position': employee_position_list,
            'warehouse_id': employee_warehouse_id_list,
            'receiver_id': employee_receiver_id_list
        }

        route_data = {
            'route_id': route_id_list,
            'location_id_depart': location_id_depart,
            'location_id_arrive': location_id_arrive,
            'travel_time': travel_time_list,
            'checkpoints': None
        }

        print(warehouse_data)
        print(receiver_data)
        print(truck_data)
  
        # Create a DataFrame from the dictionary
        warehouse_df = pd.DataFrame(warehouse_data)
        receiver_df = pd.DataFrame(receiver_data)
        truck_df = pd.DataFrame(truck_data)
        employee_df = pd.DataFrame(employee_data)
        route_df = pd.DataFrame(route_data)

        # Print the DataFrame
        print(warehouse_df)
        print(receiver_df)
        print(truck_df)
        print(employee_df)
        print(route_df)


    def generatingTestCases(self):

        # ---- [ create WarehouseShippingRequest ] ----
        # wh_ship_req = WarehouseShippingRequest(
            # warehouse_shipping_request_id, 
            # receiver_id, 
            # warehouse_id, 
            # delivery_time_interval, 
            # truck_order: list[TruckOrder],
            # goods_list: list[string], 
            # receiver_approval_manager_id
        # )

        
        # ---- [ create ReceiverShippingRequest ] ----
        # rc_ship_req = ReceiverShippingRequest(
            # receiver_shipping_request_id, 
            # receiver_id, 
            # warehouse_id, 
            # truck_order: list[TruckOrder], 
            # goods_list: list[string], 
            # warehouse_approval_manager_id
        # )
        
        # ---- [ create TruckDeliverySystem ] ----
        # tds = TruckDeliverySystem(
            # warehouse_id, 
            # receiver_id, 
            # travel_time , 
            # truck_order: list[TruckOrder],
            # wh_ship_req, 
            # rc_ship_req
        # )

        # ---- [ inputs summary ] ----
        # query out: warehouse_id | warehouse_approval_manager_id | receiver_approval_manager_id | receiver_id | travel_time
        # defined: delivery_time_interval | goods_list 
        # query + define: truck_order

        # ---- [ outputs summary ] ----
        # truck_id | truck_type | truck_warehouse_location | driver_id |
        # truck.getTruckID(),
                #         truck.getTruckType(),
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
        pass

warehouse_num =  5
warehouse_parking_range = [2,5]
truck_num_range = [3,20]
warehouse_truck_processing_time = [5, 10]
receiver_num = 3
receiver_truck_processing_time = [3, 6]

tcg = TestCaseGenerator(warehouse_num, warehouse_parking_range, truck_num_range, warehouse_truck_processing_time, receiver_num, receiver_truck_processing_time)
tcg.generatingDatabase() 
 

        