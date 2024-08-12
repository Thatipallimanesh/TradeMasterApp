class AccountServiceImpl:
    def __init__(self, user_repository, transaction_repository):
        self.user_repository = user_repository
        self.transaction_repository = transaction_repository

    def create_account(self, username, password, email):
        if self.get_user(username) is not None:
            print(f"Username '{username}' already exists. Please choose a different username.")
            return
        self.user_repository.create_user(username, password, email)
        print(f"Account created for {username}.")

    def get_user(self, username):
        return self.user_repository.get_user(username)

    def get_transaction_history(self, username: str):
        user = self.get_user(username)
        if user is None:
            print("Please enter correct username")
            return
        return self.transaction_repository.get_transactions_by_username(username)

    def change_password(self, username, email, new_password):
        user = self.get_user(username)
        if user is None:
            print("Please enter correct username")
            return
        if email != user[3]:
            print("Please enter correct email id")
            return
        self.user_repository.update_user(username, new_password)

    def delete_account(self, username, password):
        user = self.get_user(username)
        if user is None:
            print("Please enter correct username")
            return
        if user[2] != password:
            print("Please enter correct password")
            return
        self.user_repository.delete_user(username)
        print("Account deleted")