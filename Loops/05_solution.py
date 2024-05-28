input_str = "banana"


for char in input_str:
    print(char)
    if input_str.count(char) == 1 :
        print("char is ", char)
        break