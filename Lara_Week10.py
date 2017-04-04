#   File Name: Lara_Week10.py
#   Assignment: Lara_Week10.py
#
#   Author: Jose Lara on 3/28/2017
#   Class: SSW 810 - Special Topic in SWE
#
#   This program gets data from files and uses Pretty table to display it
#   This program was completed using Python 3.5.1

# Library imports
import unittest
from _collections import defaultdict
from prettytable import PrettyTable


# Test Classes
class StudentTest(unittest.TestCase):
    def test__init__(self):
        stu = Student('123', 'Jose', 'SFEN')
        self.assertEqual(Student('123', 'Jose', 'SFEN').name, stu.name, True)
        self.assertEqual(Student('123', 'Jose', 'SFEN').major, stu.major, True)

    def test_assign_grade(self):
        stu = Student('123', 'Jose', 'SFEN')
        stu.assign_grade('SSW 540', 'A')
        stu2 = Student('123', 'Jose', 'SFEN')
        stu2.assign_grade('SSW 540', 'A')

        self.assertEqual(stu2.get_courses(), stu.get_courses(), True)
class InstructorTest(unittest.TestCase):
    def test__init__(self):
        inst = Instructor('3321', 'James Rowland', 'SFEN')
        self.assertNotEqual(Student('123', 'Jose', 'SFEN').name, inst.name, True)


# Program
class Student:
    '''defines a object of Student type'''

    def __init__(self, id, name, major):
        self.name = name
        self.CWID = id
        self.major = major
        self.courses = defaultdict(str)
        self.missing_courses = list()

    def assign_grade(self, course, grade):
        self.courses[course] = grade

    def get_courses(self):
        return self.courses.keys()

    def get_grades(self, course):
        return self.courses.get(course)

    def set_missing_courses(self, courses):
        self.missing_courses = courses

    def get_missing_courses(self):
        return self.missing_courses


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


class Major:
    '''stores the require courses for SFEN and SYEN students'''
    def __init__(self):
        self.majors_data = dict()

    def set_major_requirements(self, major, course):
        '''sets the major required by students'''
        self.majors_data.setdefault(major, []).append(course)

    def get_missing_courses(self, student):
        '''get the missing courses for the major required by students'''
        for key, value in student.items():
            course_taken = set([x for x in student[key].get_courses()])
            student_major = student[key].major
            remainder = set(self.majors_data[student_major]) - course_taken
            student[key].set_missing_courses(remainder)


class Repository:
    '''defines a object of Repository type. It holds all students, instructors and grades.'''

    def read_student_data(self, file_name):
        '''Read files for students and instructor data'''
        try:
            open(file_name, "r")

        except FileNotFoundError:
            print(file_name, "file cannot be opened!")

        except IOError:
            print('Please check that file is not corrupted.')

        else:
            with open(file_name, 'r') as file_opened:
                # reading data from file
                each_line = file_opened.readlines()

                if len(each_line) == 0:
                    raise ValueError('file is empty')
                else:
                    dict_data = defaultdict(lambda: defaultdict(str))
                    for line in each_line:
                        CWID, name, dept = line.strip('\n').split('\t')

                        dict_data[CWID] = Student(CWID, name, dept)

                    return dict_data

    def read_instrutor_data(self, file_name):
        '''Read files for students and instructor data'''
        try:
            open(file_name, "r")

        except FileNotFoundError:
            print(file_name, "file cannot be opened!")

        except IOError:
            print('Please check that file is not corrupted.')

        else:
            with open(file_name, 'r') as file_opened:
                # reading data from file
                each_line = file_opened.readlines()

                if len(each_line) == 0:
                    raise ValueError('file is empty')
                else:
                    dict_data = defaultdict(lambda: defaultdict(str))
                    for line in each_line:
                        CWID, name, dept = line.strip('\n').split('\t')

                        dict_data[CWID] = Instructor(CWID, name, dept)

                    return dict_data

    def read_grades_file(self, file_name, student_data, instructor_data):
        '''Read files for grades for students and the courses instructor teach data'''
        try:
            open(file_name, "r")

        except FileNotFoundError:
            print(file_name, "file cannot be opened!")

        except IOError:
            print('Please check that file is not corrupted.')

        else:
            # reading data from file
            with open(file_name, "r") as file_opened:
                each_line = file_opened.readlines()

                each_line.sort()

                if len(each_line) == 0:
                    raise ValueError('file is empty')
                else:
                    for line in each_line:
                        student_id, course, grade, instructor_id = line.strip('\n').split('\t')

                        student_data[student_id].assign_grade(course, grade)

                        instructor_data[instructor_id].courses_taught(course)

    def read_majors(self, file_name, major_class):
        '''Read the required courses for each students major '''
        try:
            open(file_name, 'r')
        except IOError:
            print('There was en error processing the {} file'.format(file_name))
        except FileNotFoundError:
            print('{} file does not exist'.format(file_name))
        else:
            with open(file_name, 'r') as file_opened:
                each_line = file_opened.readlines()

                if len(each_line) == 0:
                    raise ValueError('File is Empty')
                else:
                    for line in each_line:
                        major, course = line.strip('\n').split('\t')

                        major_class.set_major_requirements(major, course)

                    return major_class

    def instructor_table(self, data):
        '''Displays a pretty Table for instructors data'''
        instructor_table = PrettyTable(["CWID", "Name", "Dept", 'Course', 'Students'])

        for x in data:
            course_value = [x for x in data[x].get_courses()]
            for y in course_value:
                instructor_table.add_row([data[x].CWID, data[x].name,data[x].department, y, data[x].get_students(y)])

        print("Instructor Table")
        print(instructor_table)

    def student_table(self, data):
        '''Displays a pretty Table for students data'''
        student_table = PrettyTable(["CWID", "Name", "Completed Courses", "Missing Courses"])
        for x in data:
            student_table.add_row([data[x].CWID, data[x].name, [x for x in data[x].get_courses()], data[x].get_missing_courses()])

        print("Student Table")
        print(student_table)


# Main Program
def main():
    """Program starts here"""
    repo = Repository()
    majors = Major()
    student_data = repo.read_student_data('students.txt')
    instructor_data = repo.read_instrutor_data('instructors.txt')
    repo.read_grades_file('grades.txt', student_data, instructor_data)
    repo.read_majors('majors.txt', majors)
    majors.get_missing_courses(student_data)
    repo.instructor_table(instructor_data)
    repo.student_table(student_data)


if __name__ == '__main__':
    main()
    #unittest.main(exit=False, verbosity=2)