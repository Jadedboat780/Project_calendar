import googleapiclient
from google.oauth2 import service_account
from googleapiclient.discovery import build
from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import date
import time
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

def New_Events1(text, description, day, time, group): # Метод для загрузки данных в календарь для преподователей
  time = time.split(' — ')
  event = {
            'summary': text,
            'description': description,
            'colorId': '7',
            'start': {
                'dateTime': f'{day}T{time[0]}:00+03:00',
            },
            'end': {
                'dateTime': f'{day}T{time[-1]}:00+03:00',
            }}
  creatings = service.events().insert(calendarId=CalendarID[group], body=event).execute()
  print('Создан ивент, его id: %s' % (creatings.get('id')))

def New_Events(day, time, group, text='', description=''): # Метод для загрузки данных в календарь для групп
  time = time.split(' — ')
  event = {
            'summary': f'{text}',
            'description': f'{description}',
            'colorId': '9',
            'start': {
                'dateTime': f'{day}T{time[0]}:00+03:00',
            },
            'end': {
                'dateTime': f'{day}T{time[-1]}:00+03:00',
            }}
  creatings = service.events().insert(calendarId=CalendarID[group], body=event).execute()
  print('Создан ивент, его id: %s' % (creatings.get('id')))

def Par_Group(): # Парсинг расписания групп
  today = str(date.today()) # Текущая дата
  days = list() # Засовываем дату (год-месяц-день) текущей пары
  shedule_group = list() # Засовываем разделенное расписание
  Groups = str()  # Для хранения группы

  try:
    for group in name_groups:  # Цикл перебирает элементы из списка и парсит расписание соответствующей группы
      shedule_group .append(f"&{group}")
      wd.get('https://rksi.ru/schedule')
      select_group = wd.find_element(By.XPATH, '//*[@id="group"]')  # Парсим раздел группы
      list_group = select_group.text.split('\n')

      for i in list_group:
        if group in i:
          select_group.send_keys(i)
      wd.find_element(By.XPATH, '/html/body/div[10]/div[1]/main/form[1]/input').click()
      temp = [i.text.replace('\n', '||') for i in wd.find_elements(By.XPATH, '//b | //p')][1:-4]

      for timetable in temp:  # Разделяем список на подсписок
        shedule_group .append(timetable.split('||'))
  except:
      print("Eror")

  for name in shedule_group :  # Обрабатываем данные
    if name[0] == "&":
      Groups = name[1:]

    if len(name[0]) >= 15 and len(name[0]) <= 23 and name[0][0:1].isdigit():
      ns = name[0].split(',')# Разделяем дату на 'день, месяц', 'день недели'
      nd = name[0].split(" ") # Разделяем дату на 'день', 'месяц', 'день недели'
      ns.append(nd[1].replace(",", "")) # Избавляемся от знака , в месяце и засовываем в список
      day = f"{ns[0]}{ns[1]}" # Засовываем день месяц день недели
      ras = day.split() # Храним список: день, месяц, день недели
      month = {'января': '01', 'февраля': '02', 'марта': '03', 'апреля': '04', 'мая': '05', 'июня': '06',
               'июля': '07', 'августа': '08', 'сентября': '09', 'октября': '10', 'ноября': '11', 'декабря': '12'}

      if int(ras[0]) >= 1 and int(ras[0]) < 10:
        days.append(f"{today[0:4]}-{month[ras[1]]}-0{ras[0]}")
      else:
        days.append(f"{today[0:4]}-{month[ras[1]]}-{ras[0]}")

    if len(name) == 3:  # Обработанные данные загружаем в календарь
      #print(f'{days[-1]} {name[0]} {Groups} {name[1]} Время: {name[0]}: {name[2]}')
      New_Events(f'{days[-1]}', f'{name[0]}', Groups, f'{name[1]}', f'Время: {name[0]}: {name[2]}')   # В аргумнтах указываем в какой календарь загружать

def Par_Techer(): # Парсинг расписания преподователей
    shedule_teacher = list() # Засовываем разделенное расписание
    today = str(date.today()) # Текущая дата
    days1 = list() # Засовываем дату (год-месяц-день) текущей пары

    for teach in name_teacher:
      try:
        shedule_teacher.append(f"&{teach}") # Засовываем в этот список какого преподователя мы в данный момент парсим
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
          print('Eror')

    for name in shedule_teacher:
      if name[0] == "&":
          Teacher = f'{name[1:]}' # вписываем преподователя которого мы парсим убирая триггерный символ

      if len(name[0]) >= 15 and len(name[0]) <= 23 and name[0][0:1].isdigit():
          ns = name[0].split(',')# Разделяем дату на 'день, месяц', 'день недели'
          nd = name[0].split(" ") # Разделяем дату на 'день', 'месяц', 'день недели'
          ns.append(nd[1].replace(",", "")) # Избавляемся от знака , в месяце и засовываем в список
          day = f"{ns[0]}{ns[1]}" # Засовываем день месяц день недели
          ras = day.split() # Храним список: день, месяц, день недели
          month = {'января': '01', 'февраля': '02', 'марта': '03', 'апреля': '04', 'мая': '05', 'июня': '06',
                   'июля': '07', 'августа': '08', 'сентября': '09', 'октября': '10', 'ноября': '11', 'декабря': '12'}

          if int(ras[0]) >= 1 and int(ras[0]) < 10:
            days1.append(f"{today[0:4]}-{month[ras[1]]}-0{ras[0]}")
          else:
            days1.append(f"{today[0:4]}-{month[ras[1]]}-{ras[0]}")

      if len(name) == 3:
        #print(f'{days1[-1]} {name[0]} {Teacher} {name[1]} Время: {name[0]}: {name[2]}')
        New_Events1(f'{name[1]}', f'Время: {name[0]}: {name[2]}', f'{days1[-1]}', f'{name[0]}', Teacher)

def main():

  while True:
    Par_Group()
    Par_Techer()
    time.sleep(60 * 60 * 24 * 7)

if __name__ == '__main__':
    main()