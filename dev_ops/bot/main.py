#aiogram 2.14.3
from aiogram import Bot,Dispatcher,executor,types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import re
from command_ssh import *
import time
from sql import *

import logging
logging.basicConfig(filename='Log.txt',level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')


bot = Bot(token='6572075975:AAHR9lTpU0AhPlOboiMGQSsnqwZugJRpq8c')
storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=storage)

class emailState(StatesGroup):
    email = State()
class email_insert_State(StatesGroup):
    email = State()
class phoneState(StatesGroup):
    phone = State()

class phone_insert_State(StatesGroup):
    phone = State()
class passwordState(StatesGroup):
    password = State()
class argState(StatesGroup):
    arg = State()


@dp.message_handler(commands=['find_email'])
async def find_email(message: types.Message, state: FSMContext):
    logging.info('Вызов find_email')
    await message.answer("Введите текст в котором надо найти email:")
    await message.answer("/close - для выхода из функции")
    await emailState.email.set()

@dp.message_handler(state=emailState.email)
async def process_email(message: types.Message, state: FSMContext):
    response = message.text
    logging.debug(f'find_email поймал сообщение от пользователя:{response}')
    if response != '/close':
        logging.debug(f"find_email провалился в response != '/close' и начинает выполнение функции re.findall")
        emails = re.findall(r'[\w\.-]+@[\w\.-]+\.[\w\.-]+', response)
        if emails:
            logging.debug(f"find_email - re.findall - нашел нужные значения")
            await message.answer(f"Найденные email: {', '.join(emails)}")
            await message.answer("Хотите записать эти email-адреса? (д/н)")
            logging.debug(f"find_email - отчет отправлен пользователю и предложен выбор для внесения в базу")
            async with state.proxy() as data:
                data['emails'] = emails
            await email_insert_State.email.set()
        else:
            logging.debug(f"find_email - re.findall - не нашел нужные значения")
            await message.answer("Email не найдены")
            await message.answer("/close - для выхода из функции")
            logging.debug(f"find_email - отчет отправлен пользователю")
    else:
        logging.debug(f"find_email - провалился в завершение функции")
        await message.answer('Вы вышли из функции...')
        logging.debug('find_email - отправил сообщение <завершил работу> ')
        await state.finish()
        logging.debug('find_email - закрыл state и завершил работу')

@dp.message_handler(state=email_insert_State.email)
async def process_email_insert(message: types.Message, state: FSMContext):
    response = message.text
    logging.debug(f'process_email_insert поймал сообщение от пользователя:{response}')
    if response == 'д':
        async with state.proxy() as data:
            emails = data['emails']
        await message.answer(f'Записываем email-адреса: {", ".join(emails)}')
        logging.debug(f'process_email_insert начинает запись')
        answer = ''
        for i in emails:
            res = email_insert(i)
            answer += f'{i}:{res}\n'
        await message.answer(answer)
    else:
        await message.answer('Email-адреса не записаны.')
    await message.answer('Работа функции закончена.')
    await state.finish()
    logging.debug('process_email_insert - закрыл state и завершил работу')




@dp.message_handler(commands=['find_phone_number'])
async def find_email(message: types.Message):
    logging.info('Вызов find_phone_number')
    await message.answer("Введите текст в котором надо найти номера телефонов:")
    await message.answer("/close - для выхода из функции")
    await phoneState.phone.set()
@dp.message_handler(state=phoneState.phone)
async def process_phone(message: types.Message, state: FSMContext):
    response = message.text
    logging.debug(f'find_phone_number поймал сообщение от пользователя:{response}')
    if response != '/close':
        logging.debug(f"find_phone_number провалился в response != '/close' и начинает выполнение функции re.findall")
        phone_pattern = r'(\+7|8)?[\s-]?\(?(\d{1,3})\)?[\s-]?(\d{3})[\s-]?(\d{2})[\s-]?(\d{2})'
        phone_numbers = re.findall(phone_pattern, response)
        result = []
        logging.debug(f'Начало number in ({phone_numbers})')
        for number in phone_numbers:
            formatted_number = ''.join(number[1:])
            result.append(formatted_number)
        if result:
            logging.debug(f'find_phone_number нашел телефонные номера')
            await message.answer(f"Найденные номера телефонов: {', '.join(result)}")
            await message.answer("Хотите записать эти email-адреса? (д/н)")
            logging.debug(f"find_phone_number - отчет отправлен пользователю и предложен выбор для внесения в базу")
            async with state.proxy() as data:
                data['phones'] = result
            await phone_insert_State.phone.set()
        else:
            logging.debug(f'find_phone_number не нашел телефонные номера')
            await message.answer("Телефоны не найдены")
            await message.answer("/close - для выхода из функции")
            logging.debug(f'find_phone_number отправил отчет')
    else:
        await message.answer('Вы вышли из функции...')
        await state.finish()
        logging.debug(f'find_phone_number отправил отчет и завершил работу')
