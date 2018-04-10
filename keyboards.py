
import telebot

##############################  INLINE KEYBOARDS ################################################
def startboard():
    keyboard = telebot.types.InlineKeyboardMarkup()
    callback_button1 = telebot.types.InlineKeyboardButton(text='AUTH', callback_data='auth')
    callback_button2 = telebot.types.InlineKeyboardButton(text='How are you?', callback_data='how are you')
    keyboard.add(callback_button1,callback_button2)
    return keyboard






##############################  REPLY KEYBOARDS ################################################


