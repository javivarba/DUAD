# persistence.py

import json
import os
from logic import Category, Transaction

DATA_FOLDER = "data"
CATEGORIES_FILE = os.path.join(DATA_FOLDER, "categories.json")
TRANSACTIONS_FILE = os.path.join(DATA_FOLDER, "transactions.json")

def load_data():
    # Crea la carpeta si no existe
    if not os.path.exists(DATA_FOLDER):
        os.makedirs(DATA_FOLDER)

    # Cargar categorías
    if os.path.exists(CATEGORIES_FILE):
        with open(CATEGORIES_FILE, "r") as f:
            category_names = json.load(f)
        categories = [Category(name) for name in category_names]
    else:
        categories = []

    # Cargar transacciones
    if os.path.exists(TRANSACTIONS_FILE):
        with open(TRANSACTIONS_FILE, "r") as f:
            transactions_data = json.load(f)
        transactions = [
            Transaction(
                t["title"],
                t["amount"],
                t["category"],
                t["is_income"]
            )
            for t in transactions_data
        ]
    else:
        transactions = []

    return categories, transactions

def save_data(categories, transactions):
    # Asegurar carpeta
    if not os.path.exists(DATA_FOLDER):
        os.makedirs(DATA_FOLDER)

    # Guardar categorías
    category_names = [c.name for c in categories]
    with open(CATEGORIES_FILE, "w") as f:
        json.dump(category_names, f, indent=4)

    # Guardar transacciones
    transactions_data = [
        {
            "title": t.title,
            "amount": t.amount,
            "category": t.category,
            "is_income": t.is_income
        }
        for t in transactions
    ]
    with open(TRANSACTIONS_FILE, "w") as f:
        json.dump(transactions_data, f, indent=4)
