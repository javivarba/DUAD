name=input ("Enter your name: ")

last_name=input ("Enter your last name ")

age=int(input  ("How old are you? "))

if age <2 : categoria= "Baby"

elif age <10 : categoria = "kid"

elif age <12 : categoria = "Pre Teenager"

elif age <13 : categoria = "Teenager"

elif age <18 : categoria = "Young adult"

elif age <60 : categoria = "Adult"

else: categoria="Senior"


print(f' "Your name is" {name} "and your age is" {age} "years old, so you are an " {categoria}')