import logging
import re
from monitoring import MonitorBot
from db import DBOperator

from pathlib import Path
import os
from dotenv import load_dotenv
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler



dotenv_path = Path('.env')
load_dotenv(dotenv_path=dotenv_path)

TOKEN = os.getenv('TOKEN')
# chat id 493569077
# Подключаем логирование
logging.basicConfig(
    filename='logfile.txt', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def start(update: Update, context):
    user = update.effective_user
    update.message.reply_text(f'Привет {user.full_name}!')


def helpCommand(update: Update, context):
    update.message.reply_text('Help!')


def findPhoneNumbersCommand(update: Update, context):
    update.message.reply_text('Введите текст для поиска телефонных номеров: ')
    return 'findPhoneNumbers'


phones = []
def findPhoneNumbers (update: Update, context):
    global phones
    phones = []
    user_input = update.message.text # Получаем текст, содержащий(или нет) номера телефонов
    logging.debug(user_input)
    phoneNumRegex = re.compile(r'((8|\+7)\s?(\(\d{3}\)|\d{3})[-\s]?\d{3}[-\s]?\d{2}[-\s]?\d{2})') # формат номера телефона

    phoneNumberList = phoneNumRegex.findall(user_input) # Ищем номера телефонов
    logging.debug(phoneNumberList)
    
    if not phoneNumberList: # Обрабатываем случай, когда номеров телефонов нет
        update.message.reply_text('Телефонные номера не найдены')
        return # Завершаем выполнение функции
        
    phoneNumbers = '' # Создаем строку, в которую будем записывать номера телефонов
    for i in range(len(phoneNumberList)):
        phoneNumbers += f'{i+1}. {phoneNumberList[i][0]}\n' # Записываем очередной номер
        phones.append(phoneNumberList[i][0])
        
    update.message.reply_text(phoneNumbers+'\nОтправьте "Да" (без кавычек) для того, чтобы записать телефоны в БД') # Отправляем сообщение пользователю
    return "insertPhones"

def insertPhones(update: Update, context):
    logging.debug(phones)
    if update.message.text.lower() == 'да':
        db_bot = DBOperator()
        for p in phones:
            db_bot.insert_phone(p)
        update.message.reply_text('Телефоны записаны!') # Отправляем сообщение пользователю
    else:
        update.message.reply_text('Телефоны записывать в БД не стал') # Отправляем сообщение пользователю
    logging.debug(context)
    return ConversationHandler.END


def findEmailsCommand(update: Update, context):
    update.message.reply_text('Введите текст для поиска email\'ов: ')
    return 'findEmails'

emails_array = []
def findEmails(update: Update, context):
    global emails_array
    emails_array = []
    user_input = update.message.text # Получаем текст, содержащий(или нет) email
    logging.debug(user_input)
    emailNumRegex = re.compile(r'[\w.%+-]+@[a-zA-Z\d.-]+\.[a-zA-Z]{2,}') # формат email
    emailList = emailNumRegex.findall(user_input) # Ищем email
    logging.debug(emailList)

    if not emailList: # Обрабатываем случай, когда email нет
        update.message.reply_text('Email не найдены')
        return # Завершаем выполнение функции

    emails = '' # Создаем строку, в которую будем записывать email
    for i in range(len(emailList)):
        emails += f'{i+1}. {emailList[i]}\n' # Записываем очередной email
        emails_array.append(emailList[i])
    update.message.reply_text(emails+'\nОтправьте "Да" (без кавычек) для того, чтобы записать email\'ы в БД') # Отправляем сообщение пользователю
    return "insertEmails"
    # return ConversationHandler.END # Завершаем работу обработчика диалога

def insertEmail(update: Update, context):
    logging.debug(emails_array)
    if update.message.text.lower() == 'да':
        db_bot = DBOperator()
        for e in emails_array:
            db_bot.insert_email(e)
        update.message.reply_text('Email\'ы записаны!') # Отправляем сообщение пользователю
    else:
        update.message.reply_text('Email\'ы записывать в БД не стал') # Отправляем сообщение пользователю
    logging.debug(context)
    return ConversationHandler.END


def verifyPassCommand(update: Update, context):
    update.message.reply_text('Введите пароль для проверки: ')
    return 'verifyPassword'

def verify_password(update: Update, context):
    user_pass = update.message.text # Получаем пароль
    logging.debug(user_pass)
    passRegex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()])[A-Za-z\d!@#$%^&*()]{8,}$')
    logging.debug(passRegex.fullmatch(user_pass))

    if passRegex.fullmatch(user_pass):
        update.message.reply_text('Пароль сложный')
    else:
        update.message.reply_text('Пароль простой')
    return ConversationHandler.END # Завершаем работу обработчика диалога

def echo(update: Update, context):
    update.message.reply_text(update.message.text)


def main():
    updater = Updater(TOKEN, use_context=True)

    # Получаем диспетчер для регистрации обработчиков
    dp = updater.dispatcher

    # Обработчик диалога поиска номеров
    convHandlerFindPhoneNumbers = ConversationHandler(
        entry_points=[CommandHandler('find_phone_number', findPhoneNumbersCommand)],
        states={
            'findPhoneNumbers': [MessageHandler(Filters.text & ~Filters.command, findPhoneNumbers)],
            'insertPhones': [MessageHandler(Filters.text & ~Filters.command, insertPhones)],
        },
        fallbacks=[]
    )

    # Обработчик диалога поиска email
    convHandlerFindEmails = ConversationHandler(
        entry_points=[CommandHandler('find_emails', findEmailsCommand)],
        states={
            'findEmails': [MessageHandler(Filters.text & ~Filters.command, findEmails)],
            'insertEmails': [MessageHandler(Filters.text & ~Filters.command, insertEmail)],
        },
        fallbacks=[]
    )

    # Обработчик диалога проверки пароля
    convHandlerVerifyPass = ConversationHandler(
        entry_points=[CommandHandler('verify_password', verifyPassCommand)],
        states={
            'verifyPassword': [MessageHandler(Filters.text & ~Filters.command, verify_password)],
        },
        fallbacks=[]
    )
		
	# Регистрируем обработчики команд
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", helpCommand))
    monitoring = MonitorBot()
    db_bot = DBOperator()
    bot_adapter = lambda func: (lambda update, context: update.message.reply_text(func()))
    dp.add_handler(CommandHandler("get_release", bot_adapter(monitoring.get_release)))
    dp.add_handler(CommandHandler("get_uname", bot_adapter(monitoring.get_uname)))
    dp.add_handler(CommandHandler("get_uptime", bot_adapter(monitoring.get_uptime)))
    dp.add_handler(CommandHandler("get_df", bot_adapter(monitoring.get_df)))
    dp.add_handler(CommandHandler("get_free", bot_adapter(monitoring.get_free)))
    dp.add_handler(CommandHandler("get_mpstat", bot_adapter(monitoring.get_mpstat)))
    dp.add_handler(CommandHandler("get_w", bot_adapter(monitoring.get_w)))
    dp.add_handler(CommandHandler("get_auths", bot_adapter(monitoring.get_auths)))
    dp.add_handler(CommandHandler("get_critical", bot_adapter(monitoring.get_critical)))
    dp.add_handler(CommandHandler("get_ps", bot_adapter(monitoring.get_ps)))
    dp.add_handler(CommandHandler("get_ss", bot_adapter(monitoring.get_ss)))
    dp.add_handler(CommandHandler("get_apt_list", lambda update, context: (
        update.message.reply_text(monitoring.get_apt_list()) if not context.args else update.message.reply_text(monitoring.get_apt_list(context.args[0]))
        )))
    dp.add_handler(CommandHandler("get_services", bot_adapter(monitoring.get_services)))
    dp.add_handler(CommandHandler("get_repl_logs", bot_adapter(monitoring.get_repl_logs)))
    dp.add_handler(CommandHandler("get_emails", bot_adapter(db_bot.get_emails)))
    dp.add_handler(CommandHandler("get_phone_numbers", bot_adapter(db_bot.get_phones)))

    dp.add_handler(convHandlerFindPhoneNumbers)
    dp.add_handler(convHandlerFindEmails)
    dp.add_handler(convHandlerVerifyPass)
	
	# Регистрируем обработчик текстовых сообщений
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
		
	# Запускаем бота
    updater.start_polling()

	# Останавливаем бота при нажатии Ctrl+C
    updater.idle()


if __name__ == '__main__':
    main()
