import telebot
import logging
import config
import DBworker
import helpdeskAPI
import keyboards

bot = telebot.TeleBot(config.bot_token)

#######################################logging###################################
logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)

handler = logging.FileHandler(filename='loggingbot.log', encoding='utf-8')
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s '
                              '(%(filename)s : %(lineno)s',
                              datefmt='(%y-%m-%d %H:%M:%S)')

handler.setFormatter(formatter)
logger.addHandler(handler)
#################################################################################


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    callback_button1 = telebot.types.InlineKeyboardButton(text='AUTH', callback_data='auth')
    callback_button2 = telebot.types.InlineKeyboardButton(text='How are you?', callback_data='how are you')
    keyboard.add(callback_button1,callback_button2)
    bot.send_message(message.chat.id,
                  'Привет!\n'
                  'Я ABM inventory bot\n'
                  'Пока что доступна только верификация по email', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    # Если сообщение из чата с ботом
    if call.message:
        if call.data == 'EDIT':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='Введите код товара',reply_markup='some keyboard')

        elif call.data == 'auth':
            bot.send_message(chat_id=call.message.chat.id,
                             text='Введите свой e-mail...')
            DBworker.set_state(call.message.chat.id, config.States.S_ENTER_MAIL.value)

        elif call.data == 'how are you':
            bot.send_message(chat_id=call.message.chat.id,
                             text='I`m fine, thank`s!\n'
                                    'And you?')
            DBworker.set_state(call.message.chat.id, config.States.S_HOW_ARE_YOU.value)

@bot.message_handler(func=lambda message: DBworker.get_current_state(message.chat.id) == config.States.S_ENTER_MAIL.value)
def ifmail(message):

    if not message.entities == None: # 'entities' - изменяется если ввели не просто текст  (сужаем круг проверки)
        bot.send_message(message.chat.id, "Спасибо, проверяю")

        if helpdeskAPI.get_all_mails(message.text) == False:
            bot.send_message(message.chat.id, "Почта\n%s\nПодтверждена, Теперь расшарь мне свой номер телефона)" % message.text)
            DBworker.set_state(message.chat.id, config.States.S_MAIL_AUTH_TRUE.value)

        else:
            bot.send_message(message.chat.id, "Пользователь с такой почтой отсутствует в системе!\n"
                                              "Проверь почту и попробуй еще раз😋")

            DBworker.set_state(message.chat.id, config.States.S_ENTER_MAIL.value)

    else:
        bot.send_message(message.chat.id,"Мне кажется, что это не адрес электронной почты, внимательнее будь)\n"
                                         "Попробуй еще разок)")

@bot.message_handler(func=lambda message: DBworker.get_current_state(message.chat.id) == config.States.S_START.value)
def send_welcome(message):
    bot.send_message(message.chat.id,
                  'Привет!\n'
                  'Я ABM inventory bot\n'
                  'Пока что доступна только верификация по email', reply_markup=keyboards.startboard())

@bot.message_handler(func=lambda message: DBworker.get_current_state(message.chat.id) == config.States.S_MAIL_AUTH_TRUE.value)
def mail_auth_true(message):
    bot.send_message(message.chat.id, "Круто, теперь расшарь мне свой номер тел)")

@bot.message_handler(func=lambda message: DBworker.get_current_state(message.chat.id) == config.States.S_HOW_ARE_YOU.value)
def dialog(message):
    bot.send_message(message.chat.id, "Прости, я бы с радостью поговорил с тобой, но у меня срочные дела...\n"
                                      "До скорого!\n"
                                      "Если что-то нужно - дай мне знать)",reply_markup=keyboards.startboard())

if __name__ == '__main__':
    bot.polling(none_stop=True, interval=1)

