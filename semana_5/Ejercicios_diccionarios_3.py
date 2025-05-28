
student = {'name': 'Michael Corleone', 'email': 'michaelcorleone@cosanostra.com', 'level':'CAPO','age':'25','murdered':'3'}


list_of_keys= ['email', 'age']

for key in list_of_keys:
    student.pop(key, None)


print(student)
