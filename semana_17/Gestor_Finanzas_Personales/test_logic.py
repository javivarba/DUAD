# test_logic.py

import unittest
from logic import Category, Transaction, FinanceManager

class TestFinanceManager(unittest.TestCase):

    def setUp(self):
        self.manager = FinanceManager()

    def test_add_category_success(self):
        self.manager.add_category("Food")
        self.assertIn("Food", self.manager.get_categories())

    def test_add_duplicate_category(self):
        self.manager.add_category("Travel")
        self.manager.add_category("travel")  # Case insensitive
        self.assertEqual(len(self.manager.get_categories()), 1)

    def test_add_empty_category(self):
        with self.assertRaises(ValueError):
            self.manager.add_category("  ")

    def test_add_transaction_success(self):
        self.manager.add_category("Salary")
        self.manager.add_transaction("Paycheck", 1000.0, "Salary", True)
        self.assertEqual(len(self.manager.get_transactions()), 1)

    def test_add_transaction_without_categories(self):
        with self.assertRaises(ValueError):
            self.manager.add_transaction("Bonus", 500.0, "Salary", True)

    def test_add_transaction_invalid_amount(self):
        self.manager.add_category("Misc")
        with self.assertRaises(ValueError):
            self.manager.add_transaction("Bad", -10.0, "Misc", False)

    def test_add_transaction_invalid_category(self):
        self.manager.add_category("Utilities")
        with self.assertRaises(ValueError):
            self.manager.add_transaction("Water bill", 50.0, "Food", False)

    def test_transaction_data_integrity(self):
        self.manager.add_category("Freelance")
        self.manager.add_transaction("Project A", 200.0, "Freelance", True)
        t = self.manager.get_transactions()[0]
        self.assertEqual(t.title, "Project A")
        self.assertEqual(t.amount, 200.0)
        self.assertTrue(t.is_income)

if __name__ == "__main__":
    unittest.main()
