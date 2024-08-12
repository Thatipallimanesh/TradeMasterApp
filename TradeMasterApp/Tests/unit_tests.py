import unittest
import psycopg2
from Data_layer import UserRepository, StockRepository, TransactionRepository, StockPriceHistoryRepository
from Service_layer import StockServiceImpl, AccountServiceImpl


class TestTradeMaster(unittest.TestCase):

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
        self.stock_service = StockServiceImpl(self.user_repository, self.stock_repository, self.transaction_repository, self.stock_price_history_repository)

        self.username = "unit_tester"
        self.password = "123"
        self.email = "tester@gmail.com"
        self.stock_symbol = 'IREDA'

    def tearDown(self):
        # Close the database connection
        self.cursor.close()
        self.connection.close()

    def test_create_account(self):
        # user = self.account_service.get_user(self.username)
        # if user is not None:
        #     self.account_service.delete_account(self.username, user[2])
        self.account_service.create_account(self.username, self.password, self.email)
        user = self.account_service.get_user(self.username)
        self.assertIsNotNone(user)
        self.assertEqual(user[1], self.username)
        self.assertEqual(user[2], self.password)

    def test_buy_stock(self):
        # create user if not present
        if self.account_service.get_user(self.username) is None:
            self.account_service.create_account(self.username, self.password, self.email)

        stock = self.stock_service.get_stock(self.stock_symbol)
        initial_quantity = stock[3]

        # Perform the buy operation
        quantity = 10
        self.stock_service.buy_stock(self.username, self.stock_symbol, quantity)

        updated_stock = self.stock_service.get_stock(self.stock_symbol)
        updated_quantity = updated_stock[3]

        # Assert that the quantity has decreased by the amount bought
        self.assertEqual(updated_quantity, initial_quantity - quantity)

        trans = self.account_service.get_transaction_history(self.username)
        last_transaction = trans[-1]
        self.assertEqual(last_transaction[2], self.stock_symbol)
        self.assertEqual(last_transaction[3], quantity)
        self.assertEqual(last_transaction[5], 'BUY')

    def test_sell_stock(self):
        # create user if not present
        if self.account_service.get_user(self.username) is None:
            self.account_service.create_account(self.username, self.password, self.email)

        stock = self.stock_service.get_stock(self.stock_symbol)
        initial_quantity = stock[3]

        # Perform the sell operation
        quantity = 5
        self.stock_service.sell_stock(self.username, self.stock_symbol, quantity)

        # Fetch the updated stock quantity
        updated_stock = self.stock_service.get_stock(self.stock_symbol)
        updated_quantity = updated_stock[3]

        # Assert that the quantity has increased by the amount sold
        self.assertEqual(updated_quantity, initial_quantity + quantity)
        trans = self.account_service.get_transaction_history(self.username)
        last_transaction = trans[-1]
        self.assertEqual(last_transaction[2], self.stock_symbol)
        self.assertEqual(last_transaction[3], quantity)
        self.assertEqual(last_transaction[5], 'SELL')


if __name__ == '__main__':
    unittest.main()
