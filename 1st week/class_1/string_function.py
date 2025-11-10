class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __str__(self):
        return f"My name is {self.name} and I am {self.age} years old"


p1 = Person("Amina", 14)
p2 = Person("John", 12)

print(p1)
print(p2)
