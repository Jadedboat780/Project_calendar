import googleapiclient
from google.oauth2 import service_account
from googleapiclient.discovery import build
import requests, bs4
import openpyxl
from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import date
import schedule
import re
from id import name_groups, name_teacher, CalendarID

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


def New_Events(text, description, day, time, color, group):  # Метод для загрузки данных в календарь для преподователей
    time = time.split(' — ')
    event = {
        'summary': text,
        'description': description,
        'colorId': color,
        'start': {
            'dateTime': f'{day}T{time[0]}:00+03:00',
        },
        'end': {
            'dateTime': f'{day}T{time[-1]}:00+03:00',
        }}
    creatings = service.events().insert(calendarId=CalendarID[group], body=event).execute()
    print('Создан ивент, его id: %s' % (creatings.get('id')))
    print("Был создан ивент, цвет", color)


class Parcer():

    def Par_Group(self):  # Парсинг расписания групп
        '''Пасрит расписание групп'''
        today = str(date.today())  # Текущая дата
        days = list()  # Засовываем дату (год-месяц-день) текущей пары
        shedule_group = list()  # Засовываем разделенное расписание
        Groups = str()  # Для хранения группы

        for group in name_groups:  # Цикл перебирает элементы из списка и парсит расписание соответствующей группы
            shedule_group.append(f"&{group}")
            wd.get('https://rksi.ru/schedule')
            select_group = wd.find_element(By.XPATH, '//*[@id="group"]')  # Парсим раздел группы
            list_group = select_group.text.split('\n')

            for i in list_group:
                if group in i:
                    select_group.send_keys(i)
            wd.find_element(By.XPATH, '/html/body/div[10]/div[1]/main/form[1]/input').click()
            temp = [i.text.replace('\n', '||') for i in wd.find_elements(By.XPATH, '//b | //p')][1:-4]

            for timetable in temp:  # Разделяем список на подсписок
                shedule_group.append(timetable.split('||'))

        for name in shedule_group:  # Обрабатываем данные
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
                New_Events(f'{name[1]}', f'Время: {name[0]}: {name[2]}', f'{days[-1]}', f'{name[0]}', '9', Groups)

    def Par_Techer(self):  # Парсинг расписания преподователей
        '''Парсит расписание преподователей'''
        shedule_teacher = list()  # Засовываем разделенное расписание
        today = str(date.today())  # Текущая дата
        days1 = list()  # Засовываем дату (год-месяц-день) текущей пары

        for teach in name_teacher:
            try:
                shedule_teacher.append(
                    f"&{teach}")  # Засовываем в этот список какого преподователя мы в данный момент парсим
                wd.get('https://rksi.ru/schedule')
                select_group = wd.find_element(By.XPATH, '//*[@id="teacher"]')  # Парсим раздел группы
                list_group = select_group.text.split('\n')

                for i in list_group:
                    if teach in i:
                        select_group.send_keys(i)
                wd.find_element(By.XPATH, '/html/body/div[10]/div[1]/main/form[2]/input').click()
                temp = [i.text.replace('\n', '||') for i in wd.find_elements(By.XPATH, '//b | //p')][1:-4]

                for i in temp:
                    shedule_teacher.append(i.split("||"))
            except:
                print('Selenium опять насрал2')

        for name in shedule_teacher:
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
                New_Events(f'{name[1]}', f'Время: {name[0]}: {name[2]}', f'{days1[-1]}', f'{name[0]}', '7', Teacher)

    def Planchette(self):
        '''Находит планшетку по id, скачивает её в виде exel файла и берёт из неё нужные данные'''
        response = requests.get(url='https://drive.google.com/drive/folders/1YC6-ZKWS0LR5oxnCrPwLi_gPLwDgW4j7?hl=ru')
        soup = bs4.BeautifulSoup(response.text, 'lxml')
        id = re.search(r'data-id="[\w\-\+/#\(\)\*&\^:<>\?\!%\$]+', str(soup)).group().replace('data-id="', '')

        with open('file_exel/planchette.xlsx', 'wb') as xlsx_file:
            planchette = requests.get(url=f'https://drive.google.com/uc?export=download&id={id}')
            xlsx_file.write(planchette.content)

        wb = openpyxl.load_workbook('file_exel/planchette.xlsx')
        couple_list = {
            '1 пара': '08:00 — 09:30', '2 пара': '09:40 — 11:10', '3 пара': '11:30 — 13:00', '4 пара': '13:10 — 14:40',
            '5 пара': '15:00 — 16:30', '6 пара': '16:40 — 18:10', '7 пара': '18:20 — 19:50'}

        for couple, time in couple_list.items():
            worksheet = wb[couple]
            date = worksheet['A1'].value.split('.')
            date = f'{date[2]}-{date[1]}-{date[0]}'

            for i in range(0, worksheet.max_row):
                my_list_1 = []
                my_list_2 = []

                for col in worksheet.iter_cols(1, 4):
                    a = col[i].value
                    if a != None:
                        my_list_1.append(a)

                if len(my_list_1) >= 4:
                    print([my_list_1[3], f'{time}: {my_list_1[2]} ауд {my_list_1[0]}', date, time, 9, my_list_1[1]])
                    New_Events(my_list_1[3], f'{time}: {my_list_1[2]} ауд {my_list_1[0]}', date, time, 9, my_list_1[1])

                for col in worksheet.iter_cols(5, 8):
                    a = col[i].value
                    if a != None:
                        my_list_2.append(a)

                if len(my_list_2) >= 4:
                    print([my_list_2[3], f'{time}: {my_list_2[2]} ауд {my_list_2[0]}', date, time, 9, my_list_2[1]])
                    New_Events(my_list_2[3], f'{time}: {my_list_2[2]} ауд {my_list_2[0]}', date, time, 9, my_list_2[1])


def main():
    while True:
        schedule.every().sunday.at('12:55').do(Parcer.Par_Group)
        schedule.every().sunday.at('14:00').do(Parcer.Par_Techer)
        for i in ['07:40', '08:00', '09:25', '09:38', '11:12', '11:26', '13:05', '14:43', '14:56', '16:36', '18:15']:
            schedule.every().day.at(i).do(Parcer.Planchette)


if __name__ == '__main__':
    main()