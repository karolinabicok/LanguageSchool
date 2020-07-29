from CustomExceptions import NoSuchUsernameException


class Teacher(object):

    teacher_list = []

    def __init__(self, f_name, l_name, language, username, password):
        self.f_name = f_name
        self.l_name = l_name
        self.language = language
        self.username = username
        self.password = password

    @classmethod
    def load(cls):
        file = open("teachers.txt", "r")
        for line in file:
            attributes = line.strip().split("|")
            t = Teacher(f_name=attributes[0],
                        l_name=attributes[1],
                        language=attributes[2],
                        username=attributes[3],
                        password=attributes[4])
            cls.teacher_list.append(t)
        file.close()

    @classmethod
    def save(cls):
        file = open("teachers.txt", "w")
        for t in cls.teacher_list:
            line = f"{t.f_name}|{t.l_name}|{t.language}|{t.username}|{t.password}\n"
            file.write(line)
        file.close()

    @classmethod
    def register(cls, f_name, l_name, language, username, password):
        cls.teacher_list.append(Teacher(f_name, l_name, language, username, password))

    @classmethod
    def get_by_username(cls, username):
        for t in cls.teacher_list:
            if t.username == username:
                return t
        else:
            raise NoSuchUsernameException("Korisnicko ime ne postoji.")


