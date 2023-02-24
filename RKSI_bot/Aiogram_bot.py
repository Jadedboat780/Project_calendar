# -*- coding: utf8 -*-
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from id import TOKEN, Groups, CalendarID

storage = MemoryStorage()
bot = Bot(token=TOKEN, parse_mode='HTML')
dp = Dispatcher(bot, storage=storage)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):  # Тип сообщение
    Button1 = InlineKeyboardMarkup(row_width=5)
    btnMonth1 = InlineKeyboardButton(text=f"группы", callback_data="group")
    btnMonth2 = InlineKeyboardButton(text=f"преподаватели", callback_data="teacher")
    btnMonth3 = InlineKeyboardButton(text=f"аудитории", callback_data="audiences")
    Button1.add(btnMonth1, btnMonth2, btnMonth3)

    kb = [[types.KeyboardButton(text="Поддержка")],
          [types.KeyboardButton(text="FAQ")]]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)  # input_field_placeholder="Поддержка")

    await message.answer("Добрый день, напишите название группы, имя преподователя или номер аудитории, чтобы я мог дать вам ссылку на календарь.", reply_markup=keyboard)  # Показываем кнопки пользователю
    await message.answer(f'Вы также можете ознакомиться со списком доступных групп, преподователей и аудиторий:', reply_markup=Button1)


@dp.callback_query_handler(text='group')  # Выводит список всех доступных групп
async def group_list(callback: types.CallbackQuery):
    Button1 = InlineKeyboardMarkup(row_width=5)
    btnMonth1 = InlineKeyboardButton(text=f"скрыть", callback_data="clear")
    Button1.add(btnMonth1)
    group = 'ИБТ-11\nИБТ-12\nИБТ-13\nИБТ-22\nИБТ-23\nИБТ-31\nИБА-11\nИБА-12\nИБА-13\nИБА-24\nКС-41\nКС-42\nКС-44\nКС-46\nМТ-31\nМТ-32\nМТ-33\nМТ-34\nПИ-31\nПИ-32\nПИ-33\nПИ-41\nПИ-42ПИ-43\nРТ-21\nРТ-31\n4_СК-ДО\n3-ПОКС-ДО\nПОКС-31b\nПОКС-32b\nПОКС-33b\nПОКС-34w\nПОКС-35w\nПОКС-36w\nПОКС-37b\nИКС-11\nИКС-12\nИКС-13\nИКС-21\nИКС-22\nИКС-23\nИС-11\nИС-12\nИС-13\nИС-14\nИС-15\nИС-16\nИС-17\nИС-18\nИС-21\nИС-22\nИС-23\nИС-24\nИС-25\nИС-26\nИС-27\nИС-28\nИС-29\nИС-31\nСА-11\nСА-12\nСА-13\nСА-14\nСА-15\nСА-16\nСА-21\nСА-22\nСА-23\nСА-24\nСА-25\nСА-26\nСА-27\nСА-28\nСА-31\nСА-32\nСА-33\nСА-34\nСА-35\nСА-36\nСК-31\n4-ПОКС-ДО\n3-БУ-ДО'
    await callback.message.answer(f'<b>Список групп:</b>\n{group}', reply_markup=Button1)


