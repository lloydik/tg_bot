import logging
import psycopg2
from psycopg2 import Error
from pathlib import Path
import os
from dotenv import load_dotenv

logging.basicConfig(
    filename='db.log', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG, encoding="utf-8"
)
logger = logging.getLogger(__name__)

class DBOperator:
    def __init__(self):
        
        # dotenv_path = Path('.env')
        # load_dotenv(dotenv_path=dotenv_path)

        self.host = os.getenv('DB_HOST')
        self.port = os.getenv('DB_PORT')
        self.username = os.getenv('DB_USER')
        self.password = os.getenv('DB_PASSWORD')
        self.database = os.getenv('DB_DATABASE')
    
    def fetch(self, cmd):
        connection = None
        try:
            connection = psycopg2.connect(user=self.username,
                                        password=self.password,
                                        host=self.host,
                                        port=self.port, 
                                        database=self.database)

            cursor = connection.cursor()
            cursor.execute(cmd)
            data = cursor.fetchall()
            logging.info(data)
            logging.info("Команда успешно выполнена")
            if not data:
                return "Нет данных"
            return data
             
        except (Exception, Error) as error:
            logging.error("Ошибка при работе с PostgreSQL: %s", error)
        finally:
            if connection is not None:
                cursor.close()
                connection.close()
                logging.info("Соединение с PostgreSQL закрыто")
    
    def execute(self, cmd):
        connection = None
        try:
            connection = psycopg2.connect(user=self.username,
                                        password=self.password,
                                        host=self.host,
                                        port=self.port, 
                                        database=self.database)

            cursor = connection.cursor()
            cursor.execute(cmd)
            connection.commit()
            logging.info("Команда успешно выполнена")
        except (Exception, Error) as error:
            logging.error("Ошибка при работе с PostgreSQL: %s", error)
        finally:
            if connection is not None:
                cursor.close()
                connection.close()
                logging.info("Соединение с PostgreSQL закрыто")

    def get_emails(self):
        fetched = self.fetch('SELECT email FROM emails;')
        res = ''
        for i in range(len(fetched)):
            res += f'{i+1}. {fetched[i][0]}\n'
        return res
    
    def get_phones(self):
        fetched = self.fetch('SELECT phone FROM phones;')
        res = ''
        for i in range(len(fetched)):
            res += f'{i+1}. {fetched[i][0]}\n'
        return res
        
    def insert_phone(self, phone):
        return self.execute(f"INSERT INTO phones (phone) VALUES ('{phone}');")
        
    def insert_email(self, email):
        return self.execute(f"INSERT INTO emails (email) VALUES ('{email}');")