class StockRepository:
    def __init__(self, connection):
        self.connection = connection

    def create_stock(self, symbol: str, price: float, quantity: int):
        with self.connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO stocks (symbol, price, quantity) VALUES (%s, %s, %s)",
                (symbol, price, quantity)
            )
        self.connection.commit()

    def get_stock(self, symbol: str):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM stocks WHERE symbol = %s", (symbol,))
            return cursor.fetchone()

    def update_stock(self, symbol: str, price: float = None, quantity: int = None):
        with self.connection.cursor() as cursor:
            if price is not None:
                cursor.execute(
                    "UPDATE stocks SET price = %s WHERE symbol = %s",
                    (price, symbol)
                )
            if quantity is not None:
                cursor.execute(
                    "UPDATE stocks SET quantity = %s WHERE symbol = %s",
                    (quantity, symbol)
                )
        self.connection.commit()

    def delete_stock(self, symbol: str):
        with self.connection.cursor() as cursor:
            cursor.execute("DELETE FROM stocks WHERE symbol = %s", (symbol,))
        self.connection.commit()

    def get_all_stocks(self):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM stocks")
            return cursor.fetchall()
