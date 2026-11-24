order = {
    "id": order_id,
    "items": items,
    "total": total,
    "cash": cash,
    "change": change,
    "cashier": self.current_user.username,
    "prices": {
        name: self.Recipes[name]["Price"]
        for name in items
    },
    "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "status": "Pending"
}