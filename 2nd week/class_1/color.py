class MyError(Exception):
    pass

try:
    x = int(input("Number: "))
except ValueError as e:
    print("Not a number:", e)
else:
    print("Good:", x)
finally:
    print("Always runs")