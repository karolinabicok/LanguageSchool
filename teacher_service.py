from datetime import date as dt
from Appointment import Appointment
from Student import Student
from input_check import input_date, input_time_num
import matplotlib.pyplot as plt


class TeacherService(object):
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

    def today_earnings(self, teacher):
        today_date = str(dt.today())
        file = open("finished_appointments.txt", "r")
        earnings = 0

        for line in file:
            attributes = line.strip().split("|")
            if today_date == attributes[0] and teacher.username == attributes[2]:
                earnings += int(attributes[5])

        file.close()
        return earnings

    def view_schedules(self, teacher):
        appointments = Appointment.get_all_appointments_for_teacher(teacher)

        if not appointments:
            print("There are no scheduled appointments.")
        else:
            print("Scheduled appointments:")
            for a in appointments:
                print(
                    f"{a.date} {self.get_time_num_dict()[a.time_num]} {a.student.f_name}"
                    f" {a.student.l_name} {a.course.title}")

        return appointments

    def cancel_appointment(self, teacher):

        appointments = self.view_schedules(teacher)

        if not appointments:
            return

        else:
            print("Select the date and time of the appointment you want to cancel: ")

            time_num_dict = self.get_time_num_dict()

            for time_num in time_num_dict:
                print(time_num, ":", time_num_dict[time_num])

            date = input_date()
            time_num = input_time_num()

            if date == 'x' or time_num == 'x':
                return

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

    def finish_appointment(self, teacher):

        appointments = self.view_schedules(teacher)

        time_num_dict = self.get_time_num_dict()

        for time_num in time_num_dict:
            print(time_num, ":", time_num_dict[time_num])

        time_num = input_time_num()
        if time_num == 'x':
            return

        today_date = str(dt.today())
        a_in_list = False

        for a in appointments:
            if today_date == a.date and time_num == a.time_num:
                a_in_list = True

        if a_in_list:
            appointment = Appointment.get_appointment(today_date, time_num)

            if appointment.student.funds < appointment.price:
                print("No enough funds to finish an appointment.")
                return

            else:
                print("Appointment finished.")

                appointment.student.funds = appointment.student.funds - appointment.price

                Student.save()

                Appointment.finished_appointments.append(appointment)

                Appointment.remove_appointment(appointment.date, appointment.time_num)

                Appointment.save()

                Appointment.save_finished_appointments()

        else:
            print("Appointment at that time is not scheduled.")

    def todays_earnings_graph(self):
        teachers_and_earnings = {}

        file = open("finished_appointments.txt", "r")

        today_date = str(dt.today())

        for line in file:
            appointment = Appointment.get_attributes_from_line(line)

            if today_date == appointment.date:

                name = appointment.teacher.f_name + " " + appointment.teacher.l_name

                if name not in teachers_and_earnings.keys():
                    teachers_and_earnings[name] = self.today_earnings(appointment.teacher)

        self.plot_graph(teachers_and_earnings)
        file.close()

    def plot_graph(self, teachers_and_earnings):
        sorted_earnings = sorted(teachers_and_earnings.items(), key=lambda x: x[1])
        x_data = []
        y_data = []
        for pair in sorted_earnings:
            x_data.append(pair[0])
            y_data.append(pair[1])
        plt.title("Today's earnings by teacher")
        plt.bar(x_data, y_data, width=0.4)
        plt.xlabel('Teachers')
        plt.xticks(rotation=30)
        plt.ylabel('Earnings')
        plt.ylim(ymin=0, ymax=100)
        plt.show()

    def print_teacher_services(self):
        print("Choose available option:\n"
              "[0] View schedules\n"
              "[1] Finish appointment\n"
              "[2] Cancel appointment\n"
              "[3] View today's earnings\n"
              "[4] View today's statistics of earnings\n"
              "[5] Log out\n"
              )
