# data.py

import csv
import os

def export_to_csv(students, filename="students.csv"):
    if not students:
        print("No students to export.\n")
        return

    fieldnames = ["name", "section", "spanish", "english", "social studies", "science"]

    try:
        with open(filename, mode="w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for student in students:
                writer.writerow(student)
        print(f"Data successfully exported to '{filename}'.\n")
    except Exception as e:
        print(f"Error exporting data: {e}\n")

def import_from_csv(students, filename="students.csv"):
    if not os.path.exists(filename):
        print(f"CSV file '{filename}' not found. Nothing to import.\n")
        return

    try:
        with open(filename, mode="r", newline="") as file:
            reader = csv.DictReader(file)
            imported = 0
            for row in reader:
                student = {
                    "name": row["name"],
                    "section": row["section"],
                    "spanish": float(row["spanish"]),
                    "english": float(row["english"]),
                    "social studies": float(row["social studies"]),
                    "science": float(row["science"])
                }
                students.append(student)
                imported += 1
        print(f"Successfully imported {imported} students from '{filename}'.\n")
    except Exception as e:
        print(f"Error importing data: {e}\n")