@dp.callback_query_handler(text='teacher')  # Выводит список всех доступных преподователей
async def teacher_list(callback: types.CallbackQuery):
    Button1 = InlineKeyboardMarkup(row_width=5)
    btnMonth1 = InlineKeyboardButton(text=f"скрыть", callback_data="clear")
    Button1.add(btnMonth1)
    teacher = 'Алексеенко О.Н.\nАлешина В.В.\nАртамонова А.Г.\nАрутюнян А.Э.\nАрутюнян М.М.\nБайбекова И.Г.\nБельчич Д.С.\nБурда Е.Г.\nБурлуцкая А.В.\nБурыкина К.С.\nВащенко В.А.\nВойнова Е.С.\nГапоненко Е.Ф. \nГоворова О.А.\nГоличенко П.С.\nГригорьева Л.Ф.\nГрицай О.П.\nГуденко О.Н.\nГузов А.В.\nДемиденко А.В.\nДегтярев С.С.\nДозорова Е.В.\nДронова Р.В.\nДьяченко Е.О.\nЕрмолина Л.В.\nЖарехина И.М.\nЗаводнов Н.А.\nЗадорожный К.А.\nЗгонников Е.Ф.\nЗолотовская М.Ю.\nИваненков П.П.\nИванов В.С.\nКарачевцева Д.Г.\nКаламбет В.Б.\nКириленко А.А.\nКожухова В.В.\nНохрина Ю.В.\nПивнева М.А.\nРевнивцева О.А.\nСулавко С.Н.\nТрищук С.А.\nЯкубенко С.Я.\nМанакова О.П.\nМельникова М.В.\nМугутдинова Н.Ш.\nЧубкин Д.В.\nКомов Е.Ю.\nБолховитина О.И.\nДжалагония М.Ш.\nЛобова А.В.\nПильгун И.С.\nПрыгунова Т.А.\nПутинцева Ю.М.\nТроилина В.С.\nШвачич Д.С.\nСтарых О.А.\nМанджиева А.П.\nДолматова В.Ю.\nГивбрехт С.С.'
    teacher = teacher.split('\n')
    teacher.sort()
    teacher = '\n'.join(teacher)
    await callback.message.answer(f'<b>Список преподователей:</b>\n{teacher}', reply_markup=Button1)


@dp.callback_query_handler(text='audiences')  # Выводит список всех доступных аудиторий
async def audiences_list(callback: types.CallbackQuery):
    Button1 = InlineKeyboardMarkup(row_width=5)
    btnMonth1 = InlineKeyboardButton(text=f"скрыть", callback_data="clear")
    Button1.add(btnMonth1)
    audiences = 'каб - /05\nкаб - /06\nкаб - /103\nкаб - /104\nкаб - /106\nкаб - /109\nкаб - /110\nкаб - /110a\nкаб - /111\nкаб - /114\nкаб - /114a\nкаб - /118\nкаб - /121\nкаб - /122\nкаб - /209a\nкаб - /210\nкаб - /210a\nкаб - /212\nкаб - /213\nкаб - /214\nкаб - /216\nкаб - /216a\nкаб - /217\nкаб - /220\nкаб - /303\nкаб - /305\nкаб - /306\nкаб - /307\nкаб - /310\nкаб - /312\nкаб - /314\nкаб - /315a\nкаб - /316\nкаб - /318\nкаб - /320\nкаб - /322\nкаб - /323\nкаб - /324\nкаб - /325\nкаб - /326\nкаб - /401\nкаб - /404\nкаб - /406\nкаб - /406a\nкаб - /408\nкаб - /410\nкаб - /411\nкаб - /412\nкаб - /414\nкаб - /415\nкаб - /416\nкаб - /418\nкаб - /420\nкаб - /422\nкаб - с/з1\nкаб - с/з2\nкаб - с/з3\nкаб - с/з4\nкаб - с/з5\nкаб - с/з6\nкаб - с/з7\nкаб - с/з8\nкаб - с/з9\nкаб - Общ1-3\nкаб - Общ1-1\nкаб - Общ1\nкаб - Общ1-2\n'
    await callback.message.answer(f'<b>Вот список аудиторий:</b>\n{audiences}', reply_markup=Button1)


@dp.callback_query_handler(text='clear')  # Удаляет сообщение
async def message_clearing(callback: types.CallbackQuery):
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)


@dp.message_handler(text="Поддержка")  # Меню поддержки
async def support(message: types.Message):
    keyboard = InlineKeyboardMarkup()
    button = InlineKeyboardButton('Отменить отправку', callback_data='Close')
    keyboard.add(button)

    await Form.problem.set()
    await message.answer(
        '''Следующее сообщение будет отправлено в тех.поддержку. Напишите о вашей проблеме в виде одного сообщения. Если вы не желаете отправлять сообщение, то нажмите на /close''')


@dp.message_handler(state='*', commands='close')  # Досрочно завершает диалог
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.finish()
    await message.reply('Вы отменили отправку сообщения')


class Form(StatesGroup):
    problem = State()


@dp.message_handler(state=Form.problem)  # Принимает сообщения от пользоватля
async def process_schedule(message: types.Message, state: FSMContext):
    await bot.send_message('1102105550',
                           f'Сообщение о проблеме: \n{message.text} \n \n{message.from_user.last_name} {message.from_user.first_name} {message.from_user.id}')
    await bot.send_message(message.chat.id, 'Ваше сообщение было отправлено')
    await state.finish()  # Заканчиваем диалог


@dp.message_handler(text='FAQ')  # Меню часто задоваемые вопросы
async def help_support(message: types.Message):
    await message.reply('''1) Почему мои календари не отображаются в мобильном приложении?
 - Чтобы календари отображались в мобильном приложении, необходимо зайти в настройки мобильного приложения, где можно будет найти все календари, доступные вашему аккаунту. Нажмите на название нужного вам календаря и нажмите на кнопку "Синхронизация".
 \n2) Иногда, когда я захожу в календарь, расписание исчезает, но через несколько минут появляется. Почему это происходит?
 - Если в календаре исчесло ваше расписание, то это значит, что календарь начал обновлять своё расписание. Этот процесс происходит перед концом каждой пары, а само расписание исчезает не больше, чем на 2 минуты.''')


@dp.message_handler()  # Поиск расписания
async def bot_message(message: types.Message):
    search = True
    # Умный поиск преподователей и групп
    text = message.text
    text = text.lower()
    text_info = '''Скопируйте ссылку, но не переходите по ней. Далее зайдите на сайт Календря (https://workspace.google.com/intl/ru/products/calendar/) и нажмите войти. Дальше нажмите на 3 полоски сверху-слева, чтобы открыть главное меню. В главном меню в самом низу слева, в разделе "Другие календари", нажмите на кнопку "+" и выберете пункт "Добавить по URL", вставьте туда скопированный url календаря и всё будет готово'''

    Button1 = InlineKeyboardMarkup(row_width=5)
    btnMonth1 = InlineKeyboardButton(text=f"Видео инструкция", callback_data="mp4_instruction")
    Button1.add(btnMonth1)

    if text[0] == '/':
        if text[1:] in Groups:
            await message.answer(f'ID календаря кабинета {text[1:]}: {CalendarID[text[1:]]}\n{text_info}', reply_markup=Button1)
        else:
            await message.answer('Данный кабинет не найден')
    elif text[0: 3].isdigit():
        if text in Groups:
            await message.answer(f'ID календаря кабинета {text}: {CalendarID[text]}\n{text_info}', reply_markup=Button1)
        else:
            await message.answer('Данный кабинет не найден')
    else:
        if text in Groups:  # 1 проверка на совпадение
            if text in Groups:
                try:
                    await message.answer(f'ID календаря группы {text.upper()}: {CalendarID[text.upper()]}\n{text_info}', reply_markup=Button1)
                except:
                    await message.answer(
                        f'ID календаря преподователя {text.title()}: {CalendarID[text.title()]}\n{text_info}', reply_markup=Button1)
        else:
            for group in Groups:
                if text == group.split(' ')[0]:
                    try:
                        await message.answer(f'ID календаря группы {group.upper()}: {CalendarID[group.upper()]}\n{text_info}', reply_markup=Button1)
                        break
                    except:
                        await message.answer(
                            f'ID календаря преподователя {group.title()}: {CalendarID[group.title()]}\n{text_info}',
                            reply_markup=Button1)
                        break
            else:
                if search:
                    for group in Groups:  # 2 проверка на совпадение
                        if text[0:5] == group[0:5]:
                            Button2 = InlineKeyboardMarkup(row_width=5)
                            btnMonth1 = InlineKeyboardButton(text="Получить", callback_data="schedule")
                            Button2.add(btnMonth1)
                            try:
                                await message.answer(f'Может быть вы имели в виду: {group.title()}', reply_markup=Button2)
                                break
                            except:
                                await message.answer(f'Произошла ошибка \n<b>повторите позже</b>')
                                break
                    else:
                        if search:  # 3 проверка на совпадение (глубокая)
                            name = str(text)
                            num = len(str(text))  # Кол во букв в слове
                            its = 0  # Кол - во найденных букв в слове
                            win = 0  # Кол во совпадений
                            numbers = list()

                            for Teach in Groups:  # Сначало перебираем список и обрабатываем каждое слово в списке
                                for group in name:  # Перебираем каждую букву в введеном слове
                                    for j in Teach:  # Перебираем буквы в слове из списка
                                        if group == j:  # Находим совпадения
                                            its += 1  # Увеличеваем переменую на 1
                                            break  # Завершаем даную итерацию
                                else:
                                    if num == its:  # Если кол во найденных букв соответствует кол во букв в введеном слове
                                        if win >= 3:  # Сколько найденных групп или преподователей показать
                                            continue
                                        numbers.append(Teach)
                                        win += 1  # Увеличиваем переменную на 1
                                    its = 0
                            else:
                                if win == 0:  # Если поиск ничего не нашел
                                    await message.answer(
                                        'Поиск ничего не дал:(')  # Если ни один из трех итераторов ничего не дал
                                else:
                                    for group in numbers:
                                        Button2 = InlineKeyboardMarkup(row_width=5)
                                        btnMonth1 = InlineKeyboardButton(text=f"Получить", callback_data="schedule")
                                        Button2.add(btnMonth1)
                                        try:
                                            await message.answer(f'Может быть вы имели в виду: {group.title()}',
                                                                 reply_markup=Button2)
                                        except:
                                            await message.answer(f'Ошибка, повторите еще раз')
                                    await message.answer('Не нашли то, что искали? Уточните запрос')


@dp.callback_query_handler(text="schedule")  # Найденные группы и преподователи путем глубокого поиска
async def schedule(callback: types.CallbackQuery):
    texts = callback.message.text.split(': ')
    text_info = '''Скопируйте ссылку, но не переходите по ней. Далее зайдите на сайт Календря (https://workspace.google.com/intl/ru/products/calendar/) и нажмите войти. Дальше нажмите на 3 полоски сверху-слева, чтобы открыть главное меню. В главном меню в самом низу слева, в разделе "Другие календари", нажмите на кнопку "+" и выберете пункт "Добавить по URL", вставьте туда скопированный url календаря и всё будет готово'''

    Button1 = InlineKeyboardMarkup(row_width=5)
    btnMonth1 = InlineKeyboardButton(text=f"Видео инструкция", callback_data="mp4_instruction")
    Button1.add(btnMonth1)

    try:
        await callback.message.answer(
            f'ID календаря группы {texts[-1].upper()}: {CalendarID[texts[-1].upper()]}\n{text_info}',
            reply_markup=Button1)
    except:
        await callback.message.answer(
            f'ID календаря преподователя {texts[-1].title()}: {CalendarID[texts[-1].title()]}\n{text_info}',
            reply_markup=Button1)


@dp.callback_query_handler(text='mp4_instruction')  # Отправка видео инструкции пользователю
async def mp4instruction(callback: types.CallbackQuery):
    await callback.message.answer('Подождите, видео отправляется')
    await bot.send_video(callback.message.chat.id, open('TEST_VIDEO.mp4', 'rb'))

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)