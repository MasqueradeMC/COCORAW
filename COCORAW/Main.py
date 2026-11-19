import json
import os
import webbrowser
import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime

ctk.set_appearance_mode("system")
ctk.set_default_color_theme("green")

class modApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("COCORAW")
        self.geometry("1200x750")
        self.minsize(1000, 650)
        self.configure(fg_color="#F4F5F7")
        self.colors = {"border": "#D0D3D9"}

        self.data_file = "coco_raw_data_file.json"

        #Employees

        self.users = {
            "admin": {
                "password": "1234",
                "role": "Manager"
            },
            "Cashier":{
              "password": "5678",
              "role": "Cashier" 
            },
            "Barista":{
              "password": "9101",
              "role": "Barista" 
            },
        }

        #recipes
        self.Recipes = {
            "Pineapple Ginger Juice": {
                "Price": 500,
                "Ingredients": {
                    "Pineapple": 0.5,
                    "Ginger": 1
                }
            },
            "Cucumber Ginger Juice": {
                "Price": 500,
                "Ingredients": {
                    "Cucumber": 2,
                    "Ginger": 0.2
                }
            },
        }
        #inventory
        self.inventory = {
            "Pineapple":{"Quantity": 10, "LowLevel": "5"},
            "Ginger":{"Quantity": 5, "LowLevel": "2"},
            "Cucumber":{"Quantity": 8, "LowLevel": "3"}
        }
        self.orders = []
        self.current_user = None
        self.current_user_role = None
        self.quantity_entries = {}

        self.load_data()

        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(pady=20, padx=60, fill="both", expand=True)

        self.login_page()

    #Data Management

    def load_data(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r") as file:
                    data = json.load(file)
                    self.inventory = data.get("inventory", self.inventory)
                    self.Recipes = data.get("Recipes", self.Recipes)
                    self.orders = data.get("orders", self.orders)

            except (json.JSONDecodeError, TypeError):
                messagebox.showerror("Error", "Failed to load data.")

    def save_data(self):
        data = {
            "inventory": self.inventory,
            "Recipes": self.Recipes,
            "orders": self.orders
        }
        try:
            with open(self.data_file, "w") as file:
                json.dump(data, file, indent=4)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save data: {e}")

    #Screen
    def clear_screen(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def add_title(self, title):
        ctk.CTkLabel(self.main_frame, text=title, font=("Arial", 25)).pack(pady=15)
        ctk.CTkFrame(self.main_frame, height=2, fg_color=self.colors["border"]).pack(pady=(5))

    def add_BackButton(self, text, command):
        ctk.CTkButton(self.main_frame, text="Home", command=self.home_page).pack(pady=10)

    def make_card(self, parent, title, Value):
        card = ctk.CTkFrame(parent, width=200, height=100, corner_radius=10)
        ctk.CTkLabel(card, text=title.upper(), font=("Arial", 15)).pack(pady=10)
        


    #loginPage
    def login_page(self):

        self.current_user = None
        self.current_user_role = None

        self.clear_screen()
        
        self.add_title("COCORAW")

        ctk.CTkLabel(self.main_frame, text="EMPLOYEE LOGIN:").pack(pady=10)
        #username
        ctk.CTkLabel(self.main_frame, text="Username:").pack(pady=5)
        self.username_entry = ctk.CTkEntry(self.main_frame)
        self.username_entry.pack(pady=5)
        #password
        ctk.CTkLabel(self.main_frame, text="Password:").pack(pady=5)
        self.password_entry = ctk.CTkEntry(self.main_frame, show="*")
        self.password_entry.pack(pady=5)
        #login button
        ctk.CTkButton(self.main_frame, text="Login", command=self.login).pack(pady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username in self.users and self.users[username]["password"] == password:
            self.current_user = username
            self.current_user_role = self.users[username]["role"]
            messagebox.showinfo("Login Successful", f"Welcome, {self.current_user}!")
            self.home_page()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    #Role-Based Dashboard
    def home_page(self):
        self.clear_screen()
        self.add_title(f"COCORAW, {self.current_user} ({self.current_user_role})")

        ctk.CTkLabel(self.main_frame, text="Welcome:"+self.current_user+"|role:"+self.current_user_role,font=("Arial",15)).pack(pady=5)

        #Manager Dashboard
        if self.current_user_role == "Manager":
            low_items = self.get_low_items()
            if low_items:
                ctk.CTkLabel(self.main_frame, text="Low Inventory Items:"+",".join(low_items), font=("Arial", 15)).pack(pady=10)

            ctk.CTkButton(self.main_frame, text="orders", command=self.orders_page).pack(pady=10)

           
    #cashier Dashboard
        elif self.current_user_role == "Cashier":
            ctk.CTkButton(self.main_frame, text="orders", command=self.orders_page).pack(pady=10)

    #Barista Dashboard
        elif self.current_user_role == "Barista":
            ctk.CTkButton(self.main_frame, text="orders", command=self.orders_page).pack(pady=10)


    #access 
    def Check_Access(self, Roles):
        if self.current_user_role not in Roles:
            messagebox.showerror("Access Denied", "You do not have permission to access this page.")
            return False
        return True

    #inventory
    def get_low_items(self):
        low_items = []
        for name, details in self.inventory.items():
            if float(details["Quantity"]) <= float(details["LowLevel"]):
                low_items.append(name)
        return low_items

    def inventory_page(self):
        if not self.Check_Access(["Manager"]):
            return

        self.clear_screen()
        self.add_title("Ingredient Inventory")

        low_items = self.get_low_items()
        if low_items:
            ctk.CTkLabel(self.main_frame, text="Low Inventory Items:"+",".join(low_items), font=("Arial", 15)).pack(pady=10)

        invventory_text = ctk.CTkTextbox(self.main_frame, width=300, height=150)
        invventory_text.pack(pady=10)

    #Orders page: shows queue of pending orders
    def orders_page(self):
        self.clear_screen()
        self.add_title("Orders")

        #Only managers and cashiers can take new orders
        if self.current_user_role in ["Manager", "Cashier"]:
            ctk.CTkButton(self.main_frame, text="Take New Order", command=self.take_order_page).pack(pady=10)

        ctk.CTkLabel(self.main_frame, text="Order Queue (oldest first)", font=("Arial", 18)).pack(pady=5)

        #Display only the orders that are not completed yet
        pending = self.get_pending_orders()
        if not pending:
            ctk.CTkLabel(self.main_frame, text="No pending orders.").pack(pady=10)
        
        for position, order in enumerate(pending, start=1):
            ctk.CTkButton(
                self.main_frame,
                text=f"#{position}  Order ID {order['id']}  |  {order['time']}",
                command=lambda o=order: self.order_details_page(o)
            ).pack(pady=3)

        self.add_BackButton("Home", self.home_page)

    #Shows the menu items so the cashier can enter quantities 
    def take_order_page(self):
        #Only provides access to the manager and cashier
        if not self.Check_Access(["Manager", "Cashier"]):
            return
        self.clear_screen() 
        self.add_title("Take New Order")

        ctk.CTkLabel(self.main_frame, text="Menu (enter a quantity for each item)", font=("Arial", 15)).pack(pady=5)

        #Stores the quantity
        self.quantity_entries = {}

        #Shows every menu item with its price and a quantity box
        for name, recipe in self.Recipes.items():
            row = ctk.CTkFrame(self.main_frame, fg_color="transparent")
            row.pack(pady=5)
            ctk.CTkLabel(row, text=f"{name}  -  ${recipe['Price']}", width=300, anchor="w").pack(side="left", padx=10)
            entry = ctk.CTkEntry(row, width=60)
            entry.insert(0, "0")
            entry.pack(side="left", padx=10)
            self.quantity_entries[name] = entry
        ctk.CTkButton(self.main_frame, text="Place Order", command=self.submit_order).pack(pady=15)
        ctk.CTkButton(self.main_frame, text="Back", command=self.orders_page).pack(pady=5)
        
    # Reads the quantities and items and records them
    def submit_order(self):
        items = {}
        for name, entry in self.quantity_entries.items():
            text = entry.get().strip() or "0"

            #Error handling if a whole number is not entered
            if not text.isdigit():
                messagebox.showerror("Invalid Quantity", f"Enter a whole number for {name}.")
                return
            
            qty = int(text)
            if qty > 0:
                items[name] = qty
        #Ensures an order has atleast one item
        if not items:
            messagebox.showerror("Empty Order", "Select at least one item.")
            return
        #Calls the create order function
        self.create_order(items)

    #Creates the order, updates inventory and adds the order to the queue
    def create_order(self, items):
        #Checks the amount of each ingredient needed
        needed = {}
        for name, qty in items.items():
            for ingredient, amount in self.Recipes[name]["Ingredients"].items():
                needed[ingredient] = needed.get(ingredient, 0) + amount * qty

        #Ensures that there is enough ingredients
        short = []
        for ingredient, amount in needed.items():
            if ingredient not in self.inventory or float(self.inventory[ingredient]["Quantity"]) < amount:
                short.append(ingredient)
        if short:
            messagebox.showerror("Not Enough Ingredients", "Not enough: " + ", ".join(short))
            return 
        
        #Subtracts the ingredients needed from the inventory
        for ingredient, amount in needed.items():
            current = float(self.inventory[ingredient]["Quantity"])
            self.inventory[ingredient]["Quantity"] = round(current - amount, 2)

        #Uniuque order id
        order_id = max([o["id"] for o in self.orders], default=0) + 1

        #Total price of the order
        total = sum(self.Recipes[name]["Price"] * qty for name, qty in items.items())

        #Finalizes the order with its ID, date/time and status
        order = {
            "id": order_id,
            "items": items,
            "total": total,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status": "Pending"
        }

        #Adds order to the end of the queue
        self.orders.append(order)
        self.save_data()

        #Returns to the order page
        messagebox.showinfo("Order Created", f"Order {order_id} has been recorded.\nTotal: ${total}")
        self.orders_page()

    #Displays the orders that are not completed in the order that they were placed
    def get_pending_orders(self):
        return [o for o in self.orders if o.get("status", "Pending") != "Completed"]

    #Shows the items and quantities ordered
    def order_details_page(self, order):
        self.clear_screen()
        self.add_title(f"Order {order['id']}")

        ctk.CTkLabel(self.main_frame, text=f"Placed: {order['time']}", font=("Arial", 15)).pack(pady=5)

        for name, qty in order["items"].items():
            ctk.CTkLabel(self.main_frame, text=f"{qty} x {name}", font=("Arial", 15)).pack(pady=2)

    #Only the barista and manager can mark an order as completed
        if self.current_user_role in ["Manager", "Barista"]:
            ctk.CTkButton(self.main_frame, text="Mark as Completed", command=lambda: self.complete_order(order)).pack(pady=15)
        ctk.CTkButton(self.main_frame, text="Back to Queue", command=self.orders_page).pack(pady=5)

    #Marks an order as completed removing it from the queue
    def complete_order(self, order):
        order["status"] = "Completed"
        self.save_data()
        messagebox.showinfo("Order Completed", f"Order {order['id']} has been completed.")
        self.orders_page()

    

if __name__ == "__main__":
    app = modApp()
    app.mainloop() 