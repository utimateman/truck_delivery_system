import random
import names
import csv
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class TestCaseGenerator:
    def __init__(self, warehouse_num, warehouse_parking_range, truck_num_range, warehouse_truck_processing_time, receiver_num, receiver_truck_processing_time, delivery_time_interval_interval):
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

        self.delivery_time_interval_interval = delivery_time_interval_interval * 60 # hours to minutes

    def debuggerFunctionTruckDelivery(self, test_case_name, input, output, truck_id_list):
        print(input)
        print(output)
        print(truck_id_list)

        warehouse_row = self.warehouse_df.loc[(self.warehouse_df['warehouse_id'] == input[0])]
        warehouse_outbound_processing_time = warehouse_row['outbound_processing_time'].values[0]

        receiver_row = self.receiver_df.loc[(self.receiver_df['receiver_id'] == input[2])]
        receiver_inbound_processing_time = receiver_row['inbound_processing_time'].values[0]
        
        print("------------------------------------------------")
        print("------ [ debuggerFunctionTruckDelivery ] -------")
        print("------------------------------------------------")
        print(test_case_name)
        print("------------------------------------------------")
        print("Truck Count Input:", len(truck_id_list))
        print("Delivery Interval Input:", input[len(input)-1])
        print("wareshouse_outbound_processing_time:", warehouse_outbound_processing_time)
        print("receiver_inbound_processing_time:", receiver_inbound_processing_time)
        print("travel_time:", input[4])
        print("------------------------------------------------")
        print("Truck Count Output:", len(output))
        print("Delivery Interval Output:", output[0]['truck_delivery_time_interval'])
        print("Departure  Interval Output:", output[0]['truck_departure_time_interval'])
        print("------------------------------------------------")

        pass

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
        warehouse_manager_id_list = []

        # receiver
        receiver_id_list = []
        receiver_location_id_list = []
        receiver_inbound_processing_time = []
        receiver_outbound_processing_time = []
        receiver_manager_id_list = []

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
            warehouse_manager_id_list.append(EMPLOYEE_ID)
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
            location_id_list.append(LOCATION_ID)
            LOCATION_ID += 1
            lat, lng = self.generate_random_coordinates()
            lat_list.append(lat)
            lng_list.append(lng)

            # spawn employee
            employee_id_list.append(EMPLOYEE_ID)
            receiver_manager_id_list.append(EMPLOYEE_ID)
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
            'outbound_processing_time':warehouse_outbound_processing_time,
            'warehouse_manager_id': warehouse_manager_id_list
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
            'outbound_processing_time': receiver_outbound_processing_time,
            'receiver_manager_id': receiver_manager_id_list
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

        location_data = {
            'location_id':location_id_list,
            'location_lat':lat_list,
            'location_lng':lng_list
        }


        print(warehouse_data)
        print(receiver_data)
        print(truck_data)
  
        # Create a DataFrame from the dictionary
        self.warehouse_df = pd.DataFrame(warehouse_data)
        self.receiver_df = pd.DataFrame(receiver_data)
        self.truck_df = pd.DataFrame(truck_data)
        self.employee_df = pd.DataFrame(employee_data)
        self.route_df = pd.DataFrame(route_data)
        self.location_df = pd.DataFrame(location_data)

        # Print the DataFrame
        print(self.warehouse_df)
        print(self.receiver_df)
        print(self.truck_df)
        print(self.employee_df)
        print(self.route_df)
        print(self.location_df)

    

    def generatingTestCasesCommonInput(self, n):
        # random generate common inputs
        common_input_list = []
        for i in range(n):
            random_warehouse_row = self.warehouse_df.sample(n=1)
            print(random_warehouse_row)
            random_warehouse_id = random_warehouse_row['warehouse_id'].values[0]
            random_warehouse_manager_id = random_warehouse_row['warehouse_manager_id'].values[0]

            random_receiver_row = self.receiver_df.sample(n=1)
            print(random_receiver_row)
            random_receiver_id = random_receiver_row['receiver_id'].values[0]
            random_receiver_manager_id = random_receiver_row['receiver_manager_id'].values[0]

            route_row = self.route_df.loc[(self.route_df['location_id_depart'] == random_warehouse_id) & (self.route_df['location_id_arrive'] == random_receiver_id)]
            travel_time = route_row['travel_time'].values[0]
            goods_list = ["apple", "banana", "grape"]

            common_input_list.append({'random_warehouse_id':int(random_warehouse_id), 'random_warehouse_manager_id':int(random_warehouse_manager_id),'random_receiver_id':int(random_receiver_id), 'random_receiver_manager_id':int(random_receiver_manager_id), 'travel_time':int(travel_time),'goods_list':goods_list})
        
        return common_input_list
    
    def generatingTestCasesTruckInput(self, case, warehouse_id):
        if case == 'NORMAL':
            print("[+] - generatingTestCasesTruckInput")
            truck_of_selected_warehouse_df = self.truck_df.loc[self.truck_df['truck_warehouse_location'] == warehouse_id]
            print(truck_of_selected_warehouse_df)

            truck_count = len(truck_of_selected_warehouse_df)
            truck_sample_size = random.randint(1, truck_count)

            print("truck count:", truck_count,"|", "truck sample size:", truck_sample_size)
            sample_truck_of_selected_warehouse_df = truck_of_selected_warehouse_df.sample(n=truck_sample_size)
            print(sample_truck_of_selected_warehouse_df)

            # Group the DataFrame by truck_type and truck_parking_location, and calculate count
            grouped_sample_truck_df = sample_truck_of_selected_warehouse_df.groupby(['truck_type', 'truck_parking_location']).size().reset_index(name='truck_number')

            # Convert the grouped DataFrame to a list of dictionaries
            result = grouped_sample_truck_df.to_dict(orient='records')
            print(result)
            truck_id_list = sample_truck_of_selected_warehouse_df['truck_id'].tolist()

            print("TRUCCCCCCK SAMPLEEEE SIZEEE:", truck_sample_size)

            return result, truck_sample_size, truck_id_list
        
        elif case == 'EVERY_TRUCK':
            print("[+] - generatingTestCasesTruckInput")
            truck_of_selected_warehouse_df = self.truck_df.loc[self.truck_df['truck_warehouse_location'] == warehouse_id]
            print(truck_of_selected_warehouse_df)

            truck_count = len(truck_of_selected_warehouse_df)
            truck_sample_size = truck_count # random.randint(1, truck_count)

            print("truck count:", truck_count,"|", "truck sample size:", truck_sample_size)
            sample_truck_of_selected_warehouse_df = truck_of_selected_warehouse_df.sample(n=truck_sample_size)
            print(sample_truck_of_selected_warehouse_df)

            # Group the DataFrame by truck_type and truck_parking_location, and calculate count
            grouped_sample_truck_df = sample_truck_of_selected_warehouse_df.groupby(['truck_type', 'truck_parking_location']).size().reset_index(name='truck_number')

            # Convert the grouped DataFrame to a list of dictionaries
            result = grouped_sample_truck_df.to_dict(orient='records')
            print(result)
            truck_id_list = sample_truck_of_selected_warehouse_df['truck_id'].tolist()

            print("TRUCCCCCCK SAMPLEEEE SIZEEE:", truck_sample_size)

            return result, truck_sample_size, truck_id_list

    def generatingTestCasesTimeInput(self, case, warehouse_id, receiver_id, truck_num, travel_time=0):

        if case == 'NORMAL':
            # more than current time 1 day + no conflict of truck can't process on time for at least this order

            print("[+] - generatingTestCasesTimeInput")

            current_timestamp = datetime.now()
            delivery_timestamp_lowerbound = current_timestamp + timedelta(days=1) + timedelta(minutes=random.randint(1, self.delivery_time_interval_interval))
            formatted_delivery_timestamp_lowerbound = delivery_timestamp_lowerbound.strftime('%Y-%m-%d %H:%M:%S')

            warehouse_row = self.warehouse_df.loc[(self.warehouse_df['warehouse_id'] == warehouse_id)]
            warehouse_outbound_processing_time = warehouse_row['outbound_processing_time'].values[0]

            receiver_row = self.receiver_df.loc[(self.receiver_df['receiver_id'] == receiver_id)]
            receiver_inbound_processing_time = receiver_row['inbound_processing_time'].values[0]
            
            random_time_interval = random.randint(1, self.delivery_time_interval_interval) 
            # [ prevent ] - unable to process truck on time by the given interval
            delivery_interval =  random_time_interval +  (truck_num * (warehouse_outbound_processing_time + receiver_inbound_processing_time))
            
            delivery_interval = int(delivery_interval)
            delivery_timestamp_upperbound = delivery_timestamp_lowerbound + timedelta(minutes=delivery_interval)
            formatted_delivery_timestamp_upperbound = delivery_timestamp_upperbound.strftime('%Y-%m-%d %H:%M:%S')

          
            print("warehouse_outbound_processing_time:", warehouse_outbound_processing_time, "| receiver_inbound_processing_time:",receiver_inbound_processing_time,
                  "| truck_num:", truck_num, "| time travel:", random_time_interval)
            print("delivery_time_interval_gap:", delivery_interval)
        

            random_delivery_time_interval = [formatted_delivery_timestamp_lowerbound, formatted_delivery_timestamp_upperbound]
            print('random_delivery_time_interval:', random_delivery_time_interval)
            

            return random_delivery_time_interval

        elif case == 'FIX_DELIVERY_TIME_BASED_ON_TRUCK_PROCESSING_TIME':
            # more than current time 1 day + no conflict of truck can't process on time for at least this order

            print("[+] - generatingTestCasesTimeInput")

            warehouse_row = self.warehouse_df.loc[(self.warehouse_df['warehouse_id'] == warehouse_id)]
            warehouse_outbound_processing_time = warehouse_row['outbound_processing_time'].values[0]

            receiver_row = self.receiver_df.loc[(self.receiver_df['receiver_id'] == receiver_id)]
            receiver_inbound_processing_time = receiver_row['inbound_processing_time'].values[0]

            current_timestamp = datetime.now()
            delivery_timestamp_lowerbound = current_timestamp + timedelta(days=1) - timedelta(minutes=int((warehouse_outbound_processing_time * truck_num) + travel_time)) # delivery_time_lowerbound - ((warehouse_outbound * truck_count) + travel_time)
            formatted_delivery_timestamp_lowerbound = delivery_timestamp_lowerbound.strftime('%Y-%m-%d %H:%M:%S')

            # [ prevent ] - unable to process truck on time by the given interval
            delivery_interval =  (truck_num * (warehouse_outbound_processing_time + receiver_inbound_processing_time))
            
            delivery_interval = int(delivery_interval)
            delivery_timestamp_upperbound = delivery_timestamp_lowerbound + timedelta(minutes=delivery_interval) # delivery_time_upperbound - ((warehouse_outbound + receiver_inbound) * truck_count) + travel_time)
            formatted_delivery_timestamp_upperbound = delivery_timestamp_upperbound.strftime('%Y-%m-%d %H:%M:%S')

            print("warehouse_outbound_processing_time:", warehouse_outbound_processing_time, "| receiver_inbound_processing_time:",receiver_inbound_processing_time,
                  "| truck_num:", truck_num, "| time travel:", travel_time)
            print("delivery_time_interval_gap:", delivery_interval)
        
            fix_delivery_time_interval = [formatted_delivery_timestamp_lowerbound, formatted_delivery_timestamp_upperbound]
            print('fix_delivery_time_interval:', fix_delivery_time_interval)


            return fix_delivery_time_interval
        
        elif case == 'TIMES3_TRUCK_PROCESSING_TIME':
            # more than current time 1 day + no conflict of truck can't process on time for at least this order

            TIMES_THREE = 3
            
            print("[+] - generatingTestCasesTimeInput TIMES THREE")

            warehouse_row = self.warehouse_df.loc[(self.warehouse_df['warehouse_id'] == warehouse_id)]
            warehouse_outbound_processing_time = warehouse_row['outbound_processing_time'].values[0]

            receiver_row = self.receiver_df.loc[(self.receiver_df['receiver_id'] == receiver_id)]
            receiver_inbound_processing_time = receiver_row['inbound_processing_time'].values[0]

            current_timestamp = datetime.now()
            delivery_timestamp_lowerbound = current_timestamp + timedelta(days=1) - timedelta(minutes=int((warehouse_outbound_processing_time * truck_num) + travel_time)) # delivery_time_lowerbound - ((warehouse_outbound * truck_count) + travel_time)
            formatted_delivery_timestamp_lowerbound = delivery_timestamp_lowerbound.strftime('%Y-%m-%d %H:%M:%S')

            # [ prevent ] - unable to process truck on time by the given interval
            delivery_interval =  (truck_num * (warehouse_outbound_processing_time + receiver_inbound_processing_time))
            
            delivery_interval = int(delivery_interval) * TIMES_THREE
            delivery_timestamp_upperbound = delivery_timestamp_lowerbound + timedelta(minutes=delivery_interval) # delivery_time_upperbound - ((warehouse_outbound + receiver_inbound) * truck_count) + travel_time)
            formatted_delivery_timestamp_upperbound = delivery_timestamp_upperbound.strftime('%Y-%m-%d %H:%M:%S')

            print("warehouse_outbound_processing_time:", warehouse_outbound_processing_time, "| receiver_inbound_processing_time:",receiver_inbound_processing_time,
                  "| truck_num:", truck_num, "| time travel:", travel_time)
            print("delivery_time_interval_gap:", delivery_interval)
        
            times_three_truck_processing_time_delivery_time_interval = [formatted_delivery_timestamp_lowerbound, formatted_delivery_timestamp_upperbound]
            print('times_three_truck_processing_time_delivery_time_interval:', times_three_truck_processing_time_delivery_time_interval)

            return times_three_truck_processing_time_delivery_time_interval

    def subtract_minutes_from_timestamp(self, timestamp, minutes):
        dt = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
        new_dt = dt - timedelta(minutes=int(minutes))
        new_timestamp = new_dt.strftime("%Y-%m-%d %H:%M:%S")
        return new_timestamp
    
    def generatingOutputDepartureTime(self, delivery_time_interval, warehouse_id, receiver_id, travel_time, truck_count, case):
        print("[+] - generatingOutputDepartureTime")
        print("OUTPUT TRUCK COUNTTTTTT:",truck_count)
        if case == 'NORMAL':
            warehouse_row = self.warehouse_df.loc[(self.warehouse_df['warehouse_id'] == warehouse_id)]
            warehouse_outbound_processing_time = warehouse_row['outbound_processing_time'].values[0]

            receiver_row = self.receiver_df.loc[(self.receiver_df['receiver_id'] == receiver_id)]
            receiver_inbound_processing_time = receiver_row['inbound_processing_time'].values[0]

            depature_time_upper_bound = self.subtract_minutes_from_timestamp(delivery_time_interval[1], ((warehouse_outbound_processing_time + receiver_inbound_processing_time) * truck_count + travel_time))
            depature_time_lower_bound = self.subtract_minutes_from_timestamp(delivery_time_interval[0], (travel_time + (warehouse_outbound_processing_time * truck_count)))

            departure_time_interval = [depature_time_lower_bound, depature_time_upper_bound]

            print('delivery_time_interval:', delivery_time_interval, '| travel_time:', travel_time)
            print('truck out wh:', warehouse_outbound_processing_time, '| truck in rc:', receiver_inbound_processing_time, '| truck count:', truck_count)
            print('departure_time_interval:', departure_time_interval)

            return departure_time_interval
        
        elif case == 'TIMES3_TRUCK_PROCESSING_TIME':
            # TIMESTHREE = 3
            # truck_count = truck_count * TIMESTHREE
            warehouse_row = self.warehouse_df.loc[(self.warehouse_df['warehouse_id'] == warehouse_id)]
            warehouse_outbound_processing_time = warehouse_row['outbound_processing_time'].values[0]

            receiver_row = self.receiver_df.loc[(self.receiver_df['receiver_id'] == receiver_id)]
            receiver_inbound_processing_time = receiver_row['inbound_processing_time'].values[0]

            depature_time_upper_bound = self.subtract_minutes_from_timestamp(delivery_time_interval[1], ((warehouse_outbound_processing_time + receiver_inbound_processing_time) * truck_count + travel_time))
            depature_time_lower_bound = self.subtract_minutes_from_timestamp(delivery_time_interval[0], (travel_time + (warehouse_outbound_processing_time * truck_count)))

            departure_time_interval = [depature_time_lower_bound, depature_time_upper_bound]

            print('delivery_time_interval:', delivery_time_interval, '| travel_time:', travel_time)
            print('truck out wh:', warehouse_outbound_processing_time, '| truck in rc:', receiver_inbound_processing_time, '| truck count:', truck_count)
            print('departure_time_interval:', departure_time_interval)

            return departure_time_interval

    

    def generatingOutput(self, input_list, truck_id_list, case):
        
        # ---- [ outputs summary ] ----
        # List of [
            # truck_id | truck_queue | truck_type | truck_warehouse_location | truck_parking_location | driver_id | warehouse_id 
            # receiver_id | receiver_location | receiver_lat | receiver_lng 
            # truck_delivery_time_interval | route_id | truck_departure_time_interval 
            # warehouse_approval_manager_id | receiver_approval_manager_id 
        # ]

        # ---- [ input I have ] ----
        # [
        #         [0] - common_input_list['random_warehouse_id'], [1] - common_input_list['random_warehouse_manager_id'], 
        #         [2] - common_input_list['random_receiver_id'], [3] - common_input_list['random_receiver_manager_id'],
        #         [4] - common_input_list['travel_time'], [5] - common_input_list['goods_list'], 
        #         [6] - random_truck_input, [7] - random_delivery_time_interval,
        # ]

        print("[+] - begin generationgOutput")
        output_selected_truck = self.truck_df[self.truck_df['truck_id'].isin(truck_id_list)]
        print("BUDUDSUF",output_selected_truck)
        # output_selected_truck = self.truck_df.loc[self.truck_df['truck_warehouse_location'] == input_list[0]]
        output_queued_truck = output_selected_truck.sort_values(by=['truck_parking_location', 'truck_priority', 'truck_id'], ascending=True)

        # Duplicate column change name
        output_queued_truck['drive_id'] = output_queued_truck['truck_id']

        # Create a new column with the same size as the number of rows
        output_queued_truck['warehouse_id'] = input_list[0] * output_queued_truck.shape[0]
        output_queued_truck['receiver_id'] = input_list[2] * output_queued_truck.shape[0]
        
        output_location_id = self.receiver_df.loc[self.receiver_df['receiver_id'] == input_list[2], 'location_id'].values[0]
        output_queued_truck['receiver_location'] = [output_location_id] * output_queued_truck.shape[0]
        

        output_receiver_lat = self.location_df.loc[self.location_df['location_id'] == output_location_id, 'location_lat'].values[0]
        output_receiver_lng = self.location_df.loc[self.location_df['location_id'] == output_location_id, 'location_lng'].values[0]
        output_queued_truck['receiver_lat'] = [output_receiver_lat] * output_queued_truck.shape[0]
        output_queued_truck['receiver_lng'] = [output_receiver_lng] * output_queued_truck.shape[0]


        output_queued_truck['truck_delivery_time_interval'] = [input_list[7]] * len(output_queued_truck)

        
        output_route_id = self.route_df.loc[(self.route_df['location_id_depart'] == input_list[0]) & (self.route_df['location_id_arrive'] == input_list[2]), 'route_id'].values[0]
        output_queued_truck['route_id'] = output_route_id * output_queued_truck.shape[0]

        if case == 'NORMAL':
            # [ SERIOUS BUG FIX ] - Number of Departure Truck and Input Truck
            departure_time_interval = self.generatingOutputDepartureTime(input_list[7], input_list[0], input_list[2], input_list[4], len(output_queued_truck), case='TIMES3_TRUCK_PROCESSING_TIME')
        elif case == 'TIMES3_TRUCK_PROCESSING_TIME':
            departure_time_interval = self.generatingOutputDepartureTime(input_list[7], input_list[0], input_list[2], input_list[4], len(output_queued_truck), case='TIMES3_TRUCK_PROCESSING_TIME')
        output_queued_truck['truck_departure_time_interval'] = [departure_time_interval] * len(output_queued_truck)

        output_queued_truck['warehouse_approval_manager_id'] = [input_list[1]] * output_queued_truck.shape[0]
        output_queued_truck['receiver_approval_manager_id'] = [input_list[3]] * output_queued_truck.shape[0]

        print(output_queued_truck)
        
        output_queued_truck_list = output_queued_truck.to_dict(orient='records')
        return output_queued_truck_list


    def generatingLogicalTestCase1(self):
        # [ t1: base case ] - happy path, everything correct -> PASS

        common_input_list = self.generatingTestCasesCommonInput(1)
        common_input_list = common_input_list[0]

        random_truck_input, total_truck_count, truck_id_list = self.generatingTestCasesTruckInput(case='NORMAL', warehouse_id=common_input_list['random_warehouse_id'])
        random_delivery_time_interval = self.generatingTestCasesTimeInput(case='NORMAL', warehouse_id=common_input_list['random_warehouse_id'], receiver_id=common_input_list['random_receiver_id'], truck_num=total_truck_count)

        test_case_input = [
                common_input_list['random_warehouse_id'], common_input_list['random_warehouse_manager_id'], 
                common_input_list['random_receiver_id'], common_input_list['random_receiver_manager_id'],
                common_input_list['travel_time'], common_input_list['goods_list'], random_truck_input, random_delivery_time_interval,
        ]

        test_case_output = self.generatingOutput(test_case_input, truck_id_list, case='NORMAL')
        t1_test_case = []
        t1_test_case.append(['t1','[ t1: base case ] - happy path, everything correct -> PASS'] + test_case_input + [test_case_output])

        # self.debuggerFunctionTruckDelivery('[ t1: base case ] - happy path, everything correct -> PASS',test_case_input, test_case_output, truck_id_list)

        return t1_test_case

    def generatingLogicalTestCase2(self):
        common_input_list = self.generatingTestCasesCommonInput(1)
        common_input_list = common_input_list[0]

        random_truck_input, total_truck_count, truck_id_list = self.generatingTestCasesTruckInput(case='NORMAL', warehouse_id=common_input_list['random_warehouse_id'])
        print(common_input_list)
        random_delivery_time_interval = self.generatingTestCasesTimeInput(case='FIX_DELIVERY_TIME_BASED_ON_TRUCK_PROCESSING_TIME', warehouse_id=common_input_list['random_warehouse_id'], receiver_id=common_input_list['random_receiver_id'], truck_num=total_truck_count, travel_time=common_input_list['travel_time'])


        test_case_input = [
                common_input_list['random_warehouse_id'], common_input_list['random_warehouse_manager_id'], 
                common_input_list['random_receiver_id'], common_input_list['random_receiver_manager_id'],
                common_input_list['travel_time'], common_input_list['goods_list'], random_truck_input, random_delivery_time_interval,
        ]

        test_case_output = self.generatingOutput(test_case_input, truck_id_list, case='NORMAL')
        t2_test_case = []
        t2_test_case.append(['t2','[ t2: edge case ] - tightest departure time possible -> PASS'] + test_case_input + [test_case_output])

        self.debuggerFunctionTruckDelivery('[ t2: edge case ] - tightest departure time possible -> PASS',test_case_input, test_case_output, truck_id_list)

        return t2_test_case
    
    def generatingLogicalTestCase3(self):
        common_input_list = self.generatingTestCasesCommonInput(1)
        common_input_list = common_input_list[0]

        random_truck_input, total_truck_count, truck_id_list = self.generatingTestCasesTruckInput(case='NORMAL', warehouse_id=common_input_list['random_warehouse_id'])
        print(common_input_list)
        random_delivery_time_interval = self.generatingTestCasesTimeInput(case='FIX_DELIVERY_TIME_BASED_ON_TRUCK_PROCESSING_TIME', warehouse_id=common_input_list['random_warehouse_id'], receiver_id=common_input_list['random_receiver_id'], truck_num=total_truck_count, travel_time=common_input_list['travel_time'])


        test_case_input = [
                common_input_list['random_warehouse_id'], common_input_list['random_warehouse_manager_id'], 
                common_input_list['random_receiver_id'], common_input_list['random_receiver_manager_id'],
                common_input_list['travel_time'], common_input_list['goods_list'], random_truck_input, random_delivery_time_interval,
        ]

        test_case_output_1 = self.generatingOutput(test_case_input, truck_id_list, case='NORMAL')
        test_case_output_2 = self.generatingOutput(test_case_input, truck_id_list, case='NORMAL')

        t3_test_case = []
        t3_test_case.append(['t3'] + ['[ t3: exact overlapped case ] - truck exceed -> FAIL: second request exceed'] + test_case_input + [test_case_output_1])
        t3_test_case.append(['t3'] + ['[ t3: exact overlapped case ] - truck exceed -> FAIL: second request exceed'] + test_case_input + [{"error_message","truck processing time won't make it"}])

        self.debuggerFunctionTruckDelivery('[ t3: exact overlapped case ] - truck exceed -> FAIL: second request exceed',test_case_input, test_case_output_1, truck_id_list)

        return t3_test_case

    def generatingLogicalTestCase4(self):
        common_input_list = self.generatingTestCasesCommonInput(1)
        common_input_list = common_input_list[0]

        random_truck_input, total_truck_count, truck_id_list = self.generatingTestCasesTruckInput(case='NORMAL', warehouse_id=common_input_list['random_warehouse_id'])
        print(common_input_list)
        print("RANDOM TRUCK INPUT:",random_truck_input)
        random_delivery_time_interval = self.generatingTestCasesTimeInput(case='TIMES3_TRUCK_PROCESSING_TIME', warehouse_id=common_input_list['random_warehouse_id'], receiver_id=common_input_list['random_receiver_id'], truck_num=total_truck_count, travel_time=common_input_list['travel_time'])


        test_case_input = [
                common_input_list['random_warehouse_id'], common_input_list['random_warehouse_manager_id'], 
                common_input_list['random_receiver_id'], common_input_list['random_receiver_manager_id'],
                common_input_list['travel_time'], common_input_list['goods_list'], random_truck_input, random_delivery_time_interval,
        ]


        test_case_output_1 = self.generatingOutput(test_case_input, truck_id_list, case='NORMAL')
        test_case_output_2 = self.generatingOutput(test_case_input, truck_id_list, case='NORMAL')

        t4_test_case = []
        t4_test_case.append(['t4'] + ['[ t4: exact overlapped case ] - truck NOT exceed -> PASS'] + test_case_input + [test_case_output_1])
        t4_test_case.append(['t4'] + ['[ t4: exact overlapped case ] - truck NOT exceed -> PASS'] + test_case_input + [test_case_output_2])

        self.debuggerFunctionTruckDelivery('[ t4: exact overlapped case ] - truck NOT exceed -> PASS',test_case_input, test_case_output_1, truck_id_list)
    def generatingTestCases(self):

        '''
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
            # truck_parking_location - is correct
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
        # c7: priority of queuing factors is described as follows: departure time > location > types > transaction sequence (timestamp) > truck_ID; 
        # c8: if departure time same, then departure time (upper bound)
        # c9: is NOT checking driver's management e.g., same driver assign to 2 truck at the same time
  

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
        # t11: test departure upper bound priority (2 receiver depart same time) - order by departure(upper bound), same departure time, same location, same types -> PASS
        # t12: test departure upper bound priority (5 receiver depart same time) - order by departure(upper bound) timestamp, same departure time, same location, same types -> PASS
        # t13: test transaction sequence priority (2 receiver depart same time) - order by departure(same) - order by transaction sequence, same departure time, same location, same types -> PASS
        # t14: test transaction sequence priority (5 receiver depart same time) - order by departure(same) - order by transaction sequence timestamp, same departure time, same location, same types -> PASS
        
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

        # - miscellenous
        # t75: test order 1 truck

        # - priority combination 
        # t75: test location and types priority - same departure time, different location, different types - A:(A,B), B(A,B,C) -> PASS
        # t76: test departure time and types priority - different departure time, different location, different types - A:(A,B), B(A,B,C) -> PASS
        # t77: test departure time and types location - different departure time, different location, same types - A:(A,B), B(A,B,C) -> PASS
        # t78: probably normal case... all different - different departure time, different location, different types -> PASS
        # txx: [ DONT FORGET ] truck exceed capacity

        # ---------------------------------------------
        # random (smoking?) test
        # ---------------------------------------------
        # t79: normal random cases x [ Number of expected transaction per Day] 
        # t80: (Maybe Subset) all combinations of warehouse-receiver
        # t81: (NO) all combinations of different queuing priority; SUM(m=0, n-1)[(nCm)(n-m)r] where n = no. of truck, r = no. of receiver
        '''


        # ---- [ inputs summary ] ----
        # query out: warehouse_id | warehouse_manager_id | receiver_manager_id | receiver_id | travel_time
        # defined: goods_list 
        # query + define: truck_order | delivery_time_interval

        # ---- [ outputs summary ] ----
        # List of [
            # truck_id | truck_queue | truck_type | truck_warehouse_location | truck_parking_location | driver_id | warehouse_id 
            # receiver_id | receiver_location | receiver_lat | receiver_lng 
            # truck_delivery_time_interval | route_id | truck_departure_time_interval 
            # warehouse_approval_manager_id | receiver_approval_manager_id 
        # ]

        # [ t1: base case ] - happy path, everything correct -> PASS
        t1_test_case = self.generatingLogicalTestCase1()

        # [ t2: edge case ] - tightest departure time possible -> PASS
        t2_test_case = self.generatingLogicalTestCase2()

        # [ t3: exact overlapped case ] - truck exceed -> FAIL: second request exceed
        t3_test_case = self.generatingLogicalTestCase3()

        # [ t4: exact overlapped case ] - truck NOT exceed -> PASS   # tricky!
        t4_test_case = self.generatingLogicalTestCase4()
   

        # # [ Combine and Export All Test Cases ]
        # all_test_cases = [
        #     t1_test_case,
        #     t2_test_case,
        #     t3_test_case, 
        #     t4_test_case
        # ]

        # self.exportCSV(all_test_cases)

    def exportCSV(self, all_test_cases):
        for test_case in all_test_cases:
            for row in test_case:
                with open('/Users/krai/truck_delivery_system/truck_system_test/example_test_cases/testcase1.csv', 'a', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    # print("ROW TO WRITE:\n",row)
                    writer.writerows([row])


warehouse_num =  5
warehouse_parking_range = [2,5]
truck_num_range = [3,20]
warehouse_truck_processing_time = [5, 10]
receiver_num = 3
receiver_truck_processing_time = [3, 6]
delivery_time_interval_interval = 3



tcg = TestCaseGenerator(warehouse_num, warehouse_parking_range, truck_num_range, warehouse_truck_processing_time, receiver_num, receiver_truck_processing_time, delivery_time_interval_interval)
tcg.generatingDatabase() 
tcg.generatingTestCases()
 

        