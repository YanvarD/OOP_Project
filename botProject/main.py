import telebot
from extention import ConvertCurrency, APIexception

from config import keys, TOKEN


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start(message: telebot.types.Message):
    text = "Здравствуйте,\nчто бы конвертировать валюту введите команду следующего типа\"" \
           "<имя валюты, цену которой хотите узнать>\n" \
           "<имя валюты, в которой надо узнать цену первой валюты>\n" \
           "<количество первой валюты>\n" \
           "Введите /value что бы узнать доступные валюты"
    bot.reply_to(message, text)


@bot.message_handler(commands=["value"])
def value(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        value = message.text.split(' ')

        qoute, base, amount = value

        data = ConvertCurrency.convert(qoute,base,amount)
        if len(value) != 3:
            raise APIexception('Не верно составлен запрос,\nповторите попытку, должно быть 3 параметра')
    except APIexception as err:
        bot.reply_to(message, f'Ошибка пользователя {err}')
    except Exception as err:
        bot.reply_to(message, f'Не удалось обработать команду {err}')
    else:
        text = f'Цена {amount} {qoute} в {base} = {data}'
        bot.send_message(message.chat.id, text)






bot.polling(none_stop=True)
