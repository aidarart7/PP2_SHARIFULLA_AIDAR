#Multiple inheritance allows a class to inherit methods and properties from more than one parent class.
class Father:
    def skill1(self):
        print("Driving")

class Mother:
    def skill2(self):
        print("Cooking")

class Child(Father, Mother):  # Inherits from two classes
    pass

child = Child()
child.skill1()
child.skill2()
