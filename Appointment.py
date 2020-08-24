from Course import Course
from CustomExceptions import AppointmentNotAvailableException, AppointmentNotFoundException, NoEnoughFundsException
from Student import Student
from Teacher import Teacher
from datetime import date as dt
import os


class Appointment:
    calendar = {}
    finished_appointments = []

    def __init__(self, date, time_num, teacher, student, course, price):
        self.date = date
        self.time_num = time_num
        self.teacher = teacher
        self.student = student
        self.course = course
        self.price = price

    @classmethod
    def load(cls):
        file = open("appointments.txt", "r")
        for line in file:
            a = cls.get_attributes_from_line(line)
            cls.add_to_calendar(a)

        file.close()

    @classmethod
    def get_attributes_from_line(cls, line):
        attributes = line.strip().split("|")
        a = Appointment(
            date=attributes[0],
            time_num=int(attributes[1]),
            teacher=Teacher.get_by_username(attributes[2]),
            student=Student.get_by_username(attributes[3]),
            course=Course.get_by_title(attributes[4]),
            price=int(attributes[5])
        )
        return a

    @classmethod
    def add_to_calendar(cls, a):
        if a.date not in cls.calendar.keys():
            cls.calendar[a.date] = {}

        if a.time_num not in cls.calendar[a.date].keys():
            cls.calendar[a.date][a.time_num] = a
            return
        else:
            return

    @classmethod
    def save(cls):
        file = open("appointments.txt", "w")
        for date in cls.calendar.keys():
            for time_num in cls.calendar[date].keys():
                a = cls.calendar[date][time_num]
                line = f"{a.date}|{a.time_num}|{a.teacher.username}|{a.student.username}|{a.course.title}|{a.price}\n"
                file.write(line)
        file.close()

    @classmethod
    def get_available_time_nums(cls, date):
        if date not in cls.calendar.keys():
            cls.calendar[date] = {}
            return [0, 1, 2, 3, 4, 5, 6, 7]

        time_num_list = cls.calendar[date].keys()

        available_time_nums = []
        for num in [0, 1, 2, 3, 4, 5, 6, 7]:
            if num not in time_num_list:
                available_time_nums.append(num)
        return available_time_nums

    @classmethod
    def schedule_appointment(cls, date, time_num, student, course):

        today_date = str(dt.today())

        if student.funds <= course.price:
            raise NoEnoughFundsException("No enough funds!")

        if today_date <= date and cls.is_appointment_available(date, time_num):
            cls.add_to_calendar(Appointment(date, time_num, student.teacher, student, course, course.price))

        else:
            raise AppointmentNotAvailableException("Appointment with entered date and time is not available.")

    @classmethod
    def is_appointment_available(cls, date, time_num):
        if time_num in cls.calendar[date]:
            return False
        return True

    @classmethod
    def remove_appointment(cls, date, time_num):
        if time_num in cls.calendar[date]:
            del cls.calendar[date][time_num]

    @classmethod
    def get_all_appointments_for_student(cls, student):

        appointment_list = []

        for date in cls.calendar.keys():
            for time_num in cls.calendar[date].keys():
                a = cls.calendar[date][time_num]
                if a.student == student:
                    appointment_list.append(a)

        return appointment_list

    @classmethod
    def get_all_appointments_for_teacher(cls, teacher):

        appointment_list = []

        for date in cls.calendar.keys():
            for time_num in cls.calendar[date].keys():
                appointment = cls.calendar[date][time_num]
                if appointment.teacher == teacher:
                    appointment_list.append(appointment)

        return appointment_list

    @classmethod
    def get_finished_appointments_list(cls):
        file = open("finished_appointments.txt", "r")

        empty_file = os.stat('finished_appointments.txt').st_size == 0

        if not empty_file:
            for line in file:
                a = cls.get_attributes_from_line(line)
                cls.finished_appointments.append(a)

        file.close()
        return cls.finished_appointments

    @classmethod
    def get_appointment(cls, date, time_num):
        if date in cls.calendar.keys() and time_num in cls.calendar[date].keys():
            return cls.calendar[date][time_num]
        else:
            raise AppointmentNotFoundException("Appointment doesn't exist.")

    @classmethod
    def save_finished_appointments(cls):
        file = open("finished_appointments.txt", "w")
        cls.finished_appointments = list(dict.fromkeys(cls.finished_appointments))
        for appointment in cls.finished_appointments:
            line = f"{appointment.date}|{appointment.time_num}|{appointment.teacher.username}|" \
                   f"{appointment.student.username}|{appointment.course.title}|{appointment.price}\n"
            file.write(line)
        file.close()

    @classmethod
    def delete_unfinished_appointments(cls):
        today_date = str(dt.today())
        for date in list(cls.calendar.keys()):
            if today_date > date:
                for time_num in list(cls.calendar[date].keys()):
                    del cls.calendar[date][time_num]
        cls.save()
