

def remove_odds(my_list):
    new_list = []  
    for num in my_list:
        if num % 2 == 0:  
            new_list.append(num)  
    return new_list

# Ejemplo de uso
my_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 96, 12, 77, 49, 50, 31]
print(remove_odds(my_list))
