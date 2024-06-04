def sum_all(*args):
    print(args)
    return sum(args)

print(sum_all(12, 5))
print(sum_all(12, 5, 6))
print(sum_all(12, 5, 6, 7))