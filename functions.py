import pandas as pd 
import yfinance as yf
import os
import csv

def register_user(email, password, user_file="users.csv"):
    """Registers a new user with email and password."""
    if not os.path.exists(user_file):
        with open(user_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["email", "password"])
    with open(user_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([email, password])
    print("User registered successfully.")

# Authenticate a user
def authenticate_user(email, password, user_file="users.csv"):
    """Authenticates user login credentials."""
    if not os.path.exists(user_file):
        print("No registered users found.")
        return False
    with open(user_file, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["email"] == email and row["password"] == password:
                return True
    return False

# Fetch historical closing prices
def get_closing_prices(ticker, start_date, end_date):
    """Fetches historical closing prices for the given stock ticker."""
    try:
        stock_data = yf.download(ticker, start=start_date, end=end_date)
        closing_prices = stock_data["Close"]
        if closing_prices.empty:
            print("No data found for the given period.")
            return None
        return closing_prices
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

# Analyze closing prices
def analyze_closing_prices(data):
    """Analyzes closing prices."""
    analysis = {
        "average": data.mean(),
        "percentage_change": ((data[-1] - data[0]) / data[0]) * 100,
        "highest": data.max(),
        "lowest": data.min(),
    }
    return analysis

# Save data to CSV
def save_to_csv(data, filename):
    """Saves user interactions to a CSV file."""
    if not os.path.exists(filename):
        pd.DataFrame(columns=["email", "ticker", "analysis"]).to_csv(filename, index=False)
    df = pd.DataFrame([data])
    df.to_csv(filename, mode='a', header=False, index=False)

# Read data from CSV
def read_from_csv(filename):
    """Reads and displays stored data from the CSV file."""
    if not os.path.exists(filename):
        print("No data found.")
        return None
    return pd.read_csv(filename)
