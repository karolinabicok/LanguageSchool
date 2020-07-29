from Course import Course
from CustomExceptions import AppointmentNotAvailableException
from Teacher import Teacher
from Student import Student


class Appointment:
    calendar = {}

    def __init__(self, date, time_num, teacher, student, course):
        self.date = date
        self.time_num = time_num
        self.teacher = teacher
        self.student = student
        self.course = course

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
                course=Course.get_by_title(attributes[4])
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
                line = f"{a.date}|{a.time_num}|{a.teacher.username}|{a.student.username}|{a.course.title}\n"
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
        if cls.is_appointment_available(date, time_num):
            cls.calendar[date][time_num] = Appointment(date, time_num, student.teacher, student, course)
        else:
            raise AppointmentNotAvailableException("Nije slobodan termin za uneti datum i vremenski broj")

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

    def remove_appointment(self):
        del self.calendar[self.date][self.time_num]

