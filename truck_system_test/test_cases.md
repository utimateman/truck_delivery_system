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
# c10: number of truck in order will NOT BE COUNT as INDIVIDUAL driver doesn't need to aware of his/her friends or required to leave as a group


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

# t75: test number of truck priority priority (3 receiver depart same time) - same departure time, same location, same types, different number - (1), (2), (3) -> PASS
# t76: test number of truck priority priority (3 receiver depart same time) - same departure time, same location, same types, different number - (3), (2), (1) -> PASS
# t77: test number of truck priority priority (3 receiver depart same time) - same departure time, same location, same types, different number - (2), (1), (3) -> PASS


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