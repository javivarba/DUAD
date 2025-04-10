

def swap_first_last(my_list):
    if len(my_list) > 1:  # Solo intercambiamos si hay más de un elemento
        my_list[0], my_list[-1] = my_list[-1], my_list[0]  
    return my_list

# Ejemplo de uso
my_list = ["gato", "Mono", "Puma", "pantera", "Burro"]
print(swap_first_last(my_list))  
