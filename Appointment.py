from Course import Course
from CustomExceptions import AppointmentNotAvailableException, NoEnoughFundsException
from Teacher import Teacher
from Student import Student
import formatting

from input_check import input_date, input_time_num


class Appointment:
    calendar = {}

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
            attributes = line.strip().split("|")
            a = Appointment(
                date=attributes[0],
                time_num=int(attributes[1]),
                teacher=Teacher.get_by_username(attributes[2]),
                student=Student.get_by_username(attributes[3]),
                course=Course.get_by_title(attributes[4]),
                price=int(attributes[5])
            )
            cls.add_to_calendar(a)

        file.close()

    @classmethod
    def add_to_calendar(cls, a):
        if a.date not in cls.calendar.keys():
            cls.calendar[a.date] = {}
        cls.calendar[a.date][a.time_num] = a

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
        appointment_dict = cls.calendar[date]
        available_time_nums = []
        for num in [0, 1, 2, 3, 4, 5, 6, 7]:
            if num not in appointment_dict.keys():
                available_time_nums.append(num)
        return available_time_nums

    @classmethod
    def schedule_appointment(cls, date, time_num, student, course):
        today = formatting.date_formatted(formatting.today_date_str_formatted())
        date = formatting.date_formatted(date)

        if today <= date and cls.is_appointment_available(date, time_num) and student.funds >= course.price:
            cls.calendar[date][time_num] = Appointment(date, time_num, student.teacher, student, course,
                                                               course.price)
        else:
            raise AppointmentNotAvailableException("Uneti datum nije validan.")

    @classmethod
    def is_appointment_available(cls, date, time_num):
        if time_num in cls.calendar[date].keys():
            return False
        return True

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
                a = cls.calendar[date][time_num]
                if a.teacher == teacher:
                    appointment_list.append(a)

        return appointment_list

    @classmethod
    def cancel_appointment(cls, student_username, date, time_num):
        if date in cls.calendar.keys() and time_num in cls.calendar[date].keys():
            if cls.calendar[date][time_num].student.username == student_username:
                cls.calendar[date][time_num].remove_appointment()
                print("Uspesno otkazan cas.")

    @classmethod
    def get_finished_appointments_list(cls):
        finished_a = []
        file = open("finished_appointments", "r")
        for line in file:
            attributes = line.strip().split("|")
            a = Appointment(
                date=attributes[0],
                time_num=int(attributes[1]),
                teacher=Teacher.get_by_username(attributes[2]),
                student=Student.get_by_username(attributes[3]),
                course=Course.get_by_title(attributes[4]),
                price=int(attributes[5])
            )
            finished_a.append(a)
        file.close()
        return finished_a

    @classmethod
    def get_appointment(cls, date, time_num):
        if date in cls.calendar.keys() and time_num in cls.calendar[date].keys():
            return cls.calendar[date][time_num]
        else:
            return None

    @classmethod
    def finish_appointment(cls):
        finished_a = cls.get_finished_appointments_list()

        today_date = formatting.today_date_str_formatted()
        appointment_date = input_date()

        time_num = input_time_num()
        if today_date == appointment_date:
            appointment = Appointment.get_appointment(appointment_date, time_num)
            finished_a.append(appointment)

    @classmethod
    def save_finished_appointments(cls):
        finished_a = cls.get_finished_appointments_list()

        file = open("finished_appointments.txt", "w")
        for appointment in finished_a:
            line = f"{appointment.date}|{appointment.time_num}|{appointment.teacher.username}|" \
                   f"{appointment.student.username}|{appointment.course.title}|{appointment.price}\n"
            file.write(line)
        file.close()


