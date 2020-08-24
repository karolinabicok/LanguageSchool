from CustomExceptions import NoSuchUsernameException


class Teacher:
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
            raise NoSuchUsernameException("Username doesn't exist.")

    @classmethod
    def login(cls, username, password):
        for t in cls.teacher_list:
            if t.username == username and t.password == password:
                return True
        else:
            return False

    @classmethod
    def get_languages_list(cls):
        languages = []

        for t in cls.teacher_list:
            languages.append(t.language)

        languages = list(dict.fromkeys(languages))

        return languages

    @classmethod
    def print_teachers_and_languages(cls):
        for t in cls.teacher_list:
            print(t.username + " | " + t.language)

    @classmethod
    def teacher_in_list(cls, username):
        for t in cls.teacher_list:
            if t.username == username:
                return True
        else:
            return False

    @classmethod
    def teachers_by_language(cls, language):
        t_list = []
        for teacher in Teacher.teacher_list:
            if teacher.language == language:
                t_list.append(teacher.username)
        return t_list
