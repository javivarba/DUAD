def prime_number(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def filter_prime(numbers):
    return [num for num in numbers if prime_number(num)]

# Ejemplo
numbers = [1, 2, 7, 11, 13, 25, 55, 67, 85]
results = filter_prime(numbers)
print(results)  # [2, 7, 11, 13, 67]
