import calendar
from datetime import datetime


class SalesReportGenerator:

    def generate(self, orders, recipes, month, year):
        total_items = 0
        total_revenue = 0
        product_sales = {}

        for order in orders:
            try:
                placed = datetime.strptime(order["time"], "%Y-%m-%d %H:%M:%S")
            except (KeyError, ValueError):
                continue
            if placed.year != year or placed.month != month:
                continue

            total_revenue += order.get("total", 0)
            for name, qty in order["items"].items():
                total_items += qty
                price = recipes.get(name, {}).get("Price", 0)
                if name not in product_sales:
                    product_sales[name] = {"qty": 0, "revenue": 0}
                product_sales[name]["qty"] += qty
                product_sales[name]["revenue"] += price * qty

        return {
            "month": month,
            "year": year,
            "total_items": total_items,
            "total_revenue": total_revenue,
            "products": product_sales,
        }

    def format_report(self, data):
        month_name = calendar.month_name[data["month"]]
        report = f"SALES REPORT - {month_name} {data['year']}\n"
        report += "-" * 40 + "\n"

        if data["total_items"] == 0:
            report += "No sales were recorded for this month.\n"
            report += "Total sales: $0.00\n"
        else:
            report += f"Total items sold: {data['total_items']}\n"
            report += f"Total sales revenue: ${data['total_revenue']:,.2f}\n\n"
            report += "Sales by product:\n"
            for name, info in data["products"].items():
                report += f"  {name}: {info['qty']} sold  (${info['revenue']:,.2f})\n"
        return report

    def save_report(self, report, month, year):
        filename = f"sales_report_{year}-{month:02d}.txt"
        with open(filename, "w") as file:
            file.write(report)
        return filename