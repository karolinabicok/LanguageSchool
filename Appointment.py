from Course import Course
from CustomExceptions import AppointmentNotAvailableException, AppointmentNotFoundException
from Student import Student
from Teacher import Teacher


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

        if cls.is_appointment_available(date, time_num) and student.funds >= course.price:
            cls.calendar[date][time_num] = Appointment(date, time_num, student.teacher, student, course,
                                                       course.price)
        else:
            raise AppointmentNotAvailableException("Termin za uneti datum i vreme nije slobodan.")

    @classmethod
    def is_appointment_available(cls, date, time_num):
        if time_num in cls.calendar[date].keys():
            return False
        return True

    def remove_appointment(self):
        del self.calendar[self.date][self.time_num]

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
        file = open("finished_appointments", "r")
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
            raise AppointmentNotFoundException("Termin ne postoji.")

    @classmethod
    def save_finished_appointments(cls):
        finished_a = cls.get_finished_appointments_list()

        file = open("finished_appointments.txt", "w")
        for appointment in finished_a:
            line = f"{appointment.date}|{appointment.time_num}|{appointment.teacher.username}|" \
                   f"{appointment.student.username}|{appointment.course.title}|{appointment.price}\n"
            file.write(line)
        file.close()
