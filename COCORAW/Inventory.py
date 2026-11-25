from datetime import datetime

class Inventory:
    def __init__(self, stock=None, recipes=None):
        self.log = []

        self.stock = stock or {
            "Pineapple": {"Quantity": 20, "LowLevel": "5"},
            "Ginger": {"Quantity": 5, "LowLevel": "2"},
            "Cucumber": {"Quantity": 8, "LowLevel": "3"},
            "Sorrel": {"Quantity": 20, "LowLevel": "5"},
            "Lemon": {"Quantity": 20, "LowLevel": "5"},
            "Carrot": {"Quantity": 20, "LowLevel": "5"},
            "Watermelon": {"Quantity": 20, "LowLevel": "5"},
            "Lime": {"Quantity": 20, "LowLevel": "5"},
            "June Plum": {"Quantity": 20, "LowLevel": "5"},
            "Coconut": {"Quantity": 20, "LowLevel": "5"},
            "Strawberry": {"Quantity": 20, "LowLevel": "5"},
            "Banana": {"Quantity": 20, "LowLevel": "5"},
            "Pumpkin Seeds": {"Quantity": 20, "LowLevel": "5"},
            "Sunflower Seeds": {"Quantity": 20, "LowLevel": "5"},
            "Flaxseeds": {"Quantity": 20, "LowLevel": "5"},
            "Plantain": {"Quantity": 20, "LowLevel": "5"},
            "Oats": {"Quantity": 20, "LowLevel": "5"},
            "Mango": {"Quantity": 20, "LowLevel": "5"},
            "Spirulina": {"Quantity": 20, "LowLevel": "5"},
            "Papaya": {"Quantity": 20, "LowLevel": "5"},
            "Cinnamon": {"Quantity": 20, "LowLevel": "5"},
            "Blueberry": {"Quantity": 20, "LowLevel": "5"},
            "Beetroot": {"Quantity": 20, "LowLevel": "5"},
            "Chocolate": {"Quantity": 20, "LowLevel": "5"},
            "Protein": {"Quantity": 20, "LowLevel": "5"},
            "Mixed Seeds": {"Quantity": 20, "LowLevel": "5"},
            "Peanuts": {"Quantity": 20, "LowLevel": "5"},
        }
        
        self.recipes = recipes or {
            # Natural juices
            "Sorrel (12oz)": {"Price": 450, "Ingredients": {"Sorrel": 1}},
            "Sorrel (16oz)": {"Price": 600, "Ingredients": {"Sorrel": 1.33}},
            "Lemonade (12oz)": {"Price": 450, "Ingredients": {"Lemon": 1}},
            "Lemonade (16oz)": {"Price": 600, "Ingredients": {"Lemon": 1.33}},
            "Pineapple Ginger (12oz)": {"Price": 450, "Ingredients": {"Pineapple": 0.5, "Ginger": 1}},
            "Pineapple Ginger (16oz)": {"Price": 600, "Ingredients": {"Pineapple": 0.67, "Ginger": 1.33}},
            "Carrot Pineapple (12oz)": {"Price": 450, "Ingredients": {"Carrot": 1, "Pineapple": 1}},
            "Carrot Pineapple (16oz)": {"Price": 600, "Ingredients": {"Carrot": 1.33, "Pineapple": 1.33}},
            "Cucumber Ginger (12oz)": {"Price": 450, "Ingredients": {"Cucumber": 2, "Ginger": 0.2}},
            "Cucumber Ginger (16oz)": {"Price": 600, "Ingredients": {"Cucumber": 2.67, "Ginger": 0.27}},
            "Watermelon Lime (12oz)": {"Price": 450, "Ingredients": {"Watermelon": 1, "Lime": 1}},
            "Watermelon Lime (16oz)": {"Price": 600, "Ingredients": {"Watermelon": 1.33, "Lime": 1.33}},
            "June Plum (12oz)": {"Price": 450, "Ingredients": {"June Plum": 1}},
            "June Plum (16oz)": {"Price": 600, "Ingredients": {"June Plum": 1.33}},
            "Coconut Water (12oz)": {"Price": 350, "Ingredients": {"Coconut": 1}},
            "Coconut Water (16oz)": {"Price": 450, "Ingredients": {"Coconut": 1.33}},

            # Smoothies
            "Stranana Breeze (12oz)": {"Price": 900, "Ingredients": {"Strawberry": 1, "Banana": 1}},
            "Stranana Breeze (16oz)": {"Price": 1100, "Ingredients": {"Strawberry": 1.33, "Banana": 1.33}},
            "Big Man Ting (12oz)": {"Price": 1100, "Ingredients": {"Pumpkin Seeds": 1, "Sunflower Seeds": 1, "Flaxseeds": 1, "Plantain": 1, "Oats": 1}},
            "Big Man Ting (16oz)": {"Price": 1300, "Ingredients": {"Pumpkin Seeds": 1.33, "Sunflower Seeds": 1.33, "Flaxseeds": 1.33, "Plantain": 1.33, "Oats": 1.33}},
            "Man A Go Pine (12oz)": {"Price": 950, "Ingredients": {"Mango": 1, "Pineapple": 1}},
            "Man A Go Pine (16oz)": {"Price": 1150, "Ingredients": {"Mango": 1.33, "Pineapple": 1.33}},
            "Mr Green (12oz)": {"Price": 1000, "Ingredients": {"Spirulina": 1, "Banana": 1, "Papaya": 1}},
            "Mr Green (16oz)": {"Price": 1200, "Ingredients": {"Spirulina": 1.33, "Banana": 1.33, "Papaya": 1.33}},
            "Coconut Cinnamon (12oz)": {"Price": 900, "Ingredients": {"Coconut": 1, "Cinnamon": 1, "Banana": 1}},
            "Coconut Cinnamon (16oz)": {"Price": 1100, "Ingredients": {"Coconut": 1.33, "Cinnamon": 1.33, "Banana": 1.33}},
            "Coco Very Berry (12oz)": {"Price": 950, "Ingredients": {"Blueberry": 1, "Strawberry": 1, "Papaya": 1}},
            "Coco Very Berry (16oz)": {"Price": 1150, "Ingredients": {"Blueberry": 1.33, "Strawberry": 1.33, "Papaya": 1.33}},
            "Mango Berry (12oz)": {"Price": 950, "Ingredients": {"Mango": 1, "Blueberry": 1, "Strawberry": 1, "Pineapple": 1}},
            "Mango Berry (16oz)": {"Price": 1150, "Ingredients": {"Mango": 1.33, "Blueberry": 1.33, "Strawberry": 1.33, "Pineapple": 1.33}},
            "Pina Colada (12oz)": {"Price": 850, "Ingredients": {"Pineapple": 1, "Coconut": 1}},
            "Pina Colada (16oz)": {"Price": 1050, "Ingredients": {"Pineapple": 1.33, "Coconut": 1.33}},
            "Sweet Beet (12oz)": {"Price": 850, "Ingredients": {"Beetroot": 1, "Carrot": 1, "Papaya": 1}},
            "Sweet Beet (16oz)": {"Price": 1050, "Ingredients": {"Beetroot": 1.33, "Carrot": 1.33, "Papaya": 1.33}},
            "Caribbean Chocolate (12oz)": {"Price": 850, "Ingredients": {"Chocolate": 1, "Banana": 1}},
            "Caribbean Chocolate (16oz)": {"Price": 1050, "Ingredients": {"Chocolate": 1.33, "Banana": 1.33}},

            # Smoothie add-ons
            "Add-on: Protein": {"Price": 350, "Ingredients": {"Protein": 1}},
            "Add-on: Mixed Seeds": {"Price": 200, "Ingredients": {"Mixed Seeds": 1}},
            "Add-on: Peanuts": {"Price": 200, "Ingredients": {"Peanuts": 1}},
            "Add-on: Oats": {"Price": 200, "Ingredients": {"Oats": 1}},
            "Add-on: Spirulina": {"Price": 200, "Ingredients": {"Spirulina": 1}},
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