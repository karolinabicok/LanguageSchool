from CustomExceptions import NoSuchTitleException


class Course(object):
    course_list = []

    def __init__(self, title, price):
        self.title = title
        self.price = price

    def __str__(self):
        return f'{self.title}: ${self.price}'

    @classmethod
    def load(cls):
        file = open("courses.txt", "r")
        for line in file:
            attributes = line.strip().split("|")
            c = Course(title=attributes[0], price=int(attributes[1]))
            cls.course_list.append(c)
        file.close()

    @classmethod
    def get_by_title(cls, title):
        for c in cls.course_list:
            if title == c.title:
                return c
        else:
            raise NoSuchTitleException("Ne postoji kurs sa datim imenom.")

    @classmethod
    def get_course_list(cls):
        return cls.course_list

    @classmethod
    def add_new_course(cls, title, price):
        cls.course_list.append(Course(title, price))