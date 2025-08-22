
def check_all_numbers(func):
    def wrapper(*args, **kwargs):
        for arg in args:
            if not isinstance(arg, (int, float)):
                raise TypeError(f"Argument {arg} is not a number.")
        for key, value in kwargs.items():
            if not isinstance(value, (int, float)):
                raise TypeError(f"Keyword argument '{key}' with value {value} is not a number.")
        return func(*args, **kwargs)
    return wrapper

@check_all_numbers
def multiply(a, b):
    return a * b

print(multiply(5, 5))       
