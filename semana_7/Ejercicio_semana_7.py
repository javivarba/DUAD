def show_menu ():
    print("\nCalculator - Current Number: ", current_number)
    print("1. Sum")
    print("2. Rest")
    print("3. Multiplication")
    print("4. Division")
    print("5. clear")

def get_number ():
    while True:
        try:
            return float (input ("Enter your number: "))
        except ValueError:
            print ("Error: Please enter a valid number")

current_number = 0

while True:
    show_menu ()

    option = input ("Choose and option:")

    if option == '6':
        print(" Leaving the calculator. Goodbye!")
        break

    if option not in ('1', '2', '3', '4', '5'):
        print("Error: Option not valid. Please try again")
        continue
    if option== '5':
        current_number = 0
        print (" Clearing Results to 0.")
        continue
    new_number = get_number ()

    if option == '1':
        current_number += new_number
    elif option == '2':
        current_number -= new_number
    elif option == '3':
        current_number *= new_number
    elif option == '4':
        if new_number == 0:
            print( "Error: Unable to divide by zero.")
        else:
            current_number /= new_number
    
    print("Results are: ", current_number)