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
        # query out: warehouse_id | warehouse_manager_id | receiver_manager_id | receiver_id | travel_time
        # defined: delivery_time_interval | goods_list 
        # query + define: truck_order

        # ---- [ outputs summary ] ----
        # List of [
            # truck_id - is all positive int 
            # *** truck_queue - matches the sequence
            # *** truck_type - in total is correct e.g., 3 Box Truck, 2 Pickups
            # truck_warehouse_location - in total is correct 
            # driver_id - is all positive int
            # warehouse_id - matches input
            # receiver_id - matches input
            # receiver_location - matches receiver_id
            # receiver_lat | receiver_lng - matches receiver_id
            # truck_delivery_time_interval - matches input
            # route_id - matches route_id for warehouse-receiver
            # *** departure_time_interval - matches the calculation
            # warehouse_approval_manager_id | receiver_approval_manager_id - all positive int 
        # ]

        # ------- [ constraint ] -------
        # c1: reusing truck will not be calculated in a delivery plan
        # c2: every warehouses and receiver has an inbound/outbound processing time per truck (e.g., 3 mins/truck)
        #     which is expected to be included in  DEPARTURE INTERVAL calculation
        # c3: different parking location in the same warehouse has different priority for QUEUING SYSTEM
        # c4: different types of truck has different priority for QUEUING SYSTEM
        # c5: different departure time has different priority for QUEUING SYSTEM
        # c6: departure time for QUEUING SYSTEM is defining as departure time (lower bound) + (outbound_truck_processing_time * number of truck)
        # c7: priority of queuing factors is described as follows: departure time > location > types; 
        # c8: if departure time same, then departure time (upper bound)
        # c9: if departure time (upper bound) same, then transaction sequence (timestamp)

        # ------- [ test cases ] -------

        # ---------------------------------------------
        # invalid input
        # ---------------------------------------------
        # t1: invalid warehouse_id
        # t2: invalid warehouse_manager_id
        # t3: invalid receiver_manager_id
        # t4: invalid receiver_id
        # t5: invalid travel_time
        # t6: invalid delivery_time_interval - format, null, A2 < A1
        # t7: invalid goods_list
        # t8: invalid truck_order
        # t9: invalid WarehouseShippingRequest
        # t10: invalid ReceiverShippingRequest

        # ---------------------------------------------
        # output validation
        # ---------------------------------------------
        # t1: valid truck_id format
        # t2: valid truck_queue format
        # t3: valid truck_type format
        # t4: valid truck_warehouse_location format
        # t5: valid driver_id format
        # t6: valid warehouse_id format
        # t7: valid receiver_id format
        # t8: valid receiver_location format
        # t9: valid receiver_lat format
        # t10: valid receiver_lng format
        # t11: valid truck_delivery_time_interval format
        # t12: valid route_id format
        # t13: valid departure_time_interval format
        # t14: valid warehouse_approval_manager_id format
        # t15: valid receiver_approval_manager_id format

        # ---------------------------------------------
        # logical errors & handling
        # ---------------------------------------------
        # t1: base case - happy path, everything correct -> PASS
        
        # Departure Time 
        # t2: edge case - tightest departure time possible -> PASS
        # t3: exact overlapped case - truck exceed -> FAIL
        # t4: exact overlapped case - truck NOT exceed -> PASS
        # t5: intersect overlapped case - truck exceed -> FAIL
        # t6: intersect overlapped case - truck NOT exceed -> PASS
        # t7: subset overlapped case - truck exceed -> FAIL
        # t8: subset overlapped case - truck NOT exceed -> PASS
        # t9: multiple intersect overlapped case - truck exceed -> FAIL
        # t10: multiple intersect overlapped case - truck NOT exceed -> PASS
        
        # Truck Queuing
        # t11: test priority (2 receiver depart same time) - order by departure(upper bound), same departure time, same location, same types -> PASS
        # t12: test priority (5 receiver depart same time) - order by departure(upper bound) timestamp, same departure time, same location, same types -> PASS
        # t13: test priority (2 receiver depart same time) - order by departure(same) - order by transaction, same departure time, same location, same types -> PASS
        # t14: test priority (5 receiver depart same time) - order by departure(same) - order by transaction timestamp, same departure time, same location, same types -> PASS
        
        # - different types
        # t15: test types priority (1 types) - order by departure(upper bound), same departure time, same location, different types -> PASS
        # t16: test types priority (2 types) - same departure time, same location, different types -> PASS
        # t17: test types priority (3 types) - same departure time, same location, different types -> PASS
        # t18: test types priority (4 types) - same departure time, same location, different types -> PASS
        # t19: test types priority (2 receiver depart same time, 2 types) - same departure time, same location, different types - (A), (B) -> PASS
        # t20: test types priority (2 receiver depart same time, 2 types) - same departure time, same location, different types - (B), (A) -> PASS
        # t21: test types priority (2 receiver depart same time, 2 types) - same departure time, same location, different types - (A,B), (A) -> PASS
        # t22: test types priority (2 receiver depart same time, 2 types) - same departure time, same location, different types - (B), (A,B) -> PASS
        # t23: test types priority (2 receiver depart same time, 2 types) - same departure time, same location, different types - (B,A), (A,B) -> PASS
        # t24: test types priority (2 receiver depart same time, 3 types) - same departure time, same location, different types - (B, C), (A) -> PASS
        # t25: test types priority (2 receiver depart same time, 3 types) - same departure time, same location, different types - (B), (A, C) -> PASS
        # t26: test types priority (2 receiver depart same time, 3 types) - same departure time, same location, different types - (C), (A, B) -> PASS
        # t27: test types priority (2 receiver depart same time, 3 types) - same departure time, same location, different types - (B,C), (A,B) -> PASS
        # t28: test types priority (2 receiver depart same time, 3 types) - same departure time, same location, different types - (A,C), (A,B) -> PASS
        # t29: test types priority (2 receiver depart same time, 3 types) - same departure time, same location, different types - (B,C), (A,C) -> PASS
        # t30: test types priority (2 receiver depart same time, 3 types) - same departure time, same location, different types - (B,A,C), (C,B,A) -> PASS
        # t31: test types priority (3 receiver depart same time, 3 types) - same departure time, same location, different types - (A), (B), (C) -> PASS
        # t32: test types priority (3 receiver depart same time, 3 types) - same departure time, same location, different types - (A,B), (B,C), (A,C) -> PASS
        # t33: test types priority (3 receiver depart same time, 3 types) - same departure time, same location, different types - (C,B,A), (B,A,C), (A,B,C) -> PASS
        # t34: test types priority (4 receiver depart same time, 4 types) - same departure time, same location, different types - (A, B), (B, C), (C, D), (D, A) -> PASS
        # t35: test types priority (4 receiver depart same time, 4 types) - same departure time, same location, different types - (A, B, C), (B, C, D), (C, D, A), (D, A, B) -> PASS
        # t36: test types priority (4 receiver depart same time, 4 types) - same departure time, same location, different types - (A, B, C, D), (B, C, D, A), (C, D, A, B), (D, A, B, C) -> PASS
        # t37: test types priority (5 receiver depart same time, 3 types) - same departure time, same location, different types - (A, B, C), (A, B, C),  (A, B, C),  (A, B, C),  (A, B, C) -> PASS

        # - different location
        # t38: test location priority (2 receiver depart same time, 2 types) - same departure time, different location, same types - (A), (B) -> PASS
        # t39: test location priority (2 receiver depart same time, 2 types) - same departure time, different location, same types - (B), (A) -> PASS
        # t40: test location priority (2 receiver depart same time, 2 types) - same departure time, different location, same types - (A,B), (A) -> PASS
        # t41: test location priority (2 receiver depart same time, 2 types) - same departure time, different location, same types - (B), (A,B) -> PASS
        # t42: test location priority (2 receiver depart same time, 2 types) - same departure time, different location, same types - (B,A), (A,B) -> PASS
        # t43: test location priority (2 receiver depart same time, 3 types) - same departure time, different location, same types - (B, C), (A) -> PASS
        # t42: test location priority (2 receiver depart same time, 3 types) - same departure time, different location, same types - (B), (A, C) -> PASS
        # t44: test location priority (2 receiver depart same time, 3 types) - same departure time, different location, same types - (C), (A, B) -> PASS
        # t45: test location priority (2 receiver depart same time, 3 types) - same departure time, different location, same types - (B,C), (A,B) -> PASS
        # t46: test location priority (2 receiver depart same time, 3 types) - same departure time, different location, same types - (A,C), (A,B) -> PASS
        # t47: test location priority (2 receiver depart same time, 3 types) - same departure time, different location, same types - (B,C), (A,C) -> PASS
        # t48: test location priority (2 receiver depart same time, 3 types) - same departure time, different location, same types - (B,A,C), (C,B,A) -> PASS
        # t49: test location priority (3 receiver depart same time, 3 types) - same departure time, different location, same types - (A), (B), (C) -> PASS
        # t50: test location priority (3 receiver depart same time, 3 types) - same departure time, different location, same types - (A,B), (B,C), (A,C) -> PASS
        # t51: test location priority (3 receiver depart same time, 3 types) - same departure time, different location, same types - (C,B,A), (B,A,C), (A,B,C) -> PASS
        # t52: test location priority (4 receiver depart same time, 4 types) - same departure time, different location, same types - (A, B), (B, C), (C, D), (D, A) -> PASS
        # t53: test location priority (4 receiver depart same time, 4 types) - same departure time, different location, same types - (A, B, C), (B, C, D), (C, D, A), (D, A, B) -> PASS
        # t54: test location priority (4 receiver depart same time, 4 types) - same departure time, different location, same types - (A, B, C, D), (B, C, D, A), (C, D, A, B), (D, A, B, C) -> PASS
        # t55: test location priority (5 receiver depart same time, 3 types) - same departure time, different location, same types - (A, B, C), (A, B, C),  (A, B, C),  (A, B, C),  (A, B, C) -> PASS
        
        # - different departure time
        # t56: test departure time priority (2 receiver depart same time, 2 types) - different departure time, same location, same types - (A), (B) -> PASS
        # t57: test departure time priority (2 receiver depart same time, 2 types) - different departure time, same location, same types - (B), (A) -> PASS
        # t58: test departure time priority (2 receiver depart same time, 2 types) - different departure time, same location, same types - (A,B), (A) -> PASS
        # t59: test departure time priority (2 receiver depart same time, 2 types) - different departure time, same location, same types - (B), (A,B) -> PASS
        # t60: test departure time priority (2 receiver depart same time, 2 types) - different departure time, same location, same types - (B,A), (A,B) -> PASS
        # t61: test departure time priority (2 receiver depart same time, 3 types) - different departure time, same location, same types - (B, C), (A) -> PASS
        # t62: test departure time priority (2 receiver depart same time, 3 types) - different departure time, same location, same types - (B), (A, C) -> PASS
        # t63: test departure time priority (2 receiver depart same time, 3 types) - different departure time, same location, same types - (C), (A, B) -> PASS
        # t64: test departure time priority (2 receiver depart same time, 3 types) - different departure time, same location, same types - (B,C), (A,B) -> PASS
        # t65: test departure time priority (2 receiver depart same time, 3 types) - different departure time, same location, same types - (A,C), (A,B) -> PASS
        # t66: test departure time priority (2 receiver depart same time, 3 types) - different departure time, same location, same types - (B,C), (A,C) -> PASS
        # t67: test departure time priority (2 receiver depart same time, 3 types) - different departure time, same location, same types - (B,A,C), (C,B,A) -> PASS
        # t68: test departure time priority (3 receiver depart same time, 3 types) - different departure time, same location, same types - (A), (B), (C) -> PASS
        # t69: test departure time priority (3 receiver depart same time, 3 types) - different departure time, same location, same types - (A,B), (B,C), (A,C) -> PASS
        # t70: test departure time priority (3 receiver depart same time, 3 types) - different departure time, same location, same types - (C,B,A), (B,A,C), (A,B,C) -> PASS
        # t71: test departure time priority (4 receiver depart same time, 4 types) - different departure time, same location, same types - (A, B), (B, C), (C, D), (D, A) -> PASS
        # t72: test departure time priority (4 receiver depart same time, 4 types) - different departure time, same location, same types - (A, B, C), (B, C, D), (C, D, A), (D, A, B) -> PASS
        # t73: test departure time priority (4 receiver depart same time, 4 types) - different departure time, same location, same types - (A, B, C, D), (B, C, D, A), (C, D, A, B), (D, A, B, C) -> PASS
        # t74: test departure time priority (5 receiver depart same time, 3 types) - different departure time, same location, same types - (A, B, C), (A, B, C),  (A, B, C),  (A, B, C),  (A, B, C) -> PASS

        # - priority combination 
        # t75: test location and types priority - same departure time, different location, different types - A:(A,B), B(A,B,C) -> PASS
        # t76: test departure time and types priority - different departure time, different location, different types - A:(A,B), B(A,B,C) -> PASS
        # t77: test departure time and types location - different departure time, different location, same types - A:(A,B), B(A,B,C) -> PASS
        # t78: probably normal case... all different - different departure time, different location, different types -> PASS
        

        # ---------------------------------------------
        # random (smoking?) test
        # ---------------------------------------------
        # t79: normal random cases x [ Number of expected transaction per Day] 
        # t80: (Maybe Subset) all combinations of warehouse-receiver
        # t81: (NO) all combinations of different queuing priority; SUM(m=0, n-1)[(nCm)(n-m)r] where n = no. of truck, r = no. of receiver

        

        pass

warehouse_num =  5
warehouse_parking_range = [2,5]
truck_num_range = [3,20]
warehouse_truck_processing_time = [5, 10]
receiver_num = 3
receiver_truck_processing_time = [3, 6]

tcg = TestCaseGenerator(warehouse_num, warehouse_parking_range, truck_num_range, warehouse_truck_processing_time, receiver_num, receiver_truck_processing_time)
tcg.generatingDatabase() 
 

        