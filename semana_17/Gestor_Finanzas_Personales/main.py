# main.py

from logic import FinanceManager
from persistence import load_data, save_data
from interfaces import run_main_window

def main():
    # 1. Cargar datos desde archivo
    categories, transactions = load_data()

    # 2. Inicializar el gestor con los datos cargados
    manager = FinanceManager(categories, transactions)

    # 3. Ejecutar la ventana principal de la interfaz
    run_main_window(manager)

    # 4. Guardar los datos antes de salir
    save_data(manager.categories, manager.transactions)

if __name__ == "__main__":
    main()