@dp.message_handler(state=phone_insert_State.phone)
async def process_phone_insert(message: types.Message, state: FSMContext):
    response = message.text
    logging.debug(f'process_phone_insert поймал сообщение от пользователя:{response}')
    if response == 'д':
        async with state.proxy() as data:
            phones = data['phones']
        await message.answer(f'Записываем email-адреса: {", ".join(phones)}')
        logging.debug(f'process_email_insert начинает запись')
        answer = ''
        for i in phones:
            res = email_insert(i)
            answer += f'{i}:{res}\n'
        await message.answer(answer)
    else:
        await message.answer('Телефоны не записаны.')
    await message.answer('Работа функции закончена.')
    await state.finish()
    logging.debug('process_email_insert - закрыл state и завершил работу')


@dp.message_handler(commands=['verify_password'])
async def find_email(message: types.Message):
    logging.debug(f'Вызов verify_password')
    await message.answer("Введите пароль:")
    await message.answer("/close - для выхода из функции")
    await passwordState.password.set()
@dp.message_handler(state=passwordState.password)
async def process_phone(message: types.Message, state: FSMContext):
    password = message.text
    logging.debug(f'verify_password поймал сообщение от пользователя:{password}')
    if password != '/close':
        logging.debug(f'verify_password начинает выполнение проверки')
        if len(password) < 8 or not re.search(r'[A-Z]', password) or not re.search(r'[a-z]', password) or not re.search(r'\d', password) or not re.search(r'[!@#$%^&*()]', password):
            logging.debug(f'verify_password результат проверки - Пароль простой')
            await message.answer('Пароль простой')
            await message.answer("/close - для выхода из функции")
            logging.debug(f'verify_password отправил отчет')

        else:
            logging.debug(f'verify_password результат проверки - Пароль сложный')
            await message.answer('Пароль сложный')
            await message.answer("/close - для выхода из функции")
            logging.debug(f'verify_password отправил отчет')
    else:
        await message.answer('Вы вышли из функции...')
        await state.finish()
        logging.debug(f'verify_password отправил отчет и завершил работу')

#-----SSH---
@dp.message_handler(commands=['get_release'])
async def release(message: types.Message):
    logging.debug(f'Вызов get_release')
    logging.debug(f'get_release вызывает get_release')
    response = get_release()
    logging.debug(f'get_release - получил ответ')
    logging.debug(f'get_release - начинает отправку отчета')
    await message.answer(response)
    logging.debug(f'get_release - отправил отчет, завершил работу')
@dp.message_handler(commands=['get_uname'])
async def uname(message: types.Message):
    logging.debug(f'Вызов get_uname')
    logging.debug(f'get_uname вызывает get_uname')
    response = get_uname()
    logging.debug(f'get_uname - получил ответ')
    logging.debug(f'get_uname - начинает отправку отчета')
    await message.answer(response)
    logging.debug(f'get_uname - отправил отчет, завершил работу')
@dp.message_handler(commands=['get_uptime'])
async def uptime(message: types.Message):
    logging.debug(f'Вызов get_uptime')
    logging.debug(f'get_uptime вызывает get_uname')
    response = get_uptime()
    logging.debug(f'get_uptime - получил ответ')
    logging.debug(f'get_uptime - начинает отправку отчета')
    await message.answer(response)
    logging.debug(f'get_uptime - отправил отчет, завершил работу')
@dp.message_handler(commands=['get_df'])
async def df(message: types.Message):
    logging.debug(f'Вызов get_df')
    logging.debug(f'get_df вызывает get_df')
    response = get_df()
    logging.debug(f'get_df - получил ответ')
    logging.debug(f'get_df - начинает отправку отчета')
    await message.answer(response)
    logging.debug(f'get_df - отправил отчет, завершил работу')
