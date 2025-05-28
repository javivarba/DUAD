
import random

secret_number = random.randint (1,10)

guess_number = False

while not guess_number :

    intento=int(input("Enter a number between 1 and 10  "))

    if intento==secret_number:
        print("Congrats! You made it!")
        guess_number= True

    else:
        print ("Try again")






