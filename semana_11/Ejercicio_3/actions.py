# actions.py

# actions.py
from student import Student

def input_valid_score(subject):
    while True:
        try:
            score = float(input(f"Ingrese la nota de {subject}: "))
            if 0 <= score <= 100:
                return score
            else:
                print("La nota debe estar entre 0 y 100.")
        except ValueError:
            print("Debe ingresar un número válido.")

def create_student(students_list):
    name = input("Nombre completo: ")
    section = input("Sección (ej: 11B): ")
    spanish = input_valid_score("Español")
    english = input_valid_score("Inglés")
    social = input_valid_score("Sociales")
    science = input_valid_score("Ciencias")
    student = Student(name, section, spanish, english, social, science)
    students_list.append(student)

def show_all_students(students_list):
    if not students_list:
        print("No hay estudiantes ingresados.")
        return
    for student in students_list:
        print(f"{student.name} | {student.section} | Español: {student.spanish} | Inglés: {student.english} | Sociales: {student.social} | Ciencias: {student.science} | Promedio: {student.get_average():.2f}")

def show_top_students(students_list):
    top = sorted(students_list, key=lambda s: s.get_average(), reverse=True)[:3]
    print("Top 3 estudiantes:")
    for student in top:
        print(f"{student.name} - Promedio: {student.get_average():.2f}")

def show_overall_average(students_list):
    if not students_list:
        print("No hay datos.")
        return
    total = sum(student.get_average() for student in students_list)
    avg = total / len(students_list)
    print(f"Promedio general de todos los estudiantes: {avg:.2f}")
