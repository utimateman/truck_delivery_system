import time 

class ReceiverShippingRequest:
    def __init__(self, shipment_request_for_receiver_id, receiver_id, warehouse_id, requested_trucks, requested_goods, warehouse_manager_id):
        self.shipment_request_for_receiver_id = shipment_request_for_receiver_id,
        self.receiver_id = receiver_id
        self.warehouse_id = warehouse_id
        self.delivered_trucks = requested_trucks
        self.delivered_goods = requested_goods
        self.timestamp = time.time()
        self.receiver_approval_status = "APPROVE"
        self.receiver_approval_manager_id = 12345
        self.warehouse_manager_id = warehouse_manager_id

    def getShipmentRequestForReceiverId(self):
        return self.shipment_request_for_receiver_id
    
    def getReceiverId(self):
        return self.receiver_id
    
    def getWarehouseId(self):
        return self.warehouse_id
    
    def getDeliveryTimeInterval(self):
        return self.delivery_time_interval
    
    def getDeliveredTrucks(self):
        return self.delivered_trucks
    
    def getDeliveredGoods(self):
        return self.delivered_goods
    
    def getTimestamp(self):
        return self.timestamp
    
    def getReceiverApprovalStatus(self):
        return self.receiver_approval_status
    
    def getReceiverApprovalManagerId(self):
        return self.receiver_approval_manager_id
    
    def getWarehouseManagerId(self):
        return self.warehouse_manager_id
    
