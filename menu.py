import admin_service
from Admin import Admin
from Appointment import Appointment
from Student import Student
from Teacher import Teacher
from Course import Course
import student_service
import teacher_service

Admin.load()
Course.load()
Teacher.load()
Student.load()
Appointment.load()
Appointment.delete_unfinished_appointments()


def start():
    print("=====================================\n"
          "|                                   |\n"
          "| Welcome to Foreign Language School|\n"
          "|                                   |\n"
          "=====================================")

    while True:
        num = login_or_register()

        login(num)

        register_student(num)

        if num == 2:
            exit()


def login(num):
    if num == 0:

        login_type = login_types()

        while login_type == 'a':
            login_data = login_input()
            admin_exists = Admin.login(login_data[0], login_data[1])
            while True:
                if admin_exists:
                    admin_options()
                    break
                else:
                    print("Incorrect username or password.")
                    break
            break

        while login_type == 't':
            login_data = login_input()
            teacher_exists = Teacher.login(login_data[0], login_data[1])
            while True:
                if teacher_exists:
                    teacher_options(login_data[0])
                    break
                else:
                    print("Incorrect username or password.")
                    break
            break

        while login_type == 's':
            login_data = login_input()
            student_exists = Student.login(login_data[0], login_data[1])
            while student_exists:
                student_options(login_data[0])
                break
            else:
                print("Incorrect username or password.")
            break

        if login_type == 'x':
            return

    else:
        return


def login_or_register():
    while True:
        print("Please enter a number to:\n"
              "[0] Log in\n"
              "[1] Sign up\n"
              "[2] Exit")
        try:
            num = int(input(">>>"))
            if num == 1 or num == 0 or num == 2:
                return num
        except ValueError:
            print("Invalid entry. Try again.")


def login_types():
    print("Log in as:\n[a] Admin\n[s] Student\n[t] Teacher\n[x] Go back")
    while True:
        login_type = input(">>>")
        if login_type in ['a', 's', 't', 'x']:
            return login_type


def login_input():
    username = input("Username: ")
    password = input("Password: ")
    return username, password


def register_student(num):
    if num == 1:
        f_name = input("First name: ")
        l_name = input("Last name: ")

        username = input("Username: ")
        while Student.check_username(username):
            username = input("Username is taken. Please choose another: ")
        password = input("Password: ")

        while True:
            print("Available languages and teachers:")
            Teacher.print_teachers_and_languages()

            language = input("Language: ")
            while language not in Teacher.get_languages_list():
                language = input("Language not found. Choose one from list: ")

            teacher = input("Teacher's username: ")
            while not Teacher.teacher_in_list(teacher):
                teacher = input("Teacher not found. Teacher's username: ")

            teacher = Teacher.get_by_username(teacher)
            if language == teacher.language:
                break
            else:
                print("Language doesn't match teacher's username. Try again.")

        while True:
            funds = input("Funds: ")
            try:
                funds = int(funds)
                break
            except ValueError:
                print("Please input integer value.\n")

        Student.register(f_name, l_name, username, password, language, teacher, funds)
        Student.save()
    else:
        return


def student_options(username):
    student_serv = student_service.StudentService()

    while True:
        student = Student.get_by_username(username)

        student_serv.print_student_services()

        option = input(">>>")

        if option == '0':
            student_serv.print_courses()
        elif option == '1':
            student_serv.view_schedules(student)
        elif option == '2':
            student_serv.schedule_appointment(student)
        elif option == '3':
            student_serv.cancel_appointment(student)
        elif option == '4':
            student_serv.change_teacher(student)
        elif option == '5':
            student_serv.leave_school(student)
            return
        elif option == '6':
            student_serv.get_student_data(student)
        elif option == '7':
            return
        else:
            print("Invalid entry. Try again.")


def teacher_options(username):
    teacher_serv = teacher_service.TeacherService()

    while True:
        teacher = Teacher.get_by_username(username)

        teacher_serv.print_teacher_services()

        option = input(">>>")

        if option == '0':
            teacher_serv.view_schedules(teacher)
        elif option == '1':
            teacher_serv.finish_appointment(teacher)
        elif option == '2':
            teacher_serv.cancel_appointment(teacher)
        elif option == '3':
            print("Today's earnings: ", teacher_serv.today_earnings(teacher))
        elif option == '4':
            teacher_serv.todays_earnings_graph()
        elif option == '5':
            return
        else:
            print("Invalid entry. Try again.")


def admin_options():
    admin_serv = admin_service.AdminService()

    while True:
        admin_serv.print_admin_services()
        option = input(">>>")

        if option == '0':
            admin_serv.add_course()
        elif option == '1':
            admin_serv.register_teacher()
        elif option == '2':
            admin_serv.register_admin()
        elif option == '3':
            admin_serv.update_funds()
        elif option == '4':
            return
        else:
            print("Invalid entry. Try again.")


start()
