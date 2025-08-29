# interfaces.py

import PySimpleGUI as sg

def run_main_window(manager):
    sg.theme("DarkBlue14")

    def update_table(window):
        data = [
            [t.title, t.amount, t.category, "Income" if t.is_income else "Expense"]
            for t in manager.get_transactions()
        ]
        window["-TABLE-"].update(values=data)

    layout = [
        [sg.Text("Personal Finance Manager", font=("Arial", 16))],
        [sg.Table(
            values=[],
            headings=["Title", "Amount", "Category", "Type"],
            key="-TABLE-",
            auto_size_columns=True,
            justification="left",
            num_rows=10,
            enable_events=False
        )],
        [
            sg.Button("Add Category"),
            sg.Button("Add Income"),
            sg.Button("Add Expense"),
            sg.Button("Exit")
        ]
    ]

    window = sg.Window("Finance Manager", layout, finalize=True)
    update_table(window)

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED or event == "Exit":
            break

        elif event == "Add Category":
            add_category_popup(manager)

        elif event == "Add Income":
            try:
                add_transaction_popup(manager, is_income=True)
            except ValueError as e:
                sg.popup_error(str(e))

        elif event == "Add Expense":
            try:
                add_transaction_popup(manager, is_income=False)
            except ValueError as e:
                sg.popup_error(str(e))

        update_table(window)

    window.close()

def add_category_popup(manager):
    layout = [
        [sg.Text("Category Name:"), sg.Input(key="-CATEGORY_NAME-")],
        [sg.Button("Add"), sg.Button("Cancel")]
    ]

    window = sg.Window("Add Category", layout)
    while True:
        event, values = window.read()
        if event == "Cancel" or event == sg.WINDOW_CLOSED:
            break
        elif event == "Add":
            try:
                manager.add_category(values["-CATEGORY_NAME-"])
                break
            except ValueError as e:
                sg.popup_error(str(e))
    window.close()

def add_transaction_popup(manager, is_income: bool):
    categories = manager.get_categories()
    if not categories:
        raise ValueError("You must add at least one category before adding a transaction.")

    layout = [
        [sg.Text("Title:"), sg.Input(key="-TITLE-")],
        [sg.Text("Amount:"), sg.Input(key="-AMOUNT-")],
        [sg.Text("Category:"), sg.Combo(categories, key="-CATEGORY-", readonly=True)],
        [sg.Button("Add"), sg.Button("Cancel")]
    ]

    window = sg.Window("Add Income" if is_income else "Add Expense", layout)
    while True:
        event, values = window.read()
        if event == "Cancel" or event == sg.WINDOW_CLOSED:
            break
        elif event == "Add":
            try:
                title = values["-TITLE-"]
                amount = float(values["-AMOUNT-"])
                category = values["-CATEGORY-"]
                manager.add_transaction(title, amount, category, is_income)
                break
            except ValueError as e:
                sg.popup_error(str(e))
            except Exception:
                sg.popup_error("Invalid input.")
    window.close()
