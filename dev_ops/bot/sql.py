import logging
import psycopg2
from psycopg2 import Error

user="postgres"
password="Qq12345"
host="db_image"
port="5432"
database="base_1"

logging.basicConfig(filename='app.txt',level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')

def sozd_table():
    connection = None
    try:
        connection = psycopg2.connect(user=user, password=password, host=host, port=port, database=database)
        cursor = connection.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS email(ID SERIAL PRIMARY KEY, email VARCHAR(100) NOT NULL;")
        data = cursor.fetchall()
        cursor.execute("CREATE TABLE IF NOT EXISTS phone(ID SERIAL PRIMARY KEY, phone VARCHAR(20));")
        data = cursor.fetchall()
    except (Exception, Error) as error:
        logging.error("Ошибка при работе с PostgreSQL: %s", error)
        data = 'Ошибка'
    finally:
        if connection is not None:
            cursor.close()
            connection.close()
        return data
def get_emails():
    connection = None
    try:
        connection = psycopg2.connect(user=user, password=password, host=host, port=port, database=database)
        cursor = connection.cursor()
        cursor.execute("SELECT email FROM email;")
        data = cursor.fetchall()
    except (Exception, Error) as error:
        logging.error("Ошибка при работе с PostgreSQL: %s", error)
        data = 'Ошибка'
    finally:
        if connection is not None:
            cursor.close()
            connection.close()
        return data

def get_phone_number():
    connection = None
    try:
        connection = psycopg2.connect(user=user, password=password, host=host, port=port, database=database)
        cursor = connection.cursor()
        cursor.execute("SELECT phone FROM phone;")
        data = cursor.fetchall()
    except (Exception, Error) as error:
        logging.error("Ошибка при работе с PostgreSQL: %s", error)
        data = error
    finally:
        if connection is not None:
            cursor.close()
            connection.close()
        return data

def email_insert(arg):
    connection = None
    try:
        connection = psycopg2.connect(user=user, password=password, host=host, port=port, database=database)
        cursor = connection.cursor()
        cursor.execute(f"insert into users_email (email) values ('{arg}');")
        data = cursor.fetchall()
        data = 'Успех'
    except (Exception, Error) as error:
        logging.error("Ошибка при работе с PostgreSQL: %s", error)
        data = 'Ошибка'
    finally:
        if connection is not None:
            cursor.close()
            connection.close()
        return data

def phone_insert(arg):
    connection = None
    try:
        connection = psycopg2.connect(user=user, password=password, host=host, port=port, database=database)
        cursor = connection.cursor()
        cursor.execute(f"insert into users_phone (phone_number) values ('{arg}');")
        data = cursor.fetchall()
        data = 'Успех'
    except (Exception, Error) as error:
        logging.error("Ошибка при работе с PostgreSQL: %s", error)
        data = 'Ошибка'
    finally:
        if connection is not None:
            cursor.close()
            connection.close()
        return data
