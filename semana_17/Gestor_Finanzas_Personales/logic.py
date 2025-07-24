# logic.py

class Category:
    def __init__(self, name: str):
        self.name = name.strip()

    def __eq__(self, other):
        if isinstance(other, Category):
            return self.name.lower() == other.name.lower()
        return False

    def __repr__(self):
        return f"Category(name='{self.name}')"

class Transaction:
    def __init__(self, title: str, amount: float, category: str, is_income: bool):
        self.title = title.strip()
        self.amount = amount
        self.category = category.strip()
        self.is_income = is_income

    def __repr__(self):
        type_str = "Income" if self.is_income else "Expense"
        return f"{type_str}(title='{self.title}', amount={self.amount}, category='{self.category}')"

class FinanceManager:
    def __init__(self, categories=None, transactions=None):
        self.categories = categories if categories else []
        self.transactions = transactions if transactions else []

    def add_category(self, category_name: str):
        category_name = category_name.strip()
        if not category_name:
            raise ValueError("Category name cannot be empty.")
        new_category = Category(category_name)
        if new_category not in self.categories:
            self.categories.append(new_category)

    def add_transaction(self, title: str, amount: float, category_name: str, is_income: bool):
        if not self.categories:
            raise ValueError("No categories available.")
        if not title.strip():
            raise ValueError("Title cannot be empty.")
        if amount <= 0:
            raise ValueError("Amount must be positive.")
        if category_name.strip() not in [c.name for c in self.categories]:
            raise ValueError("Category does not exist.")

        transaction = Transaction(title, amount, category_name, is_income)
        self.transactions.append(transaction)

    def get_transactions(self):
        return self.transactions

    def get_categories(self):
        return [c.name for c in self.categories]
