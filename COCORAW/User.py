class User:
    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role

    def check_password(self, password):
        return self.password == password

    def has_access(self, authorizedrole):
        return self.role in authorizedrole


USERS = {  #dictionary of set usernames, passwords and roles
        "Admin": User("Admin", "1234", "Manager"),
        "Cashier": User("Cashier", "5678", "Cashier"),
        "Barista": User("Barista", "9101", "Barista"),
        }