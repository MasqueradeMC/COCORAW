from datetime import datetime
from ReceiptCalculator import ReceiptCalculator
class Order:
    def __init__(self, order_id, items, prices, cashier, cash, status="Pending", time=None):
        self.id = order_id
        self.items = items          
        self.prices = prices        
        self.cash = cash
        self.status = status
        self.time = time or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cashier = cashier
        self.total =  ReceiptCalculator.total(items, prices) # receiptcalculator is now implemented
        self.change = ReceiptCalculator.change(cash, self.total)

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