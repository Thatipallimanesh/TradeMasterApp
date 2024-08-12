class TransactionRepository:
    def __init__(self, connection):
        self.connection = connection

    def create_transaction(self, transaction):
        with self.connection.cursor() as cursor:
            cursor.execute(
                """INSERT INTO transactions (username, stock_symbol, quantity, date, transaction_type) 
                VALUES (%s, %s, %s, %s, %s)""",
                (transaction['username'], transaction['stock_symbol'], transaction['quantity'], transaction['date'], transaction['transaction_type'])
            )
        self.connection.commit()

    def get_transactions_by_username(self, username: str):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM transactions WHERE username = %s", (username,))
            return cursor.fetchall()

    # def get_buy_transactions_by_username(self, username):
    #     with self.connection.cursor() as cursor:
    #         cursor.execute("SELECT * FROM transactions WHERE username = %s AND transactionType = 'BUY'", (username, ))
    #         return cursor.fetchall()
    #
    # def get_sell_transactions_by_username(self, username):
    #     with self.connection.cursor() as cursor:
    #         cursor.execute("SELECT * FROM transactions WHERE username = %s AND transactionType = 'BUY'", (username, ))
    #         return cursor.fetchall()

