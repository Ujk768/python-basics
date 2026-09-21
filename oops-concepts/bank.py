class BankAccount:
    def __init__(self, owner: str, balance: float):
        self.owner = owner
        self.__balance = balance  # Private attribute

    def deposit(self, amount: float):
        if amount > 0:
            self.__balance += amount

    # Getter property
    @property
    def balance(self) -> float:
        return self.__balance

account = BankAccount("Alice", 100.0)
account.deposit(50.0)
print(account.balance)  # 150.0
# account.__balance  # Raises AttributeError