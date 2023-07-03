import time 

class WarehouseShippingRequest:
    def __init__(self, shipment_request_for_warehouse_id, receiver_id, warehouse_id, delivery_time_interval, requested_trucks, requested_goods, receiver_manager_id):
        self.shipment_request_for_warehouse_id = shipment_request_for_warehouse_id,
        self.receiver_id = receiver_id
        self.warehouse_id = warehouse_id
        self.delivery_time_interval = delivery_time_interval
        self.requested_trucks = requested_trucks
        self.requested_goods = requested_goods
        self.timestamp = time.time()
        self.warehouse_approval_status = "APPROVE"
        self.warehouse_approval_manager_id = 12345
        self.receiver_manager_id = receiver_manager_id

    def getShipmentRequestForWarehouseId(self):
        return self.shipment_request_for_warehouse_id
    
    def getReceiverId(self):
        return self.receiver_id
    
    def getWarehouseId(self):
        return self.warehouse_id
    
    def getDeliveryTimeInterval(self):
        return self.delivery_time_interval
    
    def getRequestedTrucks(self):
        return self.requested_trucks
    
    def getRequestedGoods(self):
        return self.requested_goods
    
    def getTimestamp(self):
        return self.timestamp
    
    def getWarehouseApprovalStatus(self):
        return self.warehouse_approval_status
    
    def getWarehouseApprovalManagerId(self):
        return self.warehouse_approval_manager_id
    
    def getReceiverManagerId(self):
        return self.receiver_manager_id
    
# wh = WarehouseShippingRequest(1, 1, 1, 1, 1, 1,1 )
# print(wh.getTimestamp())