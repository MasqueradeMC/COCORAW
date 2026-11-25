from datetime import datetime

class Inventory:
    def __init__(self, stock=None, recipes=None):
        self.log = []

        self.stock = stock or{ 
            "Pineapple": {"Quantity": 10, "LowLevel": "5"},
            "Ginger": {"Quantity": 5, "LowLevel": "2"},
            "Cucumber": {"Quantity": 8, "LowLevel": "3"}
        } 
        self.recipes = recipes or {
            "Pineapple Ginger Juice": {
            "Price": 500,
            "Ingredients": {"Pineapple": 0.5, "Ginger": 1 }},
            "Cucumber Ginger Juice": {
            "Price": 500,
            "Ingredients": {"Cucumber": 2, "Ginger": 0.2}},
        }

    def low_items(self):
        return [n for n, d in self.stock.items()
                if float(d["Quantity"]) <= float(d["LowLevel"])]

    def needed_for(self, items):
        needed = {}
        for name, qty in items.items():
            for ing, amt in self.recipes[name]["Ingredients"].items():
                needed[ing] = needed.get(ing, 0) + amt * qty
        return needed

    def shortages(self, needed):
        short = []
        for ingredient, amount in needed.items():
            if ingredient not in self.stock or float(self.stock[ingredient]["Quantity"]) < amount:
                short.append(ingredient)
        return short

    def adjust(self, name, amount, reason, user):
        new = round(float(self.stock[name]["Quantity"]) + amount, 2)
        if new < 0:
            raise ValueError("Stock cannot go below zero")
        self.stock[name]["Quantity"] = new
        self.log.append({
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "item": name,
            "change": amount,
            "new_quantity": new,
            "reason": reason,
            "user": user,
        })

    def use(self, needed, user, order_id):
        for ingredient, amount in needed.items():
            self.adjust(ingredient, -amount, f"Order #{order_id}", user)

    def add_item(self, name, quantity, low_level, user):
        if name in self.stock:
            raise ValueError("That ingredient is already in the system. Try again.")
        self.stock[name] = {"Quantity": 0, "LowLevel": low_level}
        self.adjust(name, quantity, "New ingredient added", user)

    def edit_item(self, name, quantity, low_level, user):
        if quantity is not None:
            difference = quantity - float(self.stock[name]["Quantity"])
            if difference != 0:
                self.adjust(name, difference, "Manual edit", user)
        if low_level is not None:
            self.stock[name]["LowLevel"] = low_level
            self.log.append({
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "item": name,
                "change": 0,
                "new_quantity": self.stock[name]["Quantity"],
                "reason": f"Low level set to {low_level}",
                "user": user,
            })