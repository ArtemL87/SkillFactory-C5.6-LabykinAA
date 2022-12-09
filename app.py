import telebot
from extensions import APIException, CryptoConverter
from config import TOKEN, keys

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def start(message: telebot.types.Message):
    text = 'ЭТОТ БОТ КОНВЕРТИРУЕТ ВАЛЮТУ' \
           '\nЧтобы начать работу введите команду боту в следующем формате:\n<имя валюты, цену которой он хочет узнать> ' \
           '<имя валюты, в которой надо узнать цену первой валюты> ' \
           '<количество первой валюты>' \
           '\nУвидеть список валют можно по команде: /values'
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['values'])
def values(messange: telebot.types.Message):
    text = 'Доступные валюты: '
    for i in keys.keys():
        text = '\n'.join((text, i, ))
    bot.send_message(messange.chat.id, text)

@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        if len(values) > 3:
            raise APIException('Слишком много параметров. \nДля помощи нажмите на ссылку: /help'
                               '\nУвидеть список валют можно по команде: /values')
        if len(values) < 3:
            raise APIException('Слишком мало параметров\nДля помощи нажмите на ссылку: /help'
                               '\nУвидеть список валют можно по команде: /values')
        quote, base, amount = values
        total_base = CryptoConverter.get_price(quote.lower(), base.lower(), amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя. \n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n {e}')
    else:
        text = f'Цена {amount} {quote.lower()} в {base.lower()} - {int(amount) * total_base}'
        bot.send_message(message.chat.id, text)



bot.polling(non_stop=True)

