# menu.py

from actions import input_student, view_students, view_top_3, view_global_average
from data import export_to_csv, import_from_csv

def show_menu(students):
    while True:
        print("\n===== Student Management Menu =====")
        print("1. Add new student")
        print("2. View all students")
        print("3. View top 3 students")
        print("4. View global average")
        print("5. Export data to CSV")
        print("6. Import data from CSV")
        print("0. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            input_student(students)
        elif choice == "2":
            view_students(students)
        elif choice == "3":
            view_top_3(students)
        elif choice == "4":
            view_global_average(students)
        elif choice == "5":
            export_to_csv(students, "students.csv")
        elif choice == "6":
            import_from_csv(students, "students.csv")
        elif choice == "0":
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")

