import psycopg2
from Data_layer import UserRepository, StockRepository, TransactionRepository, StockPriceHistoryRepository
from Service_layer import AccountServiceImpl, StockServiceImpl
from Client_tier import TradeMasterApp

if __name__ == "__main__":
    # Database configuration
    DB_CONFIG = {
        'dbname': 'trade_master',
        'user': 'postgres',
        'password': '123',
        'host': 'localhost',
        'port': 5433
    }

    # Connect to the PostgresSQL database
    connection = psycopg2.connect(**DB_CONFIG)

    cursor = connection.cursor()
    with open('database/schema.sql', 'r') as sql_file:
        cursor.execute(sql_file.read())
    connection.commit()
    cursor.close()

    # Initialize repositories
    user_repo = UserRepository(connection)
    stock_repo = StockRepository(connection)
    transaction_repo = TransactionRepository(connection)
    stock_price_history_repo = StockPriceHistoryRepository(connection)

    # Initialize services
    account_service = AccountServiceImpl(user_repo, transaction_repo)
    stock_service = StockServiceImpl(user_repo, stock_repo, transaction_repo, stock_price_history_repo)

    # Initialize and run the application
    app = TradeMasterApp(account_service, stock_service)
    app.handle_user_input()

    # Close the database connection
    connection.close()
