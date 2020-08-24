from Admin import Admin
from Course import Course
from Student import Student
from Teacher import Teacher


class AdminService:

    def print_admin_services(self):
        print("Choose option:\n"
              "[0] Add new course\n"
              "[1] Register teacher\n"
              "[2] Register new admin\n"
              "[3] Update student's funds\n"
              "[4] Log out\n")

    def register_teacher(self):
        f_name = input("First name: ")
        l_name = input("Last name: ")
        username = input("Username: ")
        password = input("Password: ")
        language = input("Language: ")
        Teacher.register(f_name, l_name, language, username, password)
        Teacher.save()
        print("Successfully registered teacher.")

    def add_course(self):
        while True:
            try:
                course = input("Course name: ")
                price = int(input("Price: "))
                Course.add_new_course(course, price)
                Course.save()
                print("Successfully added course.")
                return
            except ValueError:
                print("Please enter an integer value for price.")

    def get_student(self):
        print("Student's usernames: \n")
        students = []

        for student in Student.student_list:
            students.append(student.username)
            print(student.username)

        while True:
            username = input("Enter student's username or x to quit: ")
            if username in students or username == 'x':
                return username

    def register_admin(self):
        while True:
            username = input("Username: ")
            password = input("Password: ")
            if not Admin.admin_in_list(username):
                admin = Admin(username, password)
                Admin.admins.append(admin)
                Admin.save()
                print("Admin " + username + " is successfully registered.")
                return
            else:
                print("Username already exists. Please enter different username.")


    def update_funds(self):
        while True:
            username = self.get_student()
            if username == 'x':
                return

            try:
                funds = int(input("Add funds: "))
                student = Student.get_by_username(username)
                student.funds += funds
                Student.save()
                print("Student's funds are updated.")
                return
            except ValueError:
                print("Please input an integer number.")
