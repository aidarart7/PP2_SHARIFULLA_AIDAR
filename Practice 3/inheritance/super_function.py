#super() is used to access methods from the parent class, especially the constructor.
class Person:
    def __init__(self, name):
        self.name = name

class Student(Person):
    def __init__(self, name, grade):
        super().__init__(name)  # Call the parent class constructor
        self.grade = grade

student = Student("Aidar", 90)
print(student.name, student.grade)
