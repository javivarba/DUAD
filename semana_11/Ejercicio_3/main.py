# main.py

from menu import print_menu, get_menu_option
import actions
import data

def main():
    students = []

    while True:
        print_menu()
        option = get_menu_option()

        if option == 1:
            actions.create_student(students)
        elif option == 2:
            actions.show_all_students(students)
        elif option == 3:
            actions.show_top_students(students)
        elif option == 4:
            actions.show_overall_average(students)
        elif option == 5:
            data.export_data(students)
        elif option == 6:
            students = data.import_data()
        elif option == 0:
            print("Saliendo del sistema...")
            break

if __name__ == "__main__":
    main()

