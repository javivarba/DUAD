# Intente accesar a una variable definida dentro de una función desde afuera
cars = 5

def new_cars():
    global cars
    cars += 1
    print (f"Cars in the function: {cars}")


new_cars()
print (f"Cars out the function {cars}")

# Intente accesar a una variable global desde una función y cambiar su valor
cars = 5

def new_cars():
    global cars
    cars += 1
    print (f"Cars in the function: {cars}")


new_cars()
print (f"Cars out the function {cars}")