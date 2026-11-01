import json
import os
import webbrowser
import customtkinter as ctk
from tkinter import messagebox

ctk.set_appearance_mode("system")
ctk.set_default_color_theme("green")

class modApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("COCORAW")
        self.geometry("1200x750")
        self.minsize(1000, 650)
        self.configure(fg_color="#F4F5F7")

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

            except json.JSONDecodeError, TypeError:
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
    def Login_Page(self):

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

        ctk.CTkLabel(self.main_frame, text="Welcome:"+self.current_user+"|role:"+self.current_role,font=("Arial",15)).pack(pady=5)

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
        
        
    

if __name__ == "__main__":
    app = modApp()
    app.mainloop() 