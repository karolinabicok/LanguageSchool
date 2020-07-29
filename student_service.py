from Appointment import Appointment
from Course import Course
from CustomExceptions import AppointmentNotAvailableException
from input_check import input_date, input_time_num, input_course


class StudentService(object):

    def schedule_appointment(self, student):

        while True:
            date = input_date()

            available_time_nums = Appointment.get_available_time_nums(date)

            time_num_dict = self.get_time_num_dict()

            self.print_available_time_nums(available_time_nums, time_num_dict)

            time_num = input_time_num()

            self.print_courses()

            course = input_course()

            try:
                Appointment.schedule_appointment(date, time_num, student, course)
                print("Uspesno zakazan termin. ")
            except AppointmentNotAvailableException:
                print("Termin koji ste odabrali je zauzet.")

    def print_courses(self):
        print("Kursevi u ponudi: ")
        for course in Course.get_course_list():
            print(course)

    def print_available_time_nums(self, available_time_nums, time_num_dict):
        print("Slobodni vremenski termini: ")
        for num in available_time_nums:
            print(f"{num}: {time_num_dict[num]}")

    def get_time_num_dict(self):
        time_num_dict = {0: "9:00",
                         1: "10:00",
                         2: "11:00",
                         3: "12:00",
                         4: "13:00",
                         5: "14:00",
                         6: "15:00",
                         7: "16:00"
                         }
        return time_num_dict

    def cancel_appointment(self, student):

        appointments = self.view_schedules(student)

        print("Izaberi datum i vreme termina koji zelis da otkazes: ")

        while True:
            date = input_date()
            time_num = input_time_num()
            for a in appointments:
                if a.date == date and a.time_num == time_num:
                    a.remove_appointment()
                    print("Uspesno otkazan termin.")
                    return

    def view_price_list(self):
        courses = Course.get_course_list()
        for c in courses:
            print(str(c))

    def view_schedules(self, student):
        appointments = Appointment.get_all_appointments_for_student(student)

        print("Zakazani termini:")
        for a in appointments:
            print(
                f"{a.date} {self.get_time_num_dict()[a.time_num]} {a.teacher.f_name} {a.teacher.l_name} {a.course.title}")
        return appointments

    def change_language(self):
        pass

    def change_teacher(self):
        pass
