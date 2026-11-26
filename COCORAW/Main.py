import operator
import json
import os
import webbrowser
import calendar
import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
from User import USERS
from Inventory import Inventory
from Queue import Queue
from Order import Order
from ReceiptCalculator import ReceiptCalculator
from SalesReportGenerator import SalesReportGenerator

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")
FONT = "verdana"
ctk.ThemeManager.theme["CTkFont"]["family"] = FONT

class modApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("COCORAW SMOOTHIE SHOP")
        self.geometry("1200x750")       
        self.minsize(1000, 650)
        self.configure(fg_color="#11A600")
        self.colors = {"border": "#2B221B", "text_color": "#D0D3D9"}
        self.after(100, lambda: self.state("zoomed")) #I was trying to center the screen and it wasn't working, so we get fullscreen instead

        self.data_file = "coco_raw_data_file.json"

        self.current_user = None
        self.quantity_entries = {}

        self.last_order = None
        self.subtotal_labels = {}

        #Calculator Variables
        self.calc_first = None
        self.calc_operator = None
        self.calc_new_number = True

        self.inventory = Inventory()
        self.queue = Queue()

        self.load_data()
        self.report_generator = SalesReportGenerator()

        self.main_frame = ctk.CTkFrame(self, fg_color="#3D322B", corner_radius=15)
        self.main_frame.pack(pady=20, padx=30, fill="both", expand=True)

        self.login_page()

    #Data Management
    def load_data(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r") as file:
                    data = json.load(file)
                    self.inventory.stock = data.get("inventory", self.inventory.stock)
                    self.inventory.recipes = data.get("Recipes", self.inventory.recipes)
                    self.queue.orders = data.get("orders", self.queue.orders)
                    self.inventory.log = data.get("stock_log", self.inventory.log)

            except (OSError, json.JSONDecodeError, TypeError, AttributeError):
                messagebox.showerror("Error", "Failed to load data.")

    def save_data(self):
        data = {
            "inventory": self.inventory.stock,
            "Recipes": self.inventory.recipes ,
            "orders": self.queue.orders,
            "stock_log": self.inventory.log
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
        ctk.CTkLabel(self.main_frame, text=title, font=("verdana", 28, "bold")).pack(pady=20, padx=10)
        ctk.CTkFrame(self.main_frame, height=2, fg_color=self.colors["border"]).pack(fill="x", padx=30, pady=5)

    def add_BackButton(self, text, command):
        ctk.CTkButton(self.main_frame, text=text, command=command, height=38, corner_radius=8).pack(pady=10)

    def make_card(self, parent, title, Value):
        card = ctk.CTkFrame(parent, width=200, height=100, corner_radius=10)
        ctk.CTkLabel(card, text=title.upper(), font=("verdana", 15)).pack(pady=10)
        ctk.CTkLabel(card, text=str(Value)).pack(pady=5)
        return card

    #loginPage
    def login_page(self):

        self.current_user = None
        self.clear_screen()
        self.add_title("COCORAW SMOOTHIE SHOP")

        ctk.CTkLabel(self.main_frame, text="EMPLOYEE LOGIN:").pack(pady=10)
        #username
        ctk.CTkLabel(self.main_frame, text="USERNAME:").pack(pady=5)
        self.username_entry = ctk.CTkEntry(self.main_frame)
        self.username_entry.pack(pady=5)
        #password
        ctk.CTkLabel(self.main_frame, text="PASSWORD:").pack(pady=5)
        self.password_entry = ctk.CTkEntry(self.main_frame, show="*")
        self.password_entry.pack(pady=5)
        #login button
        ctk.CTkButton(self.main_frame, text="Login", command=self.login).pack(pady=10)
        ctk.CTkButton(self.main_frame, text="Exit", command=self.destroy, fg_color="#B3261E").pack(pady=5)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        user = USERS.get(username)
        if user and user.check_password(password):
            self.current_user = user
            messagebox.showinfo("Logged in", f"Welcome, {self.current_user.username}!")
            self.home_page()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password. Please try again.")

    #Role-Based Dashboard
    def home_page(self):
        self.clear_screen()
        self.add_title(f"COCORAW, {self.current_user.username} ({self.current_user.role})")

        ctk.CTkLabel(self.main_frame, text="Welcome: " +self.current_user.role + "!",font=("verdana",15)).pack(pady=5)

        #Manager Dashboard
        if self.current_user.role == "Manager":
            low_items = self.inventory.low_items()
            if low_items:
                ctk.CTkLabel(self.main_frame, text="Low Inventory Items:"+",".join(low_items), font=("verdana", 15)).pack(pady=10)

            ctk.CTkButton(self.main_frame, text="Orders", command=self.orders_page).pack(pady=10)

            ctk.CTkButton(self.main_frame, text="Inventory", command=self.inventory_page).pack(pady=10)

            ctk.CTkButton(self.main_frame, text="Sales Report", command=self.report_page).pack(pady=10)


        #cashier Dashboard
        elif self.current_user.role == "Cashier":
            ctk.CTkButton(self.main_frame, text="Orders", command=self.orders_page).pack(pady=10)

        #Barista Dashboard
        elif self.current_user.role == "Barista":
            ctk.CTkButton(self.main_frame, text="Orders", command=self.orders_page).pack(pady=10)


        ctk.CTkButton(self.main_frame, text="Logout", command=self.login_page).pack(pady=10)

    #checks who is accessing the system
    def Check_Access(self, Roles):
        if self.current_user is None or self.current_user.role not in Roles:
            messagebox.showerror("Access Denied", "You do not have permission to access this page.")
            return False
        return True

    def inventory_page(self):
        if not self.Check_Access(["Manager"]):
            return

        self.clear_screen()
        self.add_title("Ingredient Inventory")

        low_items = self.inventory.low_items()
        if low_items:
            ctk.CTkLabel(self.main_frame, text="Low Inventory Items:"+",".join(low_items), font=("verdana", 15)).pack(pady=10)

        inventory_text = ctk.CTkTextbox(self.main_frame, width=600, height=350,corner_radius=10 )
        inventory_text.pack(pady=20, padx=30)

        ctk.CTkButton(self.main_frame, text="Edit Inventory", command=self.manage_items_page).pack(pady=5)
        ctk.CTkButton(self.main_frame, text="View Stock Log", command=self.stock_log_page).pack(pady=5)

        for name, details in self.inventory.stock.items():
            inventory_text.insert("end", f"{name}: {details['Quantity']}\n")
        inventory_text.configure(state="disabled")
        self.add_BackButton("Home", self.home_page)


    #Orders page: shows queue of pending orders
    def orders_page(self):
        self.clear_screen()
        self.add_title("Orders")

        #Only managers and cashiers can take new orders
        if self.current_user.role in ["Manager", "Cashier"]:
            ctk.CTkButton(self.main_frame, text="Take New Order", command=self.take_order_page).pack(pady=10)

        ctk.CTkLabel(self.main_frame, text="Order Queue", font=("verdana", 18)).pack(pady=5)

        #Display only the orders that are not completed yet
        pending = self.queue.pending()
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

    # Cashier Point of Sale Page
    def take_order_page(self):

        if not self.Check_Access(["Manager", "Cashier"]):
            return

        self.clear_screen()
        self.add_title("COCORAW | Point of Sale")

        self.quantity_entries = {}
        self.subtotal_labels = {}
        self.last_order = None

        # Main POS container
        container = ctk.CTkFrame(self.main_frame)
        container.pack(fill="both", expand=True, padx=20, pady=10)

        # Left side - Customer order
        order_frame = ctk.CTkScrollableFrame(container)
        order_frame.pack(side="left", fill="both", expand=True, padx=10)

        # Right side - Calculator
        calculator_frame = ctk.CTkFrame(container)
        calculator_frame.pack(side="right", fill="y", padx=10)

        ctk.CTkLabel(
            order_frame,
            text="Customer Order",
            font=("verdana", 22, "bold")
        ).pack(pady=10)

        # Menu items
        for name, recipe in self.inventory.recipes.items():

            row = ctk.CTkFrame(order_frame)
            row.pack(fill="x", padx=10, pady=5)

            ctk.CTkLabel(
                row,
                text=f"{name} - ${recipe['Price']}",
                width=250,
                anchor="w"
            ).pack(side="left", padx=5)

            entry = ctk.CTkEntry(row, width=50)
            entry.insert(0, "0")
            entry.pack(side="left", padx=5)

            entry.bind(
                "<KeyRelease>",
                lambda event: self.calculate_total()
            )

            self.quantity_entries[name] = entry

            subtotal = ctk.CTkLabel(row, text="$0.00")
            subtotal.pack(side="right", padx=10)

            self.subtotal_labels[name] = subtotal

        # Total cost
        self.total_label = ctk.CTkLabel(
            order_frame,
            text="Total: $0.00",
            font=("verdana", 28, "bold"),
            text_color="green"
        )
        self.total_label.pack(pady=15)

        # Cash received
        ctk.CTkLabel(
            order_frame,
            text="Cash Received (JMD)"
        ).pack(pady=5)

        self.cash_entry = ctk.CTkEntry(order_frame, width=200)
        self.cash_entry.pack(pady=5)

        self.cash_entry.bind(
            "<KeyRelease>",
            lambda event: self.calculate_change()
        )

        # Customer change
        self.change_label = ctk.CTkLabel(
            order_frame,
            text="Change: $0.00",
            font=("verdana", 20)
        )
        self.change_label.pack(pady=10)

        # Calculator
        ctk.CTkLabel(
            calculator_frame,
            text="Calculator",
            font=("verdana", 22, "bold")
        ).pack(pady=10)

        self.calc_display = ctk.CTkEntry(
            calculator_frame,
            width=250,
            height=45,
            font=("verdana", 22),
            justify="right"
        )

        self.calc_display.pack(padx=10, pady=10)
        self.calc_display.insert(0, "0")
        self.calc_display.configure(state="disabled")

        self.calc_first = None
        self.calc_operator = None
        self.calc_new_number = True

        buttons_frame = ctk.CTkFrame(calculator_frame)
        buttons_frame.pack(pady=5)

        buttons = [
            ["7", "8", "9", "/"],
            ["4", "5", "6", "*"],
            ["1", "2", "3", "-"],
            ["C", "0", ".", "+"],
            ["="]
        ]

        for r, button_row in enumerate(buttons):
            for c, value in enumerate(button_row):

                ctk.CTkButton(
                    buttons_frame,
                    text=value,
                    width=55,
                    height=45,
                    command=lambda v=value: self.calculator_input(v)
                ).grid(row=r, column=c, padx=3, pady=3)

        # Order buttons
        self.place_order_button = ctk.CTkButton(
            order_frame,
            text="Place Order",
            command=self.submit_order
        )
        self.place_order_button.pack(pady=5)

        self.receipt_button = ctk.CTkButton(
            order_frame,
            text="Print Receipt",
            command=self.print_receipt,
            state="disabled"
        )
        self.receipt_button.pack(pady=5)

        ctk.CTkButton(
            order_frame,
            text="Back to Order Queue",
            command=self.orders_page
        ).pack(pady=5)

    # Calculates the total cost of the order
    def calculate_total(self):

        total = 0

        for name, entry in self.quantity_entries.items():

            text = entry.get().strip()

            try:
                quantity = max(0, int(text))
            except ValueError:
                quantity = 0

            price = self.inventory.recipes[name]["Price"]
            subtotal = quantity * price

            total += subtotal

            self.subtotal_labels[name].configure(
                text=f"${subtotal:,.2f}"
            )

        self.total_label.configure(
            text=f"Total: ${total:,.2f}"
        )

        self.calculate_change(total)

        return total


    # Calculates the customer's change
    def calculate_change(self, total=None):

        if total is None:
            total = 0

            for name, entry in self.quantity_entries.items():

                try:
                    quantity = max(0, int(entry.get()))
                    total += self.inventory.recipes [name]["Price"] * quantity

                except ValueError:
                    pass

        try:
            cash = float(self.cash_entry.get())

            if not 0 <= cash < float("inf"):
                raise ValueError

        except ValueError:
            self.change_label.configure(text="Change: $0.00", text_color="green")
            return

        change = cash - total

        if change < 0:
            self.change_label.configure(
                text=f"Amount Due: ${abs(change):,.2f}",
                text_color="red"
            )

        else:
            self.change_label.configure(
                text=f"Change: ${change:,.2f}",
                text_color="green"
            )

    # Handles calculator operations
    def calculator_input(self, value):

        current = self.calc_display.get()

        operations = {
            "+": operator.add,
            "-": operator.sub,
            "*": operator.mul,
            "/": operator.truediv
        }

        try:

            if value == "C":
                result = "0"
                self.calc_first = None
                self.calc_operator = None
                self.calc_new_number = True

            elif value in operations:
                self.calc_first = float(current)
                self.calc_operator = value
                self.calc_new_number = True
                return

            elif value == "=":

                if self.calc_operator is None:
                    return

                second = float(current)

                result = str(
                    operations[self.calc_operator](
                        self.calc_first, second
                    )
                )

                self.calc_first = None
                self.calc_operator = None
                self.calc_new_number = True

            else:

                if self.calc_new_number or current == "Error":
                    current = "0"
                    self.calc_new_number = False

                if value == "." and "." in current:
                    return

                if current == "0" and value != ".":
                    result = value
                else:
                    result = current + value

        except (ValueError, ZeroDivisionError, TypeError):

            result = "Error"
            self.calc_first = None
            self.calc_operator = None
            self.calc_new_number = True

        self.calc_display.configure(state="normal")
        self.calc_display.delete(0, "end")
        self.calc_display.insert(0, result)
        self.calc_display.configure(state="disabled")


    # Reads the quantities and items and records them
    def submit_order(self):
        items = {}
        for name, entry in self.quantity_entries.items():
            text = entry.get().strip() or "0"

            #Error handling if a whole number is not entered
            if not text.isdecimal():
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
        needed = self.inventory.needed_for(items)
        short = self.inventory.shortages(needed)
        

        if short:
            messagebox.showerror("Not Enough Ingredients", "Not enough: " + ", ".join(short))
            return

        prices = {name: self.inventory.recipes[name]["Price"] for name in items}
        total = ReceiptCalculator.total(items, prices)

        try:
            cash = float(self.cash_entry.get())
            if not 0 <= cash < float("inf"):
                raise ValueError
        except ValueError:
            messagebox.showerror(
                "Invalid Payment", "Enter a valid cash amount.")
            return

        if cash < total:
            messagebox.showerror(
                "Insufficient Payment", "The customer has not paid enough.")
            return

        
        order_id = self.queue.next_id()
        self.inventory.use(needed, self.current_user.username, order_id)
        order = Order(order_id, items, prices, self.current_user.username, cash).makeorder()
        
        self.queue.add(order)
        self.last_order = order

        order_id = order["id"]
        change = order["change"]

        self.save_data()


        # Enable receipt printing
        self.receipt_button.configure(state="normal")

        # Prevent the same order from being submitted twice
        self.place_order_button.configure(state="disabled")

        for entry in self.quantity_entries.values():
            entry.configure(state="disabled")

        self.cash_entry.configure(state="disabled")

        messagebox.showinfo(
            "Order Created",
            f"Order {order_id} recorded successfully!\n"
            f"Total: ${total:,.2f}\n"
            f"Cash: ${cash:,.2f}\n"
            f"Change: ${change:,.2f}"
        )

        ctk.CTkButton(
            self.place_order_button.master,
            text="Start New Order",
            command=self.take_order_page
        ).pack(pady=5)

    
    #Shows the items and quantities ordered
    def order_details_page(self, order):
        self.clear_screen()
        self.add_title(f"Order {order['id']}")

        ctk.CTkLabel(self.main_frame, text=f"Placed: {order['time']}", font=("segoe UI", 15)).pack(pady=5)

        for name, qty in order["items"].items():
            ctk.CTkLabel(self.main_frame, text=f"{qty} x {name}", font=("segoe UI", 15)).pack(pady=2)

        #Only the barista and manager can mark an order as completed
        if self.current_user.role in ["Manager", "Barista"]:
            ctk.CTkButton(self.main_frame, text="Mark as Completed", command=lambda: self.complete_order(order)).pack(pady=15)
        ctk.CTkButton(self.main_frame, text="Back to Queue", command=self.orders_page).pack(pady=5)

    #Marks an order as completed removing it from the queue
    def complete_order(self, order):
        self.queue.complete(order)
        self.save_data()
        messagebox.showinfo("Order Completed", f"Order {order['id']} has been completed.")
        self.orders_page()


    # Generates and prints the customer's receipt
    def print_receipt(self):
        if self.last_order is None:
            messagebox.showerror(
                "No Order",
                "Place an order before printing a receipt."
            )
            return

        order = self.last_order

        receipt = ReceiptCalculator.build(self.last_order)

        try:

            # Creates a folder for all receipts
            os.makedirs("Receipts", exist_ok=True)

            filename = os.path.abspath(
                f"Receipts/Receipt_{order['id']}.txt"
            )

            with open(filename, "w", encoding="utf-8") as file:
                file.write(receipt)

        except OSError as e:
            messagebox.showerror("Receipt Error", str(e))
            return

        try:

            if os.name == "nt":
                # Sends receipt to default Windows printer
                os.startfile(filename, "print")

                messagebox.showinfo(
                    "Receipt",
                    "Receipt sent for printing."
                )

            else:
                webbrowser.open("file://" + filename)

        except OSError:

            messagebox.showwarning(
                "Printer Error",
                f"Unable to print automatically.\n"
                f"Receipt saved at:\n{filename}"
            )

        
    def report_page(self):
        if not self.Check_Access(["Manager"]):
            return

        self.clear_screen()
        self.add_title("Monthly Sales Report")

        ctk.CTkLabel(self.main_frame, text="Select a month and year", font=("verdana", 15)).pack(pady=5)

        selector = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        selector.pack(pady=5)

        months = list(calendar.month_name)[1:]
        self.month_menu = ctk.CTkOptionMenu(selector, values=months, width=180, height=38)
        self.month_menu.set(months[datetime.now().month - 1])
        self.month_menu.pack(side="left", padx=5)

        self.year_entry = ctk.CTkEntry(selector, width=180, height=38)
        self.year_entry.insert(0, str(datetime.now().year))
        self.year_entry.pack(side="left", padx=5)

        ctk.CTkButton(self.main_frame, text="Generate Report", command=self.generate_report).pack(pady=10)

        self.report_box = ctk.CTkTextbox(self.main_frame, width=650, height=350, corner_radius=10)
        self.report_box.pack(pady=15, padx=20)
        self.report_box.configure(state="disabled")

        self.add_BackButton("Home", self.home_page)

    def add_item_action(self):
        name = self.new_name.get().strip()
        try:
            quantity = float(self.new_qty.get() or 0)
            low_level = float(self.new_low.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Quantity and low level must be numbers.")
            return

        if not name or quantity < 0 or low_level < 0:
            messagebox.showerror("Invalid Input", "Enter a name and a non negative numbers.")
            return

        try:
            self.inventory.add_item(name, quantity, low_level, self.current_user.username)
        except ValueError as e:
            messagebox.showerror("Cannot Add", str(e))
            return

        self.save_data()
        self.manage_items_page()

    def edit_item_action(self):
        qty_text = self.edit_qty.get().strip()
        low_text = self.edit_low.get().strip()
        try:
            quantity = float(qty_text) if qty_text else None
            low_level = float(low_text) if low_text else None
        except ValueError:
            messagebox.showerror("Invalid Input", "Enter numbers only.")
            return

        if quantity is None and low_level is None:
            messagebox.showerror("Nothing to Change", "Enter a new quantity or low level.")
            return
        if low_level is not None and low_level < 0:
            messagebox.showerror("Invalid Input", "Low level cannot be negative.")
            return

        try:
            self.inventory.edit_item(self.edit_menu.get(), quantity, low_level, self.current_user.username)
        except ValueError:
            messagebox.showerror("Invalid Input", "Quantity cannot be negative.")
            return

        self.save_data()
        self.inventory_page()

    def manage_items_page(self):
        if not self.Check_Access(["Manager"]):
            return

        self.clear_screen()
        self.add_title("Edit Inventory")

        ctk.CTkLabel(self.main_frame, text="Add new ingredient", font=("verdana", 18)).pack(pady=5)
        self.new_name = ctk.CTkEntry(self.main_frame, width=250, placeholder_text="Ingredient name")
        self.new_name.pack(pady=3)
        self.new_qty = ctk.CTkEntry(self.main_frame, width=250, placeholder_text="Starting quantity")
        self.new_qty.pack(pady=3)
        self.new_low = ctk.CTkEntry(self.main_frame, width=250, placeholder_text="Low level")
        self.new_low.pack(pady=3)
        ctk.CTkButton(self.main_frame, text="Add Ingredient", command=self.add_item_action).pack(pady=5)

        ctk.CTkLabel(self.main_frame, text="Edit existing ingredient", font=("verdana", 18)).pack(pady=(20, 5))
        self.edit_menu = ctk.CTkOptionMenu(self.main_frame, values=list(self.inventory.stock))
        self.edit_menu.pack(pady=3)
        self.edit_qty = ctk.CTkEntry(self.main_frame, width=250, placeholder_text="New quantity (blank = unchanged)")
        self.edit_qty.pack(pady=3)
        self.edit_low = ctk.CTkEntry(self.main_frame, width=250, placeholder_text="New low level (blank = unchanged)")
        self.edit_low.pack(pady=3)
        ctk.CTkButton(self.main_frame, text="Save Changes", command=self.edit_item_action).pack(pady=5)

        self.add_BackButton("Back to Inventory", self.inventory_page)

    def apply_adjustment(self):
        try:
            amount = float(self.adjust_amount.get())
        except ValueError:
            messagebox.showerror("Invalid Amount", "Enter a number.")
            return

        reason = self.adjust_reason.get().strip()
        if amount == 0 or not reason:
            messagebox.showerror("Missing Info", "Enter a non-zero amount and a reason.")
            return

        try:
            self.inventory.adjust(self.adjust_item.get(), amount, reason, self.current_user.username)
        except ValueError:
            messagebox.showerror("Not Enough Stock", "That would take stock below zero.")
            return

        self.save_data()
        self.inventory_page()

    def stock_log_page(self):
        if not self.Check_Access(["Manager"]):
            return

        self.clear_screen()
        self.add_title("Stock Adjustment Log")

        log_text = ctk.CTkTextbox(self.main_frame, width=700, height=350, corner_radius=10)
        log_text.pack(pady=10, padx=30)
        for e in reversed(self.inventory.log):
            log_text.insert("end", f"{e['time']} | {e['user']} | {e['item']} {e['change']:+g} -> {e['new_quantity']} | {e['reason']}\n")
        log_text.configure(state="disabled")
        self.add_BackButton("Back to Inventory", self.inventory_page)

    def generate_report(self):
        if not self.Check_Access(["Manager"]):
            return

        year_text = self.year_entry.get().strip()
        if not year_text.isdigit() or len(year_text) != 4:
            messagebox.showerror("Invalid Year", "Enter a 4-digit year, e.g. 2026.")
            return

        year = int(year_text)
        month = list(calendar.month_name).index(self.month_menu.get())

        data = self.report_generator.generate(self.queue.orders, self.inventory.recipes, month, year)
        report = self.report_generator.format_report(data)

        self.report_box.configure(state="normal")
        self.report_box.delete("1.0", "end")
        self.report_box.insert("1.0", report)
        self.report_box.configure(state="disabled")

        try:
            self.report_generator.save_report(report, month, year)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save report: {e}")


if __name__ == "__main__":
    app = modApp()
    app.mainloop()
