class Car:
    def __init__(self, brand, model):
        self.brand = brand
        self.model = model

    def move(self):
        print("DRIVE!!!")


class Plane:
    def __init__(self, brand, model):
        self.brand = brand
        self.model = model

    def move(self):
        print("FLY!!!")


class Boat:
    def __init__(self, brand, model):
        self.brand = brand
        self.model = model

    def move(self):
        print("SAIL!!!")

c1 = Car("Toyota", "Corolla")
p1 = Plane("Boeing", "373")
b1 = Boat("Ibiza", "Toring 29")

for x in (c1, p1, b1):
    x.move()