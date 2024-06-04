import math

def circle_stats(radius):
    area = math.pi * radius ** 2
    circumference = 2 * math.pi * radius
    return area, circumference
    
a, c = circle_stats(4)
print("area",a, "Circumference", c)