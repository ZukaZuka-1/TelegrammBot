import telebot
from config import TOKEN, keys
from extrention import APIException, ValuesConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message: telebot.types.Message):
    bot.reply_to(message, f"Приветствую, {message.chat.username}.\nМеня зовут Семён, я бот конвертирующий одну валюту в другую.")


@bot.message_handler(commands=['help'])
def send_rules(message: telebot.types.Message):
    bot.reply_to(message, f"Чтобы я начал работать пожалуйста введите:\n<имя валюты, цену которой он хочет узнать>\n<имя валюты, в которой надо узнать цену первой валюты>\n<количество первой валюты>\nДля того чтобы увидеть список доступной валюты, введите команду /values")


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступная валюта:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException('Ознакомьтесь с правилами.')

        quote, base, amount = values
        total_base = ValuesConverter.convert(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Неверный ввод\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработаь команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)



bot.polling(none_stop=True)


