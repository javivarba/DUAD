
# actions.py

def input_student(students):
    print("Enter student information:")
    name = input("Full name: ").strip()
    section = input("Section (e.g., 11B): ").strip()

    grades = {}
    subjects = ["Spanish", "English", "Social Studies", "Science"]

    for subject in subjects:
        while True:
            try:
                grade = float(input(f"Grade for {subject}: "))
                if 0 <= grade <= 100:
                    grades[subject.lower()] = grade
                    break
                else:
                    print("Grade must be between 0 and 100.")
            except ValueError:
                print("Invalid input. Please enter a number.")

    student = {
        "name": name,
        "section": section,
        **grades
    }
    students.append(student)
    print("Student added successfully!\n")

def view_students(students):
    if not students:
        print("No students registered yet.\n")
        return

    print("=== Student List ===")
    for i, s in enumerate(students, start=1):
        print(f"{i}. {s['name']} - Section: {s['section']}")
        print(f"   Spanish: {s['spanish']} | English: {s['english']} | Social Studies: {s['social studies']} | Science: {s['science']}\n")

def view_top_3(students):
    if len(students) < 1:
        print("Not enough students to evaluate.\n")
        return

    sorted_students = sorted(
        students,
        key=lambda s: (s['spanish'] + s['english'] + s['social studies'] + s['science']) / 4,
        reverse=True
    )

    print("=== Top 3 Students ===")
    for i, s in enumerate(sorted_students[:3], start=1):
        avg = (s['spanish'] + s['english'] + s['social studies'] + s['science']) / 4
        print(f"{i}. {s['name']} - Average: {avg:.2f}")
    print()

def view_global_average(students):
    if not students:
        print("No students to calculate average.\n")
        return

    total = 0
    for s in students:
        avg = (s['spanish'] + s['english'] + s['social studies'] + s['science']) / 4
        total += avg

    global_avg = total / len(students)
    print(f"Global average of all students: {global_avg:.2f}\n")
