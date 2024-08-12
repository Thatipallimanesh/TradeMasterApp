class TradeMasterApp:
    def __init__(self, account_service, stock_service):
        self.account_service = account_service
        self.stock_service = stock_service

    @staticmethod
    def display_menu():
        print("Welcome to TradeMaster")
        print("1. Create Account")
        print("2. View Available Stocks")
        print("3. Buy Stock")
        print("4. Sell Stock")
        print("5. View Transaction History")
        print("6. Calculate Average Stock Value")
        print("7. Change password")
        print("8. Exit")

    def handle_user_input(self):
        while True:
            self.display_menu()
            choice = input("Enter your choice: ")
            if choice == '1':
                self.create_account()
            elif choice == '2':
                self.view_available_stocks()
            elif choice == '3':
                self.buy_stock()
            elif choice == '4':
                self.sell_stock()
            elif choice == '5':
                self.view_transaction_history()
            elif choice == '6':
                self.calculate_average_stock_value()
            elif choice == '7':
                self.change_password()
            elif choice == '8':
                print("Exiting TradeMaster. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")

    def create_account(self):
        username = input("Enter username: ")
        password = input("Enter password: ")
        email = input("Enter email: ")
        self.account_service.create_account(username, password, email)

    def view_available_stocks(self):
        stocks = self.stock_service.get_available_stocks()
        print("Available Stocks:")
        for stock in stocks:
            print(f"{stock[1]} - Price: {stock[2]} Quantity: {stock[3]}")

    def buy_stock(self):
        username = input("Enter your username: ")
        stock_symbol = input("Enter stock symbol to buy: ")
        quantity = int(input("Enter quantity to buy: "))
        self.stock_service.buy_stock(username, stock_symbol, quantity)

    def sell_stock(self):
        username = input("Enter your username: ")
        stock_symbol = input("Enter stock symbol to sell: ")
        quantity = int(input("Enter quantity to sell: "))
        self.stock_service.sell_stock(username, stock_symbol, quantity)

    def view_transaction_history(self):
        username = input("Enter your username: ")
        transactions = self.account_service.get_transaction_history(username)
        print(f"Transaction History for {username}:")
        for transaction in transactions:
            print(f"{transaction[4]}: {transaction[5]} {transaction[3]} shares of {transaction[2]}")

    def calculate_average_stock_value(self):
        stock_symbol = input("Enter stock symbol: ")
        from_year = int(input("Enter from year: "))
        to_year = int(input("Enter to year: "))
        average_value = self.stock_service.calculate_average_stock_value(stock_symbol, from_year, to_year)
        print(f"Average value of {stock_symbol} from {from_year} to {to_year} is {average_value}")

    def change_password(self):
        username = input("Enter username: ")
        email = input("Enter your email id linked to the account: ")
        new_password = input("Enter new password")
        self.account_service.change_password(username, email, new_password)
