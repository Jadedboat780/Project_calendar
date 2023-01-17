import googleapiclient
from google.oauth2 import service_account
from googleapiclient.discovery import build
import requests, bs4
from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import date, datetime
import openpyxl
import datetime
import schedule
import re
import telebot
from id import name_groups, name_teacher, CalendarID, Token_bot, TG_Bot_ID

SCOPES = ['https://www.googleapis.com/auth/calendar']
calendarId = '35fc2b53f41517c857c7cd03942345f7ae6770f333eb04e36c768d03ce453e04@group.calendar.google.com'
SERVICE_ACCOUNT_FILE = 'TESTS.json'
credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = googleapiclient.discovery.build('calendar', 'v3', credentials=credentials)

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('window-size=1400,600')
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36')
wd = webdriver.Chrome(options=options)

bot = telebot.TeleBot(Token_bot)

id_events = list()  # Храним id ивентов которые надо удалить
Name_list = list()  # Хранит список всех преподователей и групп из планшетки

def start_message(id_admin, text): # Бот для отправки сообщения об ошибки
    for id in id_admin:
        bot.send_message(id, f"{text}")

def New_Events(text, description, day, time, color, group):  # Метод для загрузки данных в календарь для преподователей
    if '-' not in time:
        time = time.split(' — ')
    else:
        time = time.split('-')

    event = {
        'summary': text,
        'description': description,
        'colorId': str(color),
        'start': {
            'dateTime': f'{day}T{time[0]}:00+03:00',
        },
        'end': {
            'dateTime': f'{day}T{time[-1]}:00+03:00',
        }}
    try:
        creatings = service.events().insert(calendarId=CalendarID[group], body=event).execute()  # Выполняем запрос о создании ивента
    except Exception as e:
        start_message(TG_Bot_ID, f'Произошла ошибка \n'
                                 f'ошибка была вызвана этими данными: \n \n'
                                 f'{text} - {description} - {day} - {time} - {color} - {group} \n'
                                 f'описание ошибки: {e}')


def Delete_Events():
    global id_events
    num = -1  # Создаем переменную для поиска id в списке
    for i in id_events:  # Проходимся по списку
        try:
            num += 1  # Сразу же увеличиваем ее
            service.events().delete(calendarId=CalendarID[i], eventId=id_events[num + 1]).execute()  # Находим нужный
            print('Ивент был удален')
        except Exception as e:
            start_message(TG_Bot_ID, f'Была вызвана онибка в разделе: удаление ивентов \n'
                                     f'описание ошибки: {e}')

    id_events.clear()
    Parcer.Planchette()  # Запускаем функцию парсинга планшеток


def get_events_list(time):  # Принимает аргумент дата из планшетки
    global Name_list
    global id_events

    id_events.clear()  # Очищаем список

    for i in Name_list:
        try:
            now = datetime.datetime.utcnow().isoformat() + 'Z'
            events_result = service.events().list(calendarId=CalendarID[i], timeMin=now, maxResults=10, singleEvents=True, orderBy='startTime').execute()
            events = events_result.get('items', [])  # Ищем ивенты
            for event in events:  # Проходимся по найденным ивентам
                start = event['start'].get('dateTime')  # Записываем в переменную время ивента
                start = start.split('T')  # Разделяем на дату и время
                strs = event.get('id')  # Получаем id ивента
                if start[0] == time:  # если дата в ивенте == дате в планшетке
                    id_events.append(i)  # Записываем в список у какой группы мы парсили календарь
                    id_events.append(strs)  # добавляем в список id ивентов которые надо удалить
        except Exception as e:
            start_message(TG_Bot_ID, f'Была вызвана ошибка в разделе поиска id ивентов \n'
                                     f'Данные вызванные ошибку: {i} \n'
                                     f'описание ошибки: {e}')

    Name_list.clear()
    Delete_Events()


def planchette_id():
    try:
        response = requests.get(url='https://drive.google.com/drive/folders/1UH5pcJc0pxkYFWBMI_bNCxrdlApqv3nX')
        soup = bs4.BeautifulSoup(response.text, 'lxml')
        soup = soup.find_all('div', class_='Q5txwe')  # Достаем название планшетки

        for number, i in enumerate(soup, start=0):  # Проходимся по всем найденным планшеткам
            date = str(datetime.now()).split()[0]
            dts = date.split('-')
            date = f'{dts[-1]}.{dts[1]}.{dts[0]}'  # Преобразуем текущую дату в нужный вид
            plans = (i.text)[0:-5]  # Убираем с названия планшетки '.xlsx'

            if date == plans:  # Если текущая дата совпадает с датой планшетки
                response = requests.get(url='https://drive.google.com/drive/folders/1UH5pcJc0pxkYFWBMI_bNCxrdlApqv3nX')
                soup = bs4.BeautifulSoup(response.text, 'lxml')
                id_list = [i.replace('data-id="', '') for i in
                       re.findall(r'data-id="[\w\-\+/#\(\)\*&\^:<>\?\!%\$]+', str(soup))]
                data_exel(id=id_list[number])  # Запускаем скачивание планшетки по ее id
                break
    except Exception as e:
        start_message(TG_Bot_ID, f'Была вызвана ошибка в разделе поиска  планшеток \n'
                                 f'описание ошибки: {e} \n'
                                 f'!ИЗ-ЗА ОШИБКИ ДАЛЬНЕЙШАЯ РАБОТА ПРОГРАММЫ ОСТАНОВЛЕНА ДО ПОВТОРНОГО ЕГО ВЫЗОВА!')


def data_exel(id):  # Функция скачивания планшетки
    try:
        planchette = requests.get(url=f'https://drive.google.com/uc?export=download&id={id}')
        with open('planchette.xlsx', 'wb') as xlsx_file:
            xlsx_file.write(planchette.content)
        Parcer.planshet()  # Запускаем парсинг планшетки
    except Exception as e:
        start_message(TG_Bot_ID, 'Была вызвана ошибка в разделе скачивания планшетки \n'
                                 f'описание ошибки: {e} \n'
                                 f'!ИЗ-ЗА ОШИБКИ ДАЛЬНЕЙШАЯ РАБОТА ПРОГРАММЫ ОСТАНОВЛЕНА ДО ПОВТОРНОГО ЕГО ВЫЗОВА!')


class Parcer():  # Запускаем этот класс раз в неделю
    def Par_Group():  # Парсинг расписания групп
        '''Пасрит расписание групп'''
        shedule_group = list()  # Засовываем разделенное расписание
        today = str(date.today())  # Текущая дата
        days = list()  # Засовываем дату (год-месяц-день) текущей пары
        Groups = str()  # Для хранения группы

        wd.get('https://rksi.ru/schedule')
        select_group = wd.find_element(By.XPATH, '//*[@id="group"]')
        list_group = select_group.text.split('\n')  # Достаем весь список групп

        for i in list_group:  # Поиск всех преподователей и их парсинг
            try:
                if i in name_groups:  # Проверяем есть ли преподователь из списка на сайте
                    shedule_group.append(f"&{i}")  # Добавляем в список какую группу мы парсим сейчас
                    wd.get('https://rksi.ru/schedule')
                    select_group = wd.find_element(By.XPATH, '//*[@id="group"]')
                    list_group = select_group.text.split('\n')

                    select_group.send_keys(i)
                    wd.find_element(By.XPATH, '/html/body/div[10]/div[1]/main/form[1]/input').click()
                    temp = [i.text.replace('\n', '||') for i in wd.find_elements(By.XPATH, '//b | //p')][1:-4]

                    for j in temp:  # Разделяем список на подсписок
                        shedule_group.append(j.split('||'))
            except Exception as e:
                start_message(TG_Bot_ID, f'Была вызвана ошибка в разделе Парсинга расписания для групп \n'
                                    f'Данные вызванные ошибку: {i} \n'
                                    f'описание ошибки: {e}')

        for name in shedule_group:  # Обрабатываем данные
            try:
                if name[0] == "&":
                    Groups = f"{name[1:]}"
                if len(name[0]) >= 15 and len(name[0]) <= 23 and name[0][0:1].isdigit():
                    ns = name[0].split(',')  # Разделяем дату на 'день, месяц', 'день недели'
                    nd = name[0].split(" ")  # Разделяем дату на 'день', 'месяц', 'день недели'
                    ns.append(nd[1].replace(",", ""))  # Избавляемся от знака , в месяце и засовываем в список
                    day = f"{ns[0]}{ns[1]}"  # Засовываем день месяц день недели
                    ras = day.split()  # Храним список: день, месяц, день недели
                    month = {'января': '01', 'февраля': '02', 'марта': '03', 'апреля': '04', 'мая': '05', 'июня': '06',
                             'июля': '07', 'августа': '08', 'сентября': '09', 'октября': '10', 'ноября': '11',
                             'декабря': '12'}

                    if int(ras[0]) >= 1 and int(ras[0]) < 10:
                        days.append(f"{today[0:4]}-{month[ras[1]]}-0{ras[0]}")
                    else:
                        days.append(f"{today[0:4]}-{month[ras[1]]}-{ras[0]}")
                if len(name) == 3:  # Обработанные данные загружаем в календарь
                    print(f'{Groups} -- {name[1]} - Время: {name[0]}: {name[2]} день {days[-1]}')
                    New_Events(f'{name[1]}', f'Время: {name[0]}: {name[2]}', f'{days[-1]}', f'{name[0]}', '9', Groups)
            except Exception as e:
                start_message(TG_Bot_ID, f'Была вызвана ошибка в разделе Парсинга расписания для групп \n'
                                        f'Данные вызванные ошибку: {name} \n'
                                        f'описание ошибки: {e}')

    def Par_Techer():  # Парсинг расписания преподователей
        '''Парсит расписание преподователей'''
        shedule_teacher = list()  # Засовываем разделенное расписание
        today = str(date.today())  # Текущая дата
        days1 = list()  # Засовываем дату (год-месяц-день) текущей пары

        wd.get('https://rksi.ru/schedule')
        select_group = wd.find_element(By.XPATH, '//*[@id="teacher"]')
        list_teachers = select_group.text.split('\n')

        for i in list_teachers:  # Поиск всех преподователей и их парсинг
            try:
                if i in name_teacher:  # Проверяем есть ли преподователь из списка на сайте
                    shedule_teacher.append(f"&{i}")  # Засовываем в этот список какого преподователя мы в данный момент парсим
                    print(f'Сейчас я парсю: {i}')
                    wd.get('https://rksi.ru/schedule')
                    select_group = wd.find_element(By.XPATH, '//*[@id="teacher"]')
                    list_teachers = select_group.text.split('\n')
                    select_group.send_keys(str(i))
                    wd.find_element(By.XPATH, '/html/body/div[10]/div[1]/main/form[2]/input').click()
                    temp = [i.text.replace('\n', '||') for i in wd.find_elements(By.XPATH, '//b | //p')][1:-4]

                    for j in temp:
                        shedule_teacher.append(j.split("||"))
            except Exception as e:
                start_message(TG_Bot_ID, f'Была вызвана ошибка в разделе Парсинга расписания для преподователей \n'
                                    f'Данные вызванные ошибку: {i} \n'
                                    f'описание ошибки: {e}')

        for name in shedule_teacher:
            try:
                if name[0] == "&":
                    Teacher = f'{name[1:]}'  # вписываем преподователя которого мы парсим убирая триггерный символ

                if len(name[0]) >= 15 and len(name[0]) <= 23 and name[0][0:1].isdigit():
                    ns = name[0].split(',')  # Разделяем дату на 'день, месяц', 'день недели'
                    nd = name[0].split(" ")  # Разделяем дату на 'день', 'месяц', 'день недели'
                    ns.append(nd[1].replace(",", ""))  # Избавляемся от знака , в месяце и засовываем в список
                    day = f"{ns[0]}{ns[1]}"  # Засовываем день месяц день недели
                    ras = day.split()  # Храним список: день, месяц, день недели
                    month = {'января': '01', 'февраля': '02', 'марта': '03', 'апреля': '04', 'мая': '05', 'июня': '06',
                             'июля': '07', 'августа': '08', 'сентября': '09', 'октября': '10', 'ноября': '11',
                             'декабря': '12'}

                    if int(ras[0]) >= 1 and int(ras[0]) < 10:
                        days1.append(f"{today[0:4]}-{month[ras[1]]}-0{ras[0]}")
                    else:
                        days1.append(f"{today[0:4]}-{month[ras[1]]}-{ras[0]}")

                if len(name) == 3:
                    print(f'{Teacher} -- {name[1]} - Время: {name[0]}: {name[2]} день {days1[-1]}')
                    New_Events(f'{name[1]}', f'Время: {name[0]}: {name[2]}', f'{days1[-1]}', f'{name[0]}', '7', Teacher)
            except Exception as e:
                start_message(TG_Bot_ID, f'Была вызвана ошибка в разделе Парсинга расписания для преподователей \n'
                                    f'Данные вызванные ошибку: {name} \n'
                                    f'описание ошибки: {e}')

    def planshet():
        global Name_list
        global worksheet
        wb1 = openpyxl.load_workbook('planchette.xlsx')
        couple_list = ['1 пара', '2 пара', '3 пара', '4 пара', '5 пара', '6 пара', '7 пара']
        dates = ''

        try:
            for couple in couple_list:
                worksheet = wb1[couple]
                dates = str(worksheet['B1'].value).split()

                dates = dates[0].split('-')
                dates = f'{dates[2]}-{dates[1]}-{dates[0]}'

                for i in range(0, worksheet.max_row):
                    my_list_1 = []
                    my_list_2 = []

                    for col in worksheet.iter_cols(2, 5):
                        a = col[i].value
                        if a != None:
                            my_list_1.append(a)

                    if len(my_list_1) >= 4:
                        group = my_list_1[1].replace('  ', ' ')  # Убираем лишние пробелы в названии группы
                        prepods = my_list_1[2].replace('  ', ' ')  # Убираем лишние пробелы в имени преподователя
                        if 'КПК' not in group and 'КПК' not in prepods:
                            if '/' not in group:
                                Name_list.append(group)
                                Name_list.append(prepods)
                            else:
                                groups = group.split('/')

                                Name_list.append(groups[0])
                                Name_list.append(prepods)
                                Name_list.append(groups[-1])
                                Name_list.append(prepods)

                    for col in worksheet.iter_cols(6, 9):
                        a = col[i].value

                        if a != None:
                            my_list_2.append(a)

                    if len(my_list_2) >= 4:
                        group = my_list_2[1].replace('  ', ' ')
                        prepods = my_list_2[2].replace('  ', ' ')
                        if '/' not in group:
                            Name_list.append(group)
                            Name_list.append(prepods)
                        else:
                            groups = group.split('/')

                            Name_list.append(groups[0])
                            Name_list.append(prepods)
                            Name_list.append(groups[-1])
                            Name_list.append(prepods)

        except Exception as e:
            start_message(TG_Bot_ID, f'Была вызвана ошибка в разделе парсинга планшетки(1) \n'
                                     f'описание ошибки: {e}')
            get_events_list(dates)  # Вызывает функцию для поиска и удаления ивентов в календаре
        finally:
            get_events_list(dates)  # Вызывает функцию для поиска и удаления ивентов в календаре

    def Planchette():
        '''Находит планшетку по id, скачивает её в виде exel файла и берёт из неё нужные данные'''  # response = requests.get(url='https://drive.google.com/drive/folders/1UH5pcJc0pxkYFWBMI_bNCxrdlApqv3nX?hl=ru')    # soup = bs4.BeautifulSoup(response.text, 'lxml')    # id_list = [i.replace('data-id="', '') for i in re.findall(r'data-id="[\w\-\+/#\(\)\*&\^:<>\?\!%\$]+', str(soup))]    #    # with open('planchette.xlsx', 'wb') as xlsx_file:    #     planchette = requests.get(url=f'https://drive.google.com/uc?export=download&id={id_list[1]}')    #     xlsx_file.write(planchette.content)    wb = openpyxl.load_workbook('file_exel/planchette.xlsx')
        wb1 = openpyxl.load_workbook('planchette.xlsx')
        couple_list = ['1 пара', '2 пара', '3 пара', '4 пара', '5 пара', '6 пара', '7 пара']

        try:
            for couple in couple_list:
                worksheet = wb1[couple]
                dates = str(worksheet['B1'].value).split()
                dates = dates[0].split('-')
                dates = f'{dates[2]}-{dates[1]}-{dates[0]}'
                couple_time = worksheet['A1'].value
                spisok = list()

                for i in range(0, worksheet.max_row):
                    my_list_1 = []
                    my_list_2 = []
                    for col in worksheet.iter_cols(2, 5):
                        a = col[i].value
                        if a != None:
                            my_list_1.append(a)

                    if len(my_list_1) >= 4:
                        if '/' in my_list_1[1]:
                            for i in my_list_1[1].split('/'):
                                spisok.append([[couple_time], [my_list_1[3], f'{couple_time}: {my_list_1[2]} ауд {my_list_1[0]}', dates, couple_time, 9, i]])
                        else:
                            spisok.append([[couple_time], [my_list_1[3], f'{couple_time}: {my_list_1[2]} ауд {my_list_1[0]}', dates, couple_time, 9, my_list_1[1]]])

                    for col in worksheet.iter_cols(6, 9):
                        a = col[i].value

                        if a != None:
                            my_list_2.append(a)

                    if len(my_list_2) >= 4:
                        if '/' in my_list_2[1]:
                            for i in my_list_2[1].split('/'):
                                spisok.append([[couple_time], [my_list_2[3], f'{couple_time}: {my_list_2[2]} ауд {my_list_2[0]}', dates, couple_time, 9, i]])
                        else:
                            spisok.append([[couple_time], [my_list_2[3], f'{couple_time}: {my_list_2[2]} ауд {my_list_2[0]}', dates, couple_time, 7, my_list_2[1]]])

                date = str(datetime.now())
                date = date.split()
                date = date[-1].split(':')
                Nowtime = f'{int(date[0])}:{date[1]}'

                for i in spisok:
                    time = i[0][0].split('-')
                    if Nowtime <= time[1]:
                        New_Events(f'{i[1][0]}', f'Время: {i[1][1]}', f'{i[1][2]}', f'{i[1][3]}', f'9', i[1][-1])

                for i in spisok:
                    time = i[0][0].split('-')
                    if Nowtime <= time[1]:
                        teacher = i[1][1].split('. ')
                        teacher = teacher[0].split(': ')
                        teacher = teacher[1].replace('  ', ' ')

                        try:
                            text = i[1][1].split(': ')
                            text1 = text[-1].split('. ')
                            New_Events(f'{i[1][0]}', f'Время: {text[0]}: {i[1][-1]} {text1[-1]}', f'{i[1][2]}', f'{i[1][3]}', f'7', f'{teacher}.')
                        except Exception as e:
                            start_message(TG_Bot_ID, f'Была вызвана ошибка в разделе парсинга планшетки(2) \n'
                                                     f'Данные вызванные ошибку: {i}'
                                                     f'описание ошибки: {e}')
        except Exception as e:
            start_message(TG_Bot_ID, f'Была вызвана ошибка в разделе парсинга планшетки(2) \n'
                                     f'описание ошибки: {e}')

def Monday():
    for time in ['07:25', '09:00', '10:40', '12:35', '14:10', '16:00', '17:45']:
        schedule.every().day.at(time).do(planchette_id)


def Tuesday():
    for time in ['07:25', '09:00', '10:40', '12:35', '14:10', '16:00', '17:45']:
        schedule.every().day.at(time).do(planchette_id)


def Wednesday():
    for time in ['07:25', '09:00', '10:40', '12:35', '14:10', '16:00', '17:45']:
        schedule.every().day.at(time).do(planchette_id)


def Thursday():
    for time in ['07:25', '09:00', '10:40', '12:35', '14:10', '16:00', '17:45']:
        schedule.every().day.at(time).do(planchette_id)


def Friday():
    for time in ['07:25', '09:00', '10:40', '12:35', '14:10', '16:00', '17:45']:
        schedule.every().day.at(time).do(planchette_id)


def Saturday():
    for time in ['07:25', '09:00', '10:40', '12:35', '14:10', '16:00', '17:45']:
        schedule.every().day.at(time).do(planchette_id)


def main():
    schedule.every().monday.at('07:35').do(Monday)
    schedule.every().tuesday.at('07:34').do(Tuesday)
    schedule.every().wednesday.at('07:35').do(Wednesday)
    schedule.every().thursday.at('07:35').do(Thursday)
    schedule.every().friday.at('07:35').do(Friday)
    schedule.every().saturday.at('07:35').do(Saturday)
    schedule.every().sunday.at('12:55').do(Parcer.Par_Group)
    schedule.every().sunday.at('14:00').do(Parcer.Par_Techer)


    while True:
        schedule.run_pending()

if __name__ == '__main__':
    main()

bot.infinity_polling()