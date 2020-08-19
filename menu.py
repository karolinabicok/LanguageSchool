from Admin import Admin
from Student import Student
from Teacher import Teacher

Admin.load()
Teacher.load()
Student.load()


def start():
    print("=====================================\n"
          "|                                   |\n"
          "| Welcome to Foreign Language School|\n"
          "|                                   |\n"
          "=====================================")

    num = login_or_register()

    login(num)

    register_student(num)


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


def login(num):
    if num == 0:

        login_type = login_types()

        while login_type == 'a':
            login_data = login_input()
            admin_exists = Admin.login(login_data[0], login_data[1])
            while True:
                if admin_exists:
                    pass
                else:
                    print("Incorrect username or password.")
                    break
            break

        while login_type == 't':
            login_data = login_input()
            teacher_exists = Teacher.login(login_data[0], login_data[1])
            while True:
                if teacher_exists:
                    pass
                else:
                    print("Incorrect username or password.")
                    break
            break

        while login_type == 's':
            login_data = login_input()
            student_exists = Student.login(login_data[0], login_data[1])
            while True:
                if student_exists:
                    pass
                else:
                    print("Incorrect username or password.")
                    break
            break

        if login_type == 'x':
            return

    else:
        return


def login_or_register():
    while True:
        print("Please enter a number to log in[0] or sign up[1]: ")
        num = int(input("My choice is: "))
        if num == 1 or num == 0:
            return num


def login_types():
    print("Log in as:\n[a] Admin\n[s] Student\n[t] Teacher\n[x] Go back")
    print(">>>")
    while True:
        login_type = input()
        if login_type in ['a', 's', 't', 'x']:
            return login_type


def login_input():
    username = input("Username: ")
    password = input("Password: ")
    return username, password


start()