@dp.message_handler(commands=['get_free'])
async def free(message: types.Message):
    logging.debug(f'Вызов get_free')
    logging.debug(f'get_free вызывает get_free')
    response = get_free()
    logging.debug(f'get_free - получил ответ')
    logging.debug(f'get_free - начинает отправку отчета')
    await message.answer(response)
    logging.debug(f'get_free - отправил отчет, завершил работу')
@dp.message_handler(commands=['get_mpstat'])
async def mpstat(message: types.Message):
    logging.debug(f'Вызов get_mpstat')
    logging.debug(f'get_mpstat вызывает get_mpstat')
    responce = get_mpstat()
    logging.debug(f'get_mpstat - получил ответ')
    logging.debug(f'get_mpstat - начинает проверку длины')
    if len(responce) > 4096:
        logging.debug(f'get_mpstat - длина больше 4096')
        n = len(responce) // 4096
        logging.debug(f'get_mpstat - найдено целое число делений ответа = {n}')
        logging.debug(f'get_mpstat - запуск цикла отправки сообщений в интервале от 0 до {n}')
        for i in range(n):
            await message.answer(responce[:4096])
            logging.debug(f'get_mpstat {i}-е сообщение отправлено')
            responce = responce[4096:]
            logging.debug(f'get_mpstat - удалил первые 4096 символ из ответа от функции')
            time.sleep(1)
            logging.debug(f'get_mpstat - ушел в сон на 1 секунду')
        logging.debug(f'get_mpstat - заверил цикл, начинает проверку остатка ответа')
        if len(responce) > 0:
            logging.debug(f'get_mpstat - остаток найден')
            await message.answer(responce)
            logging.debug(f'get_mpstat - отправил последнее сообщение и завершил работу')
    else:
        logging.debug(f'get_mpstat - длина ответа меньше 4096')
        await message.answer(responce)
        logging.debug(f'get_mpstat - отправил отчет и завершил работу')
@dp.message_handler(commands=['get_w'])
async def w(message: types.Message):
    logging.debug(f'Вызов get_w')
    logging.debug(f'get_w вызывает get_w')
    response = get_w()
    logging.debug(f'get_w - получил ответ')
    logging.debug(f'get_w - начинает отправку отчета')
    await message.answer(response)
    logging.debug(f'get_w - отправил отчет, завершил работу')
@dp.message_handler(commands=['get_auths'])
async def auths(message: types.Message):
    logging.debug(f'Вызов get_auths')
    logging.debug(f'get_auths вызывает get_auths')
    response = get_auths()
    logging.debug(f'get_auths - получил ответ')
    logging.debug(f'get_auths - начинает отправку отчета')
    await message.answer(response)
    logging.debug(f'get_auths - отправил отчет, завершил работу')
@dp.message_handler(commands=['get_critical'])
async def critical(message: types.Message):
    logging.debug(f'Вызов get_critical')
    logging.debug(f'get_critical вызывает get_critical')
    response = get_critical()
    logging.debug(f'get_critical - получил ответ')
    logging.debug(f'get_critical - начинает отправку отчета')
    await message.answer(response)
    logging.debug(f'get_critical - отправил отчет, завершил работу')
@dp.message_handler(commands=['get_ps'])
async def ps(message: types.Message):
    logging.debug(f'Вызов get_ps')
    logging.debug(f'get_ps вызывает get_ps')
    responce = get_ps()
    logging.debug(f'get_ps - получил ответ')
    logging.debug(f'get_ps - начинает проверку длины ответа')
    if len(responce) > 4096:
        logging.debug(f'get_ps - длина ответа больше 4096')
        n = len(responce) // 4096
        logging.debug(f'get_ps - найдено целое число делений ответа = {n}')
        logging.debug(f'get_ps - запуск цикла отправки сообщений в интервале от 0 до {n}')
        for i in range(n):
            await message.answer(responce[:4096])
            logging.debug(f'get_ps {i}-е сообщение отправлено')
            responce = responce[4096:]
            logging.debug(f'get_ps - удалил первые 4096 символ из ответа от функции')
            time.sleep(1)
            logging.debug(f'get_ps - ушел в сон на 1 секунду')
        logging.debug(f'get_ps - заверил цикл, начинает проверку остатка ответа')
        if len(responce) > 0:
            logging.debug(f'get_ps - остаток найден')
            await message.answer(responce)
            logging.debug(f'get_ps - отправил последнее сообщение и завершил работу')
    else:
        logging.debug(f'get_ps - длина ответа меньше 4096')
        await message.answer(responce)
        logging.debug(f'get_ps - отправил отчет и завершил работу')
