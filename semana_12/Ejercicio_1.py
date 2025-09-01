# Ejercicio 1

#Parent Class

class BankAccount:
    def __init__(self, initial_balance=0):
        self.balance = initial_balance

    def deposit (self, amount):
        if amount > 0:
            self.balance += amount
            print(f"Deposited $ {amount}. New Balance is ${self.balance}.")
        else:
            print("Deposit amount must be positive.")

    def withdraw (self, amount):
        if amount <= self.balance:
            self.balance -= amount
            print(f"Withdrew ${amount}. New Balance is ${self.balance}.")



# Child Class

class SavingsAccount(BankAccount):
    def __init__(self, initial_balance=0, min_balance=100):
        super().__init__(initial_balance)
        self.min_balance = min_balance

    def withdraw(self, amount):
        if self.balance - amount >= self.min_balance:
           self.balance -= amount
           print (f"Withdrew ${amount}. New Balance is ${self.balance}.")
        else:
            print (f" Cannot withdraw ${amount}. Balance would fall below minimum allowed (${self.min_balance}).")

