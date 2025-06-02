# data.py

import csv
import os
from student import Student

CSV_FILE = "students.csv"

def export_data(students_list):
    if not students_list:
        print("No hay datos para exportar.")
        return
    with open(CSV_FILE, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["name", "section", "spanish", "english", "social", "science"])
        writer.writeheader()
        for student in students_list:
            writer.writerow(student.to_dict())
    print("Datos exportados correctamente.")

def import_data():
    if not os.path.exists(CSV_FILE):
        print("No hay un archivo previamente exportado.")
        return []
    students = []
    with open(CSV_FILE, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            students.append(Student.from_dict(row))
    print("Datos importados correctamente.")
    return students