@dp.message_handler(commands=['get_ss'])
async def ss(message: types.Message):
    logging.debug(f'Вызов get_ss')
    logging.debug(f'get_ss вызывает get_ss')
    response = get_ss()
    logging.debug(f'get_ss - получил ответ')
    logging.debug(f'get_ss - начинает отправку отчета')
    await message.answer(response)
    logging.debug(f'get_ss - отправил отчет, завершил работу')
@dp.message_handler(commands=['get_services'])
async def services(message: types.Message):
    logging.debug(f'Вызов get_services')
    logging.debug(f'get_services вызывает get_services')
    response = get_services()
    logging.debug(f'get_services - получил ответ')
    logging.debug(f'get_services - начинает отправку отчета')
    await message.answer(response)
    logging.debug(f'get_services - отправил отчет, завершил работу')

@dp.message_handler(commands=['get_apt_list'])
async def apt_list_arg(message: types.Message):
    logging.debug(f'Вызов get_apt_list')
    await message.answer("Введите аргумент или /next чтобы продолжить без ввода аргумента:")
    await message.answer("/close - для выхода из функции")
    await argState.arg.set()
@dp.message_handler(state=argState.arg)
async def process_phone(message: types.Message, state: FSMContext):
    arg_text = message.text
    logging.debug(f'get_apt_list поймал сообщение от пользователя:{arg_text}')
    if arg_text != '/close':
        logging.debug(f'get_apt_list - сообщение не является /close')
        if arg_text != '/next':
            logging.debug(f'get_apt_list - сообщение не является /next')
            logging.debug(f'get_apt_list - вызов функции get_apt_list_arg({arg_text})')
            responce = get_apt_list_arg(arg_text)
            logging.debug(f'get_apt_list - получил ответ')
            logging.debug(f'get_apt_list - начинает проверку длины ответа')
            if len(responce) > 4096:
                logging.debug(f'get_apt_list - длина ответа больше 4096')
                n = len(responce) // 4096
                logging.debug(f'get_apt_list - найдено целое число делений ответа = {n}')
                logging.debug(f'get_apt_list - запуск цикла отправки сообщений в интервале от 0 до {n}')
                for i in range(n):
                    await message.answer(responce[:4096])
                    logging.debug(f'get_apt_list {i}-е сообщение отправлено')
                    responce = responce[4096:]
                    logging.debug(f'get_apt_list - удалил первые 4096 символ из ответа от функции')
                    time.sleep(1)
                    logging.debug(f'get_apt_list - ушел в сон на 1 секунду')
                logging.debug(f'get_apt_list - заверил цикл, начинает проверку остатка ответа')
                if len(responce) > 0:
                    logging.debug(f'get_apt_list - остаток найден')
                    await message.answer(responce)
                    await state.finish()
                    logging.debug(f'get_apt_list - отправил последнее сообщение и завершил работу')
            else:
                logging.debug(f'get_apt_list - длина ответа меньше 4096')
                await message.answer(responce)
                await state.finish()
                logging.debug(f'get_apt_list - отправил отчет и завершил работу')
        else:
            logging.debug(f'get_apt_list - сообщение является /next')
            logging.debug(f'get_apt_list вызывает get_apt_list')
            responce = get_apt_list()
            logging.debug(f'get_apt_list - получил ответ')
            logging.debug(f'get_apt_list - начинает проверку длины ответа')
            if len(responce) > 4096:
                logging.debug(f'get_apt_list - длина ответа больше 4096')
                n = len(responce) // 4096
                logging.debug(f'get_apt_list - найдено целое число делений ответа = {n}')
                logging.debug(f'get_apt_list - запуск цикла отправки сообщений в интервале от 0 до {n}')
                for i in range(n):
                    await message.answer(responce[:4096])
                    logging.debug(f'get_apt_list {i}-е сообщение отправлено')
                    responce = responce[4096:]
                    logging.debug(f'get_apt_list - удалил первые 4096 символ из ответа от функции')
                    time.sleep(1)
                    logging.debug(f'get_apt_list - ушел в сон на 1 секунду')
                logging.debug(f'get_apt_list - заверил цикл, начинает проверку остатка ответа')
                if len(responce) > 0:
                    logging.debug(f'get_apt_list - остаток найден')
                    await message.answer(responce)
                    await state.finish()
                    logging.debug(f'get_apt_list - отправил последнее сообщение и завершил работу')
            else:
                logging.debug(f'get_apt_list - длина ответа меньше 4096')
                await message.answer(responce)
                await state.finish()
                logging.debug(f'get_apt_list - отправил отчет и завершил работу')
    else:
        logging.debug(f'get_apt_list - сообщение является /close')
        await message.answer('Вы вышли из функции...')
        await state.finish()
        logging.debug(f'get_apt_list - отправил отчет и завершил работу')

