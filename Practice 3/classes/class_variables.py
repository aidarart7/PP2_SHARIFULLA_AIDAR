class Car:
    wheels = 4   # class variable

    def __init__(self, brand):
        self.brand = brand   # instance variable

car1 = Car("BMW")
car2 = Car("Toyota")

print(car1.wheels)
print(car2.wheels)
