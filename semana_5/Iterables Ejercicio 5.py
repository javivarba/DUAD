

numbers = []

for i in range(10):
    num= int(input(f"Enter your number {i + 1}: "))
    numbers.append(num)

print ("\nNumbers Entered:" , numbers)

highest_number =  max(numbers)


print( "The highest number is:" ,highest_number )
