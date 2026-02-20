#Method overriding allows a child class to provide a different implementation of a method defined in the parent class.
class Animal:
    def speak(self):
        print("Animal sound")

class Cat(Animal):
    def speak(self):  # Override parent method
        print("Meow")

cat = Cat()
cat.speak()
