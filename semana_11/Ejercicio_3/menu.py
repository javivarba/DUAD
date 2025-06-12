# Menu.py


def print_menu():
    print("\n--- Sistema de Control de Estudiantes ---")
    print("1. Ingresar estudiante")
    print("2. Ver todos los estudiantes")
    print("3. Ver top 3 estudiantes")
    print("4. Ver promedio general")
    print("5. Exportar datos")
    print("6. Importar datos")
    print("0. Salir")

def get_menu_option():
    while True:
        try:
            option = int(input("Seleccione una opción: "))
            if 0 <= option <= 6:
                return option
            else:
                print("Opción inválida.")
        except ValueError:
            print("Debe ingresar un número.")
