def bubble_sort (numbers):
    for step in range(len(numbers)-1):
        for i in range(len(numbers)-1-step):
            print(f"Comparing {numbers [i]} and {numbers [i + 1]}")

            if numbers [i] > numbers [i +1]:
                print ("Swapping")
                numbers [i], numbers [i+1] = numbers [i+1], numbers[i]

my_list = [4,2,1]
bubble_sort(my_list)