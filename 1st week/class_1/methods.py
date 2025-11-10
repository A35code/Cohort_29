class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def welcome(self):
        grade = input("What grade are you?: ")
        course = input("What is your course?: ")
        print(f"My name is {self.name}, and I am in {course} and grade {grade}, I am {self.age} years")

    def details(self):
        print(f"Here are your details for your name and age: \n {self.name}, {self.age}")


p1 = Person("Amina", 14)
p2 = Person("John", 12)

print(p1)
print(p2)
p1.welcome()
p2.details()