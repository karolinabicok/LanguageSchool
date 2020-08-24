from Appointment import Appointment
from Course import Course
from CustomExceptions import AppointmentNotAvailableException, NoEnoughFundsException
from Student import Student
from Teacher import Teacher
from input_check import input_date, input_time_num, input_course


class StudentService(object):

    def schedule_appointment(self, student):

        while True:
            date = input_date()
            if date == 'x':
                return

            available_time_nums = Appointment.get_available_time_nums(date)

            time_num_dict = self.get_time_num_dict()

            self.print_available_time_nums(available_time_nums, time_num_dict)

            time_num = input_time_num()

            if time_num == 'x':
                return

            self.print_courses()

            course = input_course()

            try:
                Appointment.schedule_appointment(date, time_num, student, course)
                Appointment.save()
                print("You have successfully scheduled an appointment.")
                return
            except AppointmentNotAvailableException:
                print("The selected appointment is unavailable.")
            except NoEnoughFundsException:
                print("You don't have enough funds to schedule an appointment.")
                return

    def print_courses(self):
        print("Available courses: ")
        for course in Course.get_course_list():
            print(course)

    def print_available_time_nums(self, available_time_nums, time_num_dict):
        print("Available time nums: ")
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

        print("Appointments that can be canceled:")
        appointments = self.view_schedules(student)

        if not appointments:
            print("There are no scheduled appointments.\n")
            return
        else:
            print("Select the date and time of the appointment you want to cancel: ")

            time_num_dict = self.get_time_num_dict()

            for time_num in time_num_dict:
                print(time_num, ":", time_num_dict[time_num])

            date = input_date()
            time_num = input_time_num()

            for appointment in appointments:
                if appointment.date == date:
                    while appointment.time_num != time_num:
                        print("Please enter a valid number:")
                        time_num = input_time_num()
                    appointment.remove_appointment(date, time_num)
                    print("Successfully canceled appointment.")
                    Appointment.save()
                    return

            else:
                print("Appointment not found.")
                return

    def view_schedules(self, student):
        appointments = Appointment.get_all_appointments_for_student(student)

        print("Scheduled appointments:")
        for a in appointments:
            print(
                f"{a.date} {self.get_time_num_dict()[a.time_num]} {a.teacher.f_name}"
                f" {a.teacher.l_name} {a.course.title}")
        return appointments

    def leave_school(self, student):
        for date in Appointment.calendar.keys():
            for time_num in list(Appointment.calendar[date].keys()):
                if Appointment.calendar[date][time_num].student == student:
                    del Appointment.calendar[date][time_num]
                    Appointment.save()
        Student.student_list.remove(student)
        Student.save()
        print("Success.")

    def change_teacher(self, student):
        print("Available teachers for " + student.language + " language:")

        available_teachers = Teacher.teachers_by_language(student.language)

        for t in available_teachers:
            print(t)

        while True:
            chosen_teacher = input("Enter the teacher's username: ")
            if chosen_teacher in available_teachers:
                student.teacher = Teacher.get_by_username(chosen_teacher)
                print("Successfully changed teacher.\n")
                Student.save()
                return
            else:
                print("Oops! Entered username doesn't exist in list.\n")
                return

    def get_student_data(self, student):
        print("First name: ", student.f_name)
        print("Last name: ", student.l_name)
        print("Teacher: ", student.teacher.f_name + " " + student.teacher.l_name)
        print("Your funds: ", student.funds)
        print()

    def print_student_services(self):
        print("Choose available option:\n\n"
              "[0] View available courses\n"
              "[1] View schedules\n"
              "[2] Schedule appointment\n"
              "[3] Cancel appointment\n"
              "[4] Change teacher\n"
              "[5] Leave school\n"
              "[6] Your info\n"
              "[7] Log out"
              )
