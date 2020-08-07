import datetime

import formatting
from Course import Course


def check_date_format(date):
    try:
        datetime.datetime.strptime(date, "dd/MM/yyyy")
        return True
    except:
        print("Uneti datum nije validan.")
        return False


def input_date():
    while True:
        date = input("Upisite datum: ")
        date = formatting.date_formatted(date)
        today = formatting.date_formatted(formatting.today_date_str_formatted())

        if check_date_format(date) and today <= date:
            return date


def input_time_num():
    while True:

        time_num = int(input("Upisite broj: "))
        if time_num in range(0, 8):
            return time_num
        else:
            print("Uneta vrednost mora biti broj od 0 do 7.")


def input_course():
    while True:
        title = input("Unesite naziv kursa: ")
        for course in Course.course_list:
            if course.title == title:
                return course
        else:
            print("Naziv kursa nije validan. ")