@dp.message_handler(commands=['get_repl_logs'])
async def get_repl_l(message: types.Message):
    logging.debug(f'Вызов get_repl_logs')
    logging.debug(f'get_mpstat вызывает get_repl_logs')
    responce = get_repl_logs()
    logging.debug(f'get_repl_logs - получил ответ')
    logging.debug(f'get_repl_logs - начинает проверку длины')
    if len(responce) > 4096:
        logging.debug(f'get_repl_logs - длина больше 4096')
        n = len(responce) // 4096
        logging.debug(f'get_repl_logs - найдено целое число делений ответа = {n}')
        logging.debug(f'get_repl_logs - запуск цикла отправки сообщений в интервале от 0 до {n}')
        for i in range(n):
            await message.answer(responce[:4096])
            logging.debug(f'get_repl_logs {i}-е сообщение отправлено')
            responce = responce[4096:]
            logging.debug(f'get_repl_logs - удалил первые 4096 символ из ответа от функции')
            time.sleep(1)
            logging.debug(f'get_repl_logs - ушел в сон на 1 секунду')
        logging.debug(f'get_repl_logs - заверил цикл, начинает проверку остатка ответа')
        if len(responce) > 0:
            logging.debug(f'get_repl_logs - остаток найден')
            await message.answer(responce)
            logging.debug(f'get_repl_logs - отправил последнее сообщение и завершил работу')
    else:
        logging.debug(f'get_repl_logs - длина ответа меньше 4096')
        await message.answer(responce)
        logging.debug(f'get_repl_logs - отправил отчет и завершил работу')

@dp.message_handler(commands=['get_phone_numbers'])
async def g_phone(message: types.Message):
    logging.debug(f'Вызов get_phone_numbers')
    logging.debug(f'get_phone_numbers вызывает get_phone_numbers')
    response = get_phone_number()
    logging.debug(f'get_phone_numbers - получил ответ')
    logging.debug(f'get_phone_numbers - начинает обработку ответа')
    answer = ''
    try:
        for i in response:
            i = str(i)
            i = re.sub(r'[\(\)\'\,]', '', i)
            answer += i + '\n'
    except Exception as ex:
        logging.error(f'Ошибка при обработке: {ex}')
        await message.answer('Ошибка')
        return 0
    logging.debug(f'get_phone_numbers - начинает отправку отчета')
    await message.answer(answer)
    logging.debug(f'get_phone_numbers - отправил отчет, завершил работу')

@dp.message_handler(commands=['get_emails'])
async def g_email(message: types.Message):
    logging.debug(f'Вызов get_emails')
    logging.debug(f'get_emails вызывает get_emails')
    response = get_emails()
    logging.debug(f'get_emails - получил ответ')
    logging.debug(f'get_emails - начинает обработку ответа')
    answer = ''
    try:
        for i in response:
            i = str(i)
            i = re.sub(r'[\(\)\'\,]', '', i)
            answer += i + '\n'
    except Exception as ex:
        logging.error(f'Ошибка при обработке: {ex}')
        await message.answer('Ошибка')
        return 0
    logging.debug(f'get_emails - начинает отправку отчета')
    await message.answer(answer)
    logging.debug(f'get_emails - отправил отчет, завершил работу')






#---------------------------------------START---------------------------------------
if __name__ == "__main__":
    executor.start_polling(dp)
    print('Системы стартовали')
    logging.debug('Начало программы')
    a = sozd_table()
