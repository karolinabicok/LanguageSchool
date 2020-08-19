from Course import Course
from Teacher import Teacher


class Admin:
    admins = []

    def __init__(self, username, password):
        self.username = username
        self.password = password

    @classmethod
    def register_teacher(cls, f_name, l_name, language, t_username, t_password):
        Teacher.register(f_name, l_name, language, t_username, t_password)

    @classmethod
    def add_course(cls, title, price):
        Course.add_new_course(title, price)

    @classmethod
    def load(cls):
        file = open("admins.txt", "r")
        for line in file:
            attributes = line.strip().split("|")
            admin = Admin(username=attributes[0],
                          password=attributes[1])
            cls.admins.append(admin)
        file.close()

    @classmethod
    def save(cls):
        file = open("admins.txt", "w")
        for admin in cls.admins:
            line = f"{admin.username}|{admin.password}\n"
            file.write(line)
        file.close()

    @classmethod
    def login(cls, username, password):
        for a in cls.admins:
            if a.username == username and a.password == password:
                return True
        else:
            return False