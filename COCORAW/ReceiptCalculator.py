class ReceiptCalculator:
    @staticmethod
    def total(items, prices):
        return sum(prices[name] * qty for name, qty in items.items())

    @staticmethod
    def change(cash, total):
        return round(cash - total, 2)

    @staticmethod
    def build(order):
        receipt = ""
        receipt += "================================\n"
        receipt += "            COCORAW             \n"
        receipt += "        CUSTOMER RECEIPT        \n"
        receipt += "================================\n"

        receipt += f"Order ID: {order['id']}\n"
        receipt += f"Date: {order['time']}\n"
        receipt += f"Cashier: {order['cashier']}\n"

        receipt += "--------------------------------\n"

        for name, quantity in order["items"].items():
            price = order["prices"][name]
            subtotal = price * quantity

            receipt += f"{name}\n"
            receipt += f"  {quantity} x ${price:,.2f}"
            receipt += f" = ${subtotal:,.2f}\n"

        receipt += "--------------------------------\n"

        receipt += f"TOTAL:  JMD ${order['total']:,.2f}\n"
        receipt += f"CASH:   JMD ${order['cash']:,.2f}\n"
        receipt += f"CHANGE: JMD ${order['change']:,.2f}\n"

        receipt += "================================\n"
        receipt += "     Thank you for shopping!    \n"
        receipt += "================================\n"

        return receipt