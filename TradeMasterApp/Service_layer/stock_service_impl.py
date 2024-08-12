from datetime import datetime
from threading import Lock


class StockServiceImpl:
    def __init__(self, user_repository, stock_repository, transaction_repository, stock_price_history_repository):
        self.user_repository = user_repository
        self.stock_repository = stock_repository
        self.transaction_repository = transaction_repository
        self.stock_price_history_repository = stock_price_history_repository
        self.lock = Lock()

    def buy_stock(self, username: str, stock_symbol: str, quantity: int):
        user = self.user_repository.get_user(username)
        if user is None:
            print("Please enter correct username")
            return

        stock = self.stock_repository.get_stock(stock_symbol)
        if stock is None:
            print("invalid stock symbol")
            return
        if stock[3] >= quantity:
            with self.lock:
                self.stock_repository.update_stock(stock_symbol, quantity=stock[3] - quantity)
                self.transaction_repository.create_transaction({
                    'username': username,
                    'stock_symbol': stock_symbol,
                    'quantity': quantity,
                    'date': datetime.now(),
                    'transaction_type': 'BUY'
                })
                print(f"Bought {quantity} shares of {stock_symbol}.")
        else:
            print(f"Insufficient quantity for stock {stock_symbol}")
            return

    def sell_stock(self, username: str, stock_symbol: str, quantity: int):
        user = self.user_repository.get_user(username)
        if user is None:
            print("Please enter correct username")
            return

        stock = self.stock_repository.get_stock(stock_symbol)
        if stock is None:
            print(f"Stock {stock_symbol} not found")
            return
        else:
            with self.lock:
                user_transactions = self.transaction_repository.get_transactions_by_username(username)
                quantity_owned = 0
                for t in user_transactions:
                    if t[5] == 'BUY':
                        quantity_owned += t[3]
                    elif t[5] == 'SELL':
                        quantity_owned -= t[3]
                if quantity_owned >= quantity:
                    self.stock_repository.update_stock(stock_symbol, quantity=stock[3] + quantity)
                    self.transaction_repository.create_transaction({
                        'username': username,
                        'stock_symbol': stock_symbol,
                        'quantity': quantity,
                        'date': datetime.now(),
                        'transaction_type': 'SELL'
                    })
                    print(f"Sold {quantity} shares of {stock_symbol}.")
                else:
                    print("Insufficient quantity...")
                    return

    def get_available_stocks(self):
        return self.stock_repository.get_all_stocks()

    def get_stock(self, stock_symbol):
        return self.stock_repository.get_stock(stock_symbol)

    def calculate_average_stock_value(self, stock_symbol: str, from_year: int, to_year: int):
        stock = self.stock_repository.get_stock(stock_symbol)
        if stock:
            history = self.stock_price_history_repository.get_stock_price_history(stock_symbol, from_year, to_year)
            if history:
                return sum(record[2] for record in history) / len(history)
        else:
            print(f"Stock {stock_symbol} not found")
            return
