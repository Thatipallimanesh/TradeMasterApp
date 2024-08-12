class StockPriceHistoryRepository:
    def __init__(self, connection):
        self.connection = connection

    def add_stock_price_history(self, stock_symbol: str, price: float, year: int):
        with self.connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO stock_price_history (stockSymbol, price, year) VALUES (%s, %s, %s)",
                (stock_symbol, price, year)
            )
        self.connection.commit()

    def get_stock_price_history(self, stock_symbol: str, from_year: int, to_year: int):
        with self.connection.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM stock_price_history WHERE stock_symbol = %s AND year BETWEEN %s AND %s",
                (stock_symbol, from_year, to_year)
            )
            return cursor.fetchall()
