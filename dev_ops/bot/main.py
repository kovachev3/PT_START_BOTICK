import logging
import re
import psycopg2

import os

from psycopg2 import Error

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from dotenv import load_dotenv
import paramiko

load_dotenv()

client = paramiko.SSHClient()
def connect_to_machine(thishost):
    global client
    host = os.getenv('RM_HOST')
    port = os.getenv('RM_PORT')
    username = os.getenv('RM_USER')
    password = os.getenv('RM_PASSWORD')
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username, password=password, port=port)

TOKEN = os.getenv('TOKEN')

# Подключаем логирование
logging.basicConfig(
    filename='logfile.txt', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

def start(update: Update, context):
    user = update.effective_user
    update.message.reply_text(f'Привет, {user.full_name}!')

def findEmailCommand(update: Update, context):
    update.message.reply_text('Введите текст для поиска email: ')
    return 'find_email'

def findPhoneNumberCommand(update: Update, context):
    update.message.reply_text('Введите текст для поиска телефонных номеров: ')
    return 'find_phone_number'

def verifyPasswordCommand(update: Update, context):
    update.message.reply_text('Введите пароль: ')
    return 'verify_password'

def aptListCommand(update: Update, context):
    update.message.reply_text('Напишите all ,чтобы посмотреть все пакеты')
    return 'get_apt_list'

def find_email(update: Update, context):
    user_input = update.message.text
    emailNumRegex = re.compile(r"\b[a-zA-Z0-9]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}\b")
    emailNumSet = set(emailNumRegex.findall(user_input))
    context.user_data['email'] = list(emailNumSet)
    if not emailNumSet:
        update.message.reply_text('Email не были найдены')
        return
    emailNum = ''
    for i, email in enumerate(emailNumSet):
        emailNum += f'{i+1}. {email}\n'
    update.message.reply_text('Были найдены следующие email: '\
                              +'\n'+emailNum+'\n'\
                                +'Записать их в базу данных? (Y\\N)') 
    return 'SAVE EMAIL'

def save_email(update: Update, context):
    connection = psycopg2.connect(user=os.getenv('DB_USER'), password=os.getenv('DB_PASSWORD'), host=os.getenv('DB_HOST'), port=os.getenv('DB_PORT'), database=os.getenv('DB_DATABASE'))
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS email(ID SERIAL PRIMARY KEY, email VARCHAR(100) NOT NULL);")
    connection.commit()
    email_list = context.user_data['email']
    if update.message.text in ['Y', 'N']:
        if update.message.text == 'Y':
            try:
                for email in email_list:
                    cursor.execute("SELECT 1 FROM email WHERE email = %s", (email,))
                    if cursor.fetchone():
                        update.message.reply_text(f"Email {email} уже существует в базе данных.")
                        break
                else:
                    for email in email_list:
                        cursor.execute("INSERT INTO email(email) VALUES (%s)", (email,))
                    connection.commit()
                    update.message.reply_text("Успешно добавлен в бд!")
            except (Exception, Error) as error:
                update.message.reply_text("Ошибка в бд")
            finally:
                connection.close()
        else:
            connection.close()
            return ConversationHandler.END
    else:
        update.message.reply_text("OS")
        connection.close()
        return ConversationHandler.END
    return ConversationHandler.END
    
def find_phone_number(update: Update, context):
    user_input = update.message.text 
    phoneNumRegex = re.compile(r"\+?7[ -]?\(?\d{3}\)?[ -]?\d{3}[ -]?\d{2}[ -]?\d{2}|\+?7[ -]?\d{10}|\+?7[ -]?\d{3}[ -]?\d{3}[ -]?\d{4}|8[ -]?\(?\d{3}\)?[ -]?\d{3}[ -]?\d{2}[ -]?\d{2}|8[ -]?\d{10}|8[ -]?\d{3}[ -]?\d{3}[ -]?\d{4}") 
    phoneNumberList = phoneNumRegex.findall(user_input) 
    context.user_data['phone_numbers'] = phoneNumberList
    if not phoneNumberList:
        update.message.reply_text('Телефонные номера не найдены')
        return 
    phoneNumbers = ''
    for i in range(len(phoneNumberList)):
        phoneNumbers += f'{i+1}. {phoneNumberList[i]}\n' 
    update.message.reply_text('Были найдены следующие номера: '\
                              +'\n'+phoneNumbers+'\n'\
                                +'Записать их в базу данных? (Y\\N)') 
    return 'SAVE PHONE NUMBERS'
    
def save_phone_numbers(update: Update, context):
    connection = psycopg2.connect(user=os.getenv('DB_USER'), password=os.getenv('DB_PASSWORD'), host=os.getenv('DB_HOST'), port=os.getenv('DB_PORT'), database=os.getenv('DB_DATABASE'))
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS phone(ID SERIAL PRIMARY KEY, phone VARCHAR(20));")
    connection.commit()
    phoneNumberList = context.user_data['phone_numbers']
    
    if update.message.text == 'Y':
        try:
            for phone_number in phoneNumberList:
                cursor.execute("SELECT * FROM phone WHERE phone = %s", (phone_number,))
                if cursor.fetchone():
                    update.message.reply_text(f"Номер телефона {phone_number} уже существует в базе данных.")
                else:
                    cursor.execute("INSERT INTO phone(phone) VALUES (%s);", (phone_number,))
            connection.commit()
            update.message.reply_text("Все номера успешно добавлены в базу данных!")
        except (Exception, Error) as error:
            update.message.reply_text("Ошибка в бд")
            return ConversationHandler.END
    else:
        update.message.reply_text("Операция отменена. Номера не добавлены в базу данных.")

    connection.close()
    return ConversationHandler.END

def verify_password(update: Update, context):
    user_input=update.message.text
    if (
        len(str(user_input))>=8 and
        re.search(r'[A-Z]', user_input)
        and re.search(r'[a-z]', user_input)
        and re.search(r'\d', user_input)
        and re.search(r'[!@#$%^&*()]', user_input)):
        update.message.reply_text('Пароль сложный')
    else:
        update.message.reply_text('Пароль простой')
        return
    return ConversationHandler.END 

def print_info(stdout, stderr):
    data = stdout.read() + stderr.read()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    return(data)

def get_release(update: Update, context):
    global client
    connect_to_machine(os.getenv('RM_HOST'))
    stdin, stdout, stderr = client.exec_command('cat /etc/os-release')
    update.message.reply_text(print_info(stdout,stderr))

def get_uname(update: Update, context):
    global client
    connect_to_machine(os.getenv('RM_HOST'))
    stdin, stdout, stderr = client.exec_command('uname -a')
    update.message.reply_text(print_info(stdout,stderr))

def get_uptime(update: Update, context):
    global client
    connect_to_machine(os.getenv('RM_HOST'))
    stdin, stdout, stderr = client.exec_command('uptime')
    update.message.reply_text(print_info(stdout,stderr))

def get_df(update: Update, context):
    global client
    connect_to_machine(os.getenv('RM_HOST'))
    stdin, stdout, stderr = client.exec_command('df')
    update.message.reply_text(print_info(stdout,stderr))

def get_free(update: Update, context):
    global client
    connect_to_machine(os.getenv('RM_HOST'))
    stdin, stdout, stderr = client.exec_command('free')
    update.message.reply_text(print_info(stdout,stderr))

def get_mpstat(update: Update, context):
    global client
    connect_to_machine(os.getenv('RM_HOST'))
    stdin, stdout, stderr = client.exec_command('mpstat')
    update.message.reply_text(print_info(stdout,stderr))

def get_w(update: Update, context):
    global client
    connect_to_machine(os.getenv('RM_HOST'))
    stdin, stdout, stderr = client.exec_command('w')
    update.message.reply_text(print_info(stdout,stderr))

def get_auth(update: Update, context):
    global client
    connect_to_machine(os.getenv('RM_HOST'))
    stdin, stdout, stderr = client.exec_command('cat /var/log/auth.log | head -10')
    update.message.reply_text(print_info(stdout,stderr))

def get_critical(update: Update, context):
    global client
    connect_to_machine(os.getenv('RM_HOST'))
    stdin, stdout, stderr = client.exec_command('cat /var/log/syslog | head -5')
    update.message.reply_text(print_info(stdout,stderr))

def get_ps(update: Update, context):
    global client
    connect_to_machine(os.getenv('RM_HOST'))
    stdin, stdout, stderr = client.exec_command('ps')
    update.message.reply_text(print_info(stdout,stderr))

def get_ss(update: Update, context):
    global client
    connect_to_machine(os.getenv('RM_HOST'))
    stdin, stdout, stderr = client.exec_command('ss -tulpn')
    update.message.reply_text(print_info(stdout,stderr))



def get_apt_list(update: Update, context):
    global client
    connect_to_machine(os.getenv('RM_HOST'))
    user_input=str(update.message.text)
    if user_input=='all':
        stdin, stdout, stderr = client.exec_command('apt list --installed | head -15')
        update.message.reply_text(print_info(stdout,stderr))
    return ConversationHandler.END 

def get_services(update: Update, context):
    global client
    connect_to_machine(os.getenv('RM_HOST'))
    stdin, stdout, stderr = client.exec_command('service --status-all | grep [+]')
    update.message.reply_text(print_info(stdout,stderr))

def get_repl_logs(update: Update, context):
    connect_to_machine(os.getenv('RM_HOST'))
    stdin, stdout, stderr = client.exec_command("docker logs bot_image_repl | grep -E 'checkpoint|replica'")
    update.message.reply_text(print_info(stdout,stderr))

def get_emails(update: Update, context):
    connection = psycopg2.connect(user=os.getenv('DB_USER'), password=os.getenv('DB_PASSWORD'), host=os.getenv('DB_HOST'), port=os.getenv('DB_PORT'), database=os.getenv('DB_DATABASE'))
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM email;")
    data = cursor.fetchall()
    output=''
    for x in data:
        output+=str(x[0])+'. '+x[1]+'\n'
    update.message.reply_text(output)
    connection.close()

def get_phone_numbers(update: Update, context):
    connection = psycopg2.connect(user=os.getenv('DB_USER'), password=os.getenv('DB_PASSWORD'), host=os.getenv('DB_HOST'), port=os.getenv('DB_PORT'), database=os.getenv('DB_DATABASE'))
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM phone;")
    data = cursor.fetchall()
    output=''
    for x in data:
        output+=str(x[0])+'. '+str(x[1])+'\n'
    update.message.reply_text(output)
    connection.close()

def main():
    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher

    convHandlerFindEmail = ConversationHandler(
        entry_points=[CommandHandler('find_email',findEmailCommand)],
        states={
            'find_email':[MessageHandler(Filters.text & ~Filters.command, find_email)],
            'SAVE EMAIL': [MessageHandler(Filters.text & ~Filters.command, save_email)],
        },
        fallbacks=[]
    )

    convHandlerFindPhoneNumber = ConversationHandler(
        entry_points=[CommandHandler('find_phone_number', findPhoneNumberCommand)],
        states={
            'find_phone_number': [MessageHandler(Filters.text & ~Filters.command, find_phone_number)],
            'SAVE PHONE NUMBERS': [MessageHandler(Filters.text & ~Filters.command, save_phone_numbers)],
        },
        fallbacks=[]
    )
    
    convHandlerverifyPassword = ConversationHandler(
        entry_points=[CommandHandler('verify_password',verifyPasswordCommand)],
        states={
            'verify_password':[MessageHandler(Filters.text & ~Filters.command, verify_password)],
        },
        fallbacks=[]
    )


    convHandleraptList = ConversationHandler(
        entry_points=[CommandHandler('get_apt_list',aptListCommand)],
        states={
            'get_apt_list':[MessageHandler(Filters.text & ~Filters.command, get_apt_list)],
        },
        fallbacks=[]
    )
  # Регистрируем обработчики команд
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(convHandlerFindEmail)
    dp.add_handler(convHandlerFindPhoneNumber)
    dp.add_handler(convHandlerverifyPassword)
    dp.add_handler(convHandleraptList)

    dp.add_handler(CommandHandler('get_release', get_release))
    dp.add_handler(CommandHandler('get_uname', get_uname))
    dp.add_handler(CommandHandler('get_uptime', get_uptime))
    dp.add_handler(CommandHandler('get_df', get_df))
    dp.add_handler(CommandHandler('get_free', get_free))
    dp.add_handler(CommandHandler('get_mpstat', get_mpstat))
    dp.add_handler(CommandHandler('get_w', get_w))
    dp.add_handler(CommandHandler('get_auth', get_auth))
    dp.add_handler(CommandHandler('get_critical', get_critical))
    dp.add_handler(CommandHandler('get_ps', get_ps))
    dp.add_handler(CommandHandler('get_ss', get_ss))
    dp.add_handler(CommandHandler('get_services', get_services))

    dp.add_handler(CommandHandler('get_repl_logs',get_repl_logs))  
    dp.add_handler(CommandHandler('get_emails',get_emails))
    dp.add_handler(CommandHandler('get_phone_numbers',get_phone_numbers))



    updater.start_polling()

  # Останавливаем бота при нажатии Ctrl+C
    updater.idle()


if __name__ == '__main__':
    main()
