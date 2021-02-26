import itertools
import json


class Student:
    def __init__(self, name, pref):
        self.name = name
        self.pref = pref

def getStudents():
    with open('semlor.json') as json_file:
        data = json.load(json_file)
        students = list()

        for student in data:
            s = Student(student['name'], student['preference'])

            students.append(s)

        return students

students = getStudents()

# We know 197 is best score, so we really just have to find which 3 people we have to remove to satisfy everyone else.
# for combination in itertools.combinations(students, 3):

regular = 100
chocolate = 50
vegan = 20
gluten = 15
wrap = 15

"""
"regular":true,
"chocolate":false,
"vegan":false,
"gluten free":false,
"wrap":true
"""
