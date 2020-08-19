import formatting
from Appointment import Appointment
from Teacher import Teacher
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
        today_date = formatting.today_date_str_formatted()
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

        print("Zakazani termini:")
        for a in appointments:
            print(
                f"{a.date} {self.get_time_num_dict()[a.time_num]} {a.teacher.f_name}"
                f" {a.teacher.l_name} {a.course.title}")
        return appointments

    def cancel_appointment(self, teacher):

        appointments = self.view_schedules(teacher)

        print("Izaberi datum i vreme termina koji zelis da otkazes: ")

        while True:
            date = input_date()
            time_num = input_time_num()
            for appointment in appointments:
                if appointment.date == date and appointment.time_num == time_num:
                    appointment.remove_appointment()
                    print("Uspesno otkazan termin.")
                    Appointment.save()
                    return

    def finish_appointment(self, teacher):
        teacher_appointments = Appointment.get_all_appointments_for_teacher(teacher)

        today_date = formatting.today_date_str_formatted()
        appointment_date = input_date()
        time_num = input_time_num()

        a_in_list = False

        for a in teacher_appointments:
            if today_date == a.date and time_num == a.time_num:
                a_in_list = True

        if a_in_list:
            appointment = Appointment.get_appointment(appointment_date, time_num)
            Appointment.finished_appointments.append(appointment)
            Appointment.save_finished_appointments()
        else:
            print("Termin sa unetim datumom i vremenom nije zakazan.")

    def todays_earnings_graph(self):
        teachers_and_earnings = {}
        file = open("finished_appointments.txt", "r")

        for line in file:
            attributes = Appointment.get_attributes_from_line(line)
            if attributes[2] not in teachers_and_earnings.keys():
                teachers_and_earnings[attributes[2]] = self.today_earnings(attributes[2])

        for teacher in teachers_and_earnings.keys():
            t = Teacher.get_by_username(teacher)
            name = t.f_name + " " + t.l_name
            teachers_and_earnings[name] = teachers_and_earnings.pop(teacher)

        self.plot_graph(teachers_and_earnings)
        file.close()

    def plot_graph(self, teachers_and_earnings):
        sorted_earnings = sorted(teachers_and_earnings.items(), key=lambda x: x[1])
        x_data = []
        y_data = []
        for i in sorted_earnings:
            x_data.append(sorted_earnings[0])
            y_data.append(sorted_earnings[1])
        plt.title("Today's earnings by teacher")
        plt.bar(x_data, y_data)
        plt.xlabel('Teachers')
        plt.xticks(rotation=90)
        plt.ylabel('Earnings')
        plt.ylim(ymin=0, ymax=300)
        plt.show()
