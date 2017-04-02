#   File Name: Lara_Week10.py
#   Assignment: Lara_Week10.py
#
#   Author: Jose Lara on 3/28/2017
#   Class: SSW 810 - Special Topic in SWE
#
#   This program gets data from files and uses Pretty table to display it
#   This program was completed using Python 3.5.1


from _collections import defaultdict
from prettytable import PrettyTable


class Student:
    '''defines a object of Student type'''

    def __init__(self, id, name, major):
        self.name = name
        self.CWID = id
        self.major = major
        self.courses = defaultdict(str)

    def assign_grade(self, course, grade):
        self.courses[course] = grade

    def get_courses(self):
        return self.courses.keys()

    def get_grades(self, course):
        return self.courses.get(course)


class Instructor:
    '''defines a object of Instructor type'''

    def __init__(self, id, name, department):
        self.name = name
        self.CWID = id
        self.department = department
        self.courses = defaultdict(int)

    def courses_taught(self, course):
        self.courses[course] += 1

    def get_courses(self):
        return self.courses.keys()

    def get_students(self, course):
        return self.courses.get(course)


class Repository:
    '''defines a object of Repository type. It holds all students, instructors and grades.'''

    def read_data(self, file_name):
        '''Read files for students and instructor data'''
        try:
            file_opened = open(file_name, "r")

        except FileNotFoundError:
            print(file_name, "file cannot be opened!")

        except IOError:
            print('Please check that file is not corrupted.')

        else:

            # reading data from file
            each_line = file_opened.readlines()

            if len(each_line) == 0:
                raise ValueError('file is empty')
            else:
                dict_data = defaultdict(lambda: defaultdict(str))
                for line in each_line:
                    CWID, name, dept = line.strip('\n').split('\t')

                    if file_name == 'students.txt':
                        dict_data.update({CWID: Student(CWID, name, dept)})

                    elif file_name == 'instructors.txt':
                        dict_data.update({CWID: Instructor(CWID, name, dept)})

                    else:
                        return None

                return dict_data

    def read_grades_file(self, file_name, student_data, instructor_data):
        try:
            file_opened = open(file_name, "r")

        except FileNotFoundError:
            print(file_name, "file cannot be opened!")

        except IOError:
            print('Please check that file is not corrupted.')

        else:
            # reading data from file
            each_line = file_opened.readlines()

            if len(each_line) == 0:
                raise ValueError('file is empty')
            else:
                for line in each_line:
                    student_id, course, grade, instructor_id = line.strip('\n').split('\t')

                    student_data[student_id].assign_grade(course, grade)

                    instructor_data[instructor_id].courses_taught(course)



    def instructor_table(self, data):
        instructor_table = PrettyTable(["CWID", "Name", "Dept", 'Course', 'Students'])

        for x in data:
            course_value = [x for x in data[x].get_courses()]
            for y in course_value:
                instructor_table.add_row([data[x].CWID, data[x].name,data[x].department, y, data[x].get_students(y)])

        print("Instructor Table")
        print(instructor_table)

    def student_table(self, data):
        student_table = PrettyTable(["CWID", "Name", "Completed Courses"])
        for x in data:
            student_table.add_row([data[x].CWID, data[x].name, [x for x in data[x].get_courses()]])

        print("Student Table")
        print(student_table)


def main():
    repo = Repository()

    student_data = repo.read_data('students.txt')
    instructor_data = repo.read_data('instructors.txt')
    repo.read_grades_file('grades.txt', student_data, instructor_data)

    repo.instructor_table(instructor_data)
    repo.student_table(student_data)


if __name__ == '__main__':
    main()