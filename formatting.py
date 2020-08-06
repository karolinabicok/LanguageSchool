import datetime


def date_formatted(date):
    date_list = date.split('/')
    for num in date_list:
        num = int(num)
    date_list = datetime.date(date_list[2], date_list[1], date_list[0])
    return date_list


def today_date_str_formatted():
    today = datetime.datetime.today()
    today = str(today.day) + '/' + str(today.month) + '/' + str(today.year)
    return today
