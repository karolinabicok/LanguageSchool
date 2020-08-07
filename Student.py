from CustomExceptions import NoSuchUsernameException
from Teacher import Teacher


class Student(object):
    student_list = []

    def __init__(self, f_name, l_name, username, password, language, teacher, funds):
        self.f_name = f_name
        self.l_name = l_name
        self.username = username
        self.password = password
        self.language = language
        self.teacher = teacher
        self.funds = funds

    @classmethod
    def load(cls):
        file = open("students.txt", "r")
        for line in file:
            attributes = line.strip().split("|")
            s = Student(f_name=attributes[0],
                        l_name=attributes[1],
                        username=attributes[2],
                        password=attributes[3],
                        language=attributes[4],
                        teacher=Teacher.get_by_username(attributes[5]),
                        funds=int(attributes[6])
                        )
            cls.student_list.append(s)
        file.close()

    @classmethod
    def save(cls):
        file = open("students.txt", "w")
        for s in cls.student_list:
            line = f"{s.f_name}|{s.l_name}|{s.username}|{s.password}|{s.language}|{s.teacher.username}|{s.funds}\n"
            file.write(line)
        file.close()

    @classmethod
    def register(cls, f_name, l_name, username, password, language, teacher, funds):
        cls.student_list.append(Student(f_name, l_name, username, password, language, teacher, funds))

    @classmethod
    def get_by_username(cls, username):
        for student in cls.student_list:
            if student.username == username:
                return student
        else:
            raise NoSuchUsernameException("Korisnicko ime ne postoji.")


