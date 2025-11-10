class Car:
    def __init__(self):
        self.brand = "Toyota"
        self.model = "Camry"
        self.year = 2015


my_car = Car()
print(my_car.year, my_car.model)

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age


p1 = Person("Amina", 14)
p2 = Person("John", 12)

print(p1.name)
print(p2.age)