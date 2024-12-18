import datetime
from functions import *


def main():
    user_file = "users.csv"
    data_file = "user_data.csv"

    print("Welcome to the Stock Selection Tool!")

    # User Registration and Login
    while True:
        choice = input("Choose an option: [1] Register [2] Login [3] Exit: ")
        if choice == "1":
            email = input("Enter your email: ")
            password = input("Enter your password: ")
            register_user(email, password, user_file)
            print("Registration successful!")
        elif choice == "2":
            email = input("Enter your email: ")
            password = input("Enter your password: ")
            if authenticate_user(email, password, user_file):
                print("Login successful!")
                break
            else:
                print("Invalid email or password. Try again.")
        elif choice == "3":
            print("Goodbye!")
            return
        else:
            print("Invalid choice. Please try again.")

    # Main Menu
    while True:
        print("\nMenu:")
        print("[1] Analyze a stock")
        print("[2] View saved data")
        print("[3] Exit")
        user_choice = input("Choose an option: ")

        if user_choice == "1":
            # Stock Analysis
            ticker = input("Enter stock ticker (e.g., TSLA): ")
            start_date = input("Enter start date (YYYY-MM-DD): ")
            end_date = input("Enter end date (YYYY-MM-DD): ")

            # Validate dates
            try:
                start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
                end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
                if start_date > end_date:
                    raise ValueError("Start date must be before end date.")
            except ValueError as e:
                print(f"Invalid date format or range: {e}")
                continue

            # Fetch and analyze stock data
            closing_prices = get_closing_prices(ticker, start_date, end_date)

            if closing_prices is not None and not closing_prices.empty:
                print("\nClosing Prices:")
                print(closing_prices)

                # Perform analysis
                try:
                    analysis = analyze_closing_prices(closing_prices)
                    print("\nAnalysis Result:")
                    for key, value in analysis.items():
                        print(f"{key.capitalize()}: {value}")

                    # Save analysis to CSV
                    save_to_csv(
                        {
                            "email": email,
                            "ticker": ticker,
                            **analysis,
                        },
                        data_file,
                    )
                    print("Analysis saved successfully.")
                except Exception as e:
                    print(f"Error during analysis: {e}")
            else:
                print("No closing prices retrieved. Please check the ticker and date range.")

        elif user_choice == "2":
            # View Saved Data
            saved_data = read_from_csv(data_file)
            if saved_data is not None and not saved_data.empty:
                print("\nSaved Data:")
                print(saved_data)
            else:
                print("No saved data found.")

        elif user_choice == "3":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()


