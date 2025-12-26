# from matplotlib import colors
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

FILE_NAME = "sales_data.csv"

# Create CSV if not exists
try:
    df = pd.read_csv(FILE_NAME)
except FileNotFoundError:
    df = pd.DataFrame(columns=["Date", "Product", "Quantity", "Price", "Cost"])
    df.to_csv(FILE_NAME, index=False)


# Add Sales Record
def add_sale():
    date = input("Enter Date (DD-MM-YYYY): ")

    # Basic date format validation
    if len(date) != 10 or date[2] != '-' or date[5] != '-':
        print("Invalid date format! Use DD-MM-YYYY\n")
        return

    day, month, year = date.split('-')

    if not (day.isdigit() and month.isdigit() and year.isdigit()):
        print("Date should contain only numbers\n")
        return

    day = int(day)
    month = int(month)
    year = int(year)

    if day < 1 or day > 31 or month < 1 or month > 12 or year < 1900:
        print("Invalid date values!\n")
        return

    product = input("Product Name: ")
    quantity = int(input("Quantity Sold: "))
    price = float(input("Selling Price per unit: "))
    cost = float(input("Cost per unit: "))

    new_data = pd.DataFrame([[date, product, quantity, price, cost]],
                            columns=["Date", "Product", "Quantity", "Price", "Cost"])
    
    new_data.to_csv(FILE_NAME, mode='a', header=False, index=False)
    print("Sale Recorded Successfully!\n")





# Revenue & Profit
def calculate_profit():
    df = pd.read_csv(FILE_NAME)

    if df.empty:
        print("No sales data available!\n")
        return

    # Convert columns to numeric
    df["Quantity"] = pd.to_numeric(df["Quantity"])
    df["Price"] = pd.to_numeric(df["Price"])
    df["Cost"] = pd.to_numeric(df["Cost"])

    df["Revenue"] = df["Quantity"] * df["Price"]
    df["Profit"] = df["Quantity"] * (df["Price"] - df["Cost"])

    print("\nTotal Revenue:", df["Revenue"].sum())
    print("Total Profit:", df["Profit"].sum(), "\n")



# Top Selling Products
def top_products():
    df = pd.read_csv(FILE_NAME)

    if df.empty:
        print("No sales data available!\n")
        return

    df["Quantity"] = pd.to_numeric(df["Quantity"])

    top = df.groupby("Product")["Quantity"].sum().sort_values(ascending=False)

    print("\nTop Selling Products:")
    print(top, "\n")


# Sales Trend Visualization
def sales_trend_pie():
    df = pd.read_csv(FILE_NAME)

    if df.empty:
        print("No sales data available!\n")
        return

    # Convert to numeric
    df["Quantity"] = pd.to_numeric(df["Quantity"])
    df["Price"] = pd.to_numeric(df["Price"])

    # Calculate revenue
    df["Revenue"] = df["Quantity"] * df["Price"]

    # Group by Date (Sales Trend)
    daily_sales = df.groupby("Date")["Revenue"].sum()

    if len(daily_sales) < 2:
        print("At least 2 days of data required for trend analysis!\n")
        return

#     plt.figure(figsize=(9, 9))

#     plt.pie(
#     daily_sales.values,
#     labels=daily_sales.index,
#     autopct='%1.1f%%',
#     startangle=400,
#     textprops={'fontsize': 6, 'color': 'black'}
# )

#     plt.title(
#     "Sales Trend (Day-wise Contribution)",
#     fontsize=24,
#     color='blue',
#     fontweight='bold'
# )

#     plt.show()
    plt.figure(figsize=(9, 6))

    plt.barh(
    daily_sales.index,
    daily_sales.values,
    color=plt.cm.Paired(np.arange(len(daily_sales))),
    

)
    plt.title("Sales Trend (Day-wise Contribution)", fontsize=16, fontweight="bold")
    plt.xlabel("Sales Amount", fontsize=12)
    plt.ylabel("Date", fontsize=12)

    plt.tight_layout()
    plt.show()




# Simple Sales Forecasting
def forecast_sales():
    df = pd.read_csv(FILE_NAME)

    if df.empty:
        print("No data available for forecasting!\n")
        return

    # Convert to numeric
    df["Quantity"] = pd.to_numeric(df["Quantity"])
    df["Price"] = pd.to_numeric(df["Price"])

    # Revenue calculation
    df["Revenue"] = df["Quantity"] * df["Price"]

    # Group by date
    daily_sales = df.groupby("Date")["Revenue"].sum().values

    if len(daily_sales) < 2:
        print("At least 2 days of data required for forecasting!\n")
        return

    # Calculate daily changes
    changes = []
    for i in range(1, len(daily_sales)):
        changes.append(daily_sales[i] - daily_sales[i - 1])

    # Average change
    avg_change = sum(changes) / len(changes)

    # Forecast next day
    forecast = daily_sales[-1] + avg_change

    print(f"Forecasted Sales for Next Day: {forecast:.2f}\n")




# Menu
while True:
    print("===== Sales Analyzer =====")
    print("1. Add Sale")
    print("2. Revenue & Profit")
    print("3. Top Products")
    print("4. Sales Trend")
    print("5. Forecast Sales")
    print("6. Exit")

    choice = int(input("Enter choice: "))

    if choice == 1:
        add_sale()
    elif choice == 2:
        calculate_profit()
    elif choice == 3:
        top_products()
    elif choice == 4:
        sales_trend_pie()
    elif choice == 5:
        forecast_sales()
    elif choice == 6:
        print("Exiting...")
        break
    else:
        print("Invalid choice!\n")