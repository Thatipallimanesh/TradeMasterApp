class UserRepository:
    def __init__(self, connection):
        self.connection = connection

    def create_user(self, username: str, password: str, email: str):
        with self.connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO users (username, password, email) VALUES (%s, %s, %s)",
                (username, password, email)
            )
        self.connection.commit()

    def get_user(self, username: str):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            return cursor.fetchone()

    def update_user(self, username, password):
        with self.connection.cursor() as cursor:
            cursor.execute(
                "UPDATE users SET password = %s WHERE username = %s",
                (password, username)
            )
        self.connection.commit()

    def delete_user(self, username: str):
        with self.connection.cursor() as cursor:
            cursor.execute("""
            DELETE FROM transactions WHERE username = %s;
            DELETE FROM users WHERE username = %s;""", (username, username))
        self.connection.commit()


