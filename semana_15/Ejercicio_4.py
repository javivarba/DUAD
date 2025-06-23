def print_numbers_times_2(numbers_list):
	for number in numbers_list:
		print(number * 2)
		
# Big O Analisis: O(1)

def check_if_lists_have_an_equal(list_a, list_b):
	for element_a in list_a:
		for element_b in list_b:
			if element_a == element_b:
				return True
				
	return False

#Big O analisis: O(n*m)


def print_10_or_less_elements(list_to_print):
	list_len = len(list_to_print)
	for index in range(min(list_len, 10)):
		print(list_to_print[index])
		

# Big O Analisis: O(1)


def generate_list_trios(list_a, list_b, list_c):
	result_list = []
	for element_a in list_a:
		for element_b in list_b:
			for element_c in list_c:
				result_list.append(f'{element_a} {element_b} {element_c}')
				
	return result_list 

# n= len(list_a)
# m= len (list_b)
# k= len (list_c)
# Big O Analisis, basado en las 3 variantes