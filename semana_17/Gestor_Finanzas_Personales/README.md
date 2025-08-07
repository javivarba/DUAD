# Personal Finance Manager

A simple personal finance management application built with Python using a graphical interface.

## 🧾 Project Description

This application allows users to:

- Add income and expense transactions
- Organize transactions by category
- View a table with all financial movements
- Persist data automatically (JSON files)
- Practice modularity, object-oriented programming, file handling, and GUI design

## 🖼 Built With

- Python 3.10+
- [PySimpleGUI](https://pysimplegui.readthedocs.io/) – For the user interface
- Standard libraries: `os`, `json`, `unittest`

## 🚀 How to Run the Application

1. Clone or download the repository.
2. Navigate to the project folder.

### ✅ Install dependencies

> ⚠️ **Important: PySimpleGUI must be installed from a private index.**

```bash
python -m pip uninstall PySimpleGUI
python -m pip cache purge

python -m pip install --upgrade --extra-index-url https://PySimpleGUI.net/install PySimpleGUI
```

### ▶️ Run the app

```bash
python main.py
```

---

## 📁 Project Structure

```
/Gestor_Finanzas_Personales
│
├── main.py                # Entry point
├── logic.py               # Business logic and data models
├── persistence.py         # File loading and saving
├── interfaces.py          # GUI (PySimpleGUI)
├── constants.py           # Reusable constants
├── test_logic.py          # Unit tests
└── /data/                 # JSON data files (auto-generated)
    ├── categories.json
    └── transactions.json
```

---

## 🧪 Running Tests

```bash
python test_logic.py
```

---

## 🔒 License

This project is part of a Full Stack Developer training course. Educational use only.