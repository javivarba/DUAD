# Ejercicio 3

from datetime import date

class User:
    def __init__(self, name, date_of_birth):
        self.name = name
        self.date_of_birth = date_of_birth

    @property
    def age(self):
        today = date.today()
        age = today.year - self.date_of_birth.year
        if (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day):
            age -= 1
        return age

def requires_adult_user(func):
    def wrapper(user: 'User', *args, **kwargs):
        if user.age < 18:
            raise ValueError(f"User '{user.name}' is underage: {user.age} years old.")
        return func(user, *args, **kwargs)
    return wrapper

@requires_adult_user
def access_sensitive_data(user):
    print(f"Access granted to {user.name}'s sensitive data.")

# Example 
john = User("John", date(2005, 6, 15))  # 19 years old 
anna = User("Anna", date(2010, 1, 1))   # 14 years old

access_sensitive_data(anna)  

