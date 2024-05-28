numbers =[1,-2,3,-4,2,6,-8,4,-9,5,-3]
positive_number_count = 0

for num in numbers:
    if num > 0:
        positive_number_count += 1
print("Final count for positive numbers :" ,positive_number_count)