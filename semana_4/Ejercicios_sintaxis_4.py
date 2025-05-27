
number_one = int(input(" Enter your first number: "))

number_two = int(input(" Enter your second number: "))

number_three = int(input(" Enter your third number: "))

if number_one>number_two and number_one>number_three :
    mayor=number_one
elif number_two>number_one and number_two>number_three :
        mayor=number_two
else: 
    mayor=number_three

print(f"The Major number is {mayor}")



