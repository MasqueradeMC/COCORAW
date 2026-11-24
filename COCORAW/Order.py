from datetime import datetime

class Order:
    def __init__(self, order_id, items, prices, cashier, cash, status="Pending", time=None):
        self.id = order_id
        self.items = items          
        self.prices = prices        
        self.cash = cash
        self.status = status
        self.time = time or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cashier = cashier
        self.total = sum(prices[name] * qty for name, qty in items.items()) #placeholder until receiptcalculator is implemented
        self.change = round(cash - self.total, 2)

    def complete(self):
        self.status = "Completed"

    def makeorder(self):
        return { 
        "id": self.id,
        "items": self.items,
        "total": self.total,
        "cash": self.cash,
        "change": self.change,
        "cashier": self.cashier,
        "prices": self.prices,
        "time": self.time,
        "status": self.status
    }