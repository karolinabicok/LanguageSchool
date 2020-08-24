import datetime
from Course import Course
from CustomExceptions import NoSuchTitleException


def check_date_format(date):
    try:
        datetime.datetime.strptime(date, "%Y-%m-%d")
        return True
    except:
        print("Entered date is invalid.")
        return False


def input_date():
    while True:
        date = input("\nEnter the date of yyyy-mm-dd format or x to quit: ")

        if check_date_format(date) or date == 'x':
            return date


def input_time_num():
    while True:

        time_num = input("\nEnter the time number [0-7] or x to quit: ")
        if time_num == 'x':
            return time_num

        time_num = int(time_num)
        if time_num in range(0, 8):
            return time_num
        else:
            print("Entered value must be in range [0-7].\n")


def input_course():
    while True:
        try:
            title = input("\nEnter the course name: ")
            course = Course.get_by_title(title)
            return course
        except NoSuchTitleException:
            print("Course name is invalid. ")
