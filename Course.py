from CustomExceptions import NoSuchTitleException


class Course:
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
            raise NoSuchTitleException("Course with entered title doesn't exist.")

    @classmethod
    def get_course_list(cls):
        return cls.course_list

    @classmethod
    def add_new_course(cls, title, price):
        cls.course_list.append(Course(title, price))

    @classmethod
    def save(cls):
        file = open("courses.txt", "w")
        for course in cls.course_list:
            line = course.title + "|" + str(course.price) + "\n"
            file.write(line)
        file.close()
