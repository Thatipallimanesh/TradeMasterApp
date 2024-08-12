import unittest
import psycopg2
from threading import Thread
from Data_layer import UserRepository, StockRepository, TransactionRepository, StockPriceHistoryRepository
from Service_layer import StockServiceImpl, AccountServiceImpl


class TestConcurrency(unittest.TestCase):

    def setUp(self):
        self.connection = psycopg2.connect(
            dbname='trade_master',
            user='postgres',
            password='123',
            host='localhost',
            port=5433
        )
        self.cursor = self.connection.cursor()
        self.user_repository = UserRepository(self.connection)
        self.stock_repository = StockRepository(self.connection)
        self.transaction_repository = TransactionRepository(self.connection)
        self.stock_price_history_repository = StockPriceHistoryRepository(self.connection)

        self.account_service = AccountServiceImpl(self.user_repository, self.transaction_repository)
        self.stock_service = StockServiceImpl(self.user_repository, self.stock_repository, self.transaction_repository,
                                              self.stock_price_history_repository)

        self.username = "concurrency_tester"
        self.password = "123"
        self.email = "tester@gmail.com"
        self.stock_symbol = 'IRFC'

    def tearDown(self):
        # Close the database connection
        self.cursor.close()
        self.connection.close()

    def buy_stock_concurrently(self, username, quantity):
        self.stock_service.buy_stock(username, self.stock_symbol, quantity)

    def sell_stock_concurrently(self, username, quantity):
        self.stock_service.sell_stock(username, self.stock_symbol, quantity)

    def test_concurrent_buy_orders(self):
        if self.account_service.get_user(self.username) is None:
            self.account_service.create_account(self.username, self.password, self.email)

        stock = self.stock_service.get_stock(self.stock_symbol)
        initial_quantity = stock[3]
        threads = []
        quantity = 10

        # Simulate 10 concurrent buy orders
        for i in range(10):
            thread1 = Thread(target=self.buy_stock_concurrently, args=(self.username, quantity))
            threads.append(thread1)
            thread2 = Thread(target=self.sell_stock_concurrently, args=(self.username, quantity))
            threads.append(thread2)

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        # Fetch the updated stock quantity
        updated_stock = self.stock_service.get_stock(self.stock_symbol)
        updated_quantity = updated_stock[3]

        # Assert that the quantity has decreased by the total amount bought
        self.assertEqual(updated_quantity, initial_quantity)

    # def test_concurrent_sell_orders(self):
    #     if self.account_service.get_user(self.username) is None:
    #         self.account_service.create_account(self.username, self.password, self.email)
    #
    #     stock = self.stock_service.get_stock(self.stock_symbol)
    #     initial_quantity = stock[3]
    #     threads = []
    #     quantity = 10
    #
    #     # Simulate 10 concurrent sell orders
    #     for i in range(10):
    #         thread = Thread(target=self.sell_stock_concurrently, args=(self.username, quantity))
    #         threads.append(thread)
    #         thread.start()
    #
    #     for thread in threads:
    #         thread.join()
    #
    #     # Fetch the updated stock quantity
    #     updated_stock = self.stock_service.get_stock(self.stock_symbol)
    #     updated_quantity = updated_stock[3]
    #
    #     # Assert that the quantity has increased by the total amount sold
    #     self.assertEqual(updated_quantity, initial_quantity + (10 * quantity))


if __name__ == '__main__':
    unittest.main()
