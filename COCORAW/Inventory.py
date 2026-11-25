class Inventory:
    def __init__(self, stock=None, recipes=None):
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


    def use(self, needed):
        for ingredient, amount in needed.items():
            current = float(self.stock[ingredient]["Quantity"])
            self.stock[ingredient]["Quantity"] = round(current - amount, 2)