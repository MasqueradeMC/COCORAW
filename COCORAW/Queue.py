class Queue:
    def __init__(self, orders=None):
        self.orders = orders or []

    def next_id(self):
        return max([o["id"] for o in self.orders], default=0) + 1

    def add(self, order):
        self.orders.append(order)

    def pending(self): #Displays the orders that are not completed in the order that they were placed
        return [o for o in self.orders if o.get("status", "Pending") != "Completed"]

    def complete(self, order):
        order["status"] = "Completed"