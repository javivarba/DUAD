
# Cree un programa que me permita ingresar información de n cantidad de videojuegos y los guarde en un archivo csv.

import csv

def saved_videogame ():
    n = int (input("How Many Video Games Would you like to register?"))


    with open ('videogames.csv', mode= 'w', newline= '', encoding= 'utf-8') as archive:
        writer = csv.writer(archive)

        writer.writerow (['name', 'type', 'developed by', 'rate'])

        for i in range (n):
            print (f"\nVideogame {i + 1}:")
            name = input ("Name: ")
            type = input ("Type: ")
            developed_by = input ("Developed by: ")
            rate = input ("Rate: ")

            writer.writerow([name, type, developed_by, rate])

        print ("\n Data saved in 'videogames.csv' successful")

saved_videogame ()