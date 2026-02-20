#Dog inherits the method speak() from the Animal class.
#This is basic inheritance.
class Animal:
    def speak(self):
        print("Animal makes a sound")

class Dog(Animal):  # Dog inherits from Animal
    pass

dog = Dog()
dog.speak()
