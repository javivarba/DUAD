import csv
import os

students = []

def is_valid_grade(grade):
    try:
        value = float(grade)
        return 0 <= value <= 100
    except ValueError:
        return False




def input_student():
    name = input("Enter full name: ")
    section = input("Enter section (e.g., 11B): ")
    
    subjects = ['Spanish', 'English', 'Social Studies', 'Science']
    grades = {}

    for subject in subjects:
        while True:
            grade = input(f"Enter grade for {subject}: ")
            if is_valid_grade(grade):
                grades[subject] = float(grade)
                break
            else:
                print("Invalid grade. Please enter a number between 0 and 100.")

    student = {
        "name": name,
        "section": section,
        "grades": grades
    }
    students.append(student)
    print(f"Student {name} added successfully!\n")

def view_students():
    if not students:
        print("No student data available.\n")
        return
    for i, student in enumerate(students, start=1):
        print(f"{i}. {student['name']} | Section: {student['section']} | Grades: {student['grades']}")
    print()


def get_average(grades):
    return sum(grades.values()) / len(grades)

def view_top_3():
    if len(students) < 3:
        print("Not enough students to display top 3.\n")
        return

    sorted_students = sorted(students, key=lambda s: get_average(s["grades"]), reverse=True)
    print("Top 3 students by average grade:")
    for i, student in enumerate(sorted_students[:3], start=1):
        avg = get_average(student["grades"])
        print(f"{i}. {student['name']} - Average: {avg:.2f}")
    print()

def view_global_average():
    if not students:
        print("No students to calculate average.\n")
        return
    total = 0
    for student in students:
        total += get_average(student["grades"])
    print(f"Global average of all students: {total / len(students):.2f}\n")

def export_to_csv():
    if not students:
        print("No data to export.\n")
        return
    with open("students.csv", mode="w", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Section", "Spanish", "English", "Social Studies", "Science"])
        for student in students:
            row = [
                student["name"],
                student["section"],
                student["grades"]["Spanish"],
                student["grades"]["English"],
                student["grades"]["Social Studies"],
                student["grades"]["Science"]
            ]
            writer.writerow(row)
    print("Data exported successfully to 'students.csv'\n")

def import_from_csv():
    if not os.path.exists("students.csv"):
        print("No CSV file found. Please export data first.\n")
        return
    with open("students.csv", mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            student = {
                "name": row["Name"],
                "section": row["Section"],
                "grades": {
                    "Spanish": float(row["Spanish"]),
                    "English": float(row["English"]),
                    "Social Studies": float(row["Social Studies"]),
                    "Science": float(row["Science"])
                }
            }
            students.append(student)
    print("Data imported successfully from 'students.csv'\n")

def show_menu():
    print("==== Student Management System ====")
    print("1. Add new student")
    print("2. View all students")
    print("3. View top 3 students")
    print("4. View global average")
    print("5. Export data to CSV")
    print("6. Import data from CSV")
    print("0. Exit")

def main():
    while True:
        show_menu()
        choice = input("Choose an option: ")
        print()
        if choice == "1":
            input_student()
        elif choice == "2":
            view_students()
        elif choice == "3":
            view_top_3()
        elif choice == "4":
            view_global_average()
        elif choice == "5":
            export_to_csv()
        elif choice == "6":
            import_from_csv()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please try again.\n")

if __name__ == "__main__":
    main()
