class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def welcome(self):
        print(f"Hello {self.name} welcome to python advanced class")


person1 = Person("Emmanuel", 14)

#child class
class Student(Person):
    pass

    def intro(self):
        cohort = input("what cohort are you?: ")
        print(f"My name is {self.name}, I am {self.age} years old and in cohort {cohort}")

x = Student("Joseph", 17)
#x.welcome()
#person1.welcome()
x.intro()

#class Student(Person):
#    def __init__(self, name, age):
#        Person.__init__(self, name, age)

#x = Student("Sandra", 17)
#x.welcome

#class Student(Person):
#    def __init__(self, name, age, gradyear):
#        super().__init__(name, age)
#        self.gradyear = gradyear

#    def cont(self):
#        print(f"Hello I am {self.name} I am graduating in {self.gradyear}")

#x = Student("Sandra", 14, 2025)
#x.welcome()
#x.cont()