import telebot
import json
import random

TOKEN = "7468325259:AAEva4NAI-PI7e33S_tqWjN0x7JaRNilGDQ"

bot = telebot.TeleBot(TOKEN)
try:
    with open("user_data.json","r",encoding="utf-8") as file:
        user_data = json.load(file)
except FileNotFoundError:
    user_data = {}




@bot.message_handler(commands=["start"])
def handle_start(message):
    bot.send_message(message.chat.id,"Привет! Это бот для изучения английского языка! Для справки команда /help")

@bot.message_handler(commands=["learn"])
def handle_learn(message):
    try:
        user_words = user_data.get(str(message.chat.id), {})
    except:
        print("слов нет и их нужно добавить")
        return False

    try:
        words_number = int(message.text.split()[1])
        ask_translation(message.chat.id, user_words, words_number)
    except ValueError :
        print("Функция получает аргумент правильного типа, но с недопустимым значением.")
    except IndexError:
        print("происходит попытка обращения к элементу последовательности (например, строке, списку или кортежу) по индексу, который находится вне допустимого диапазона индексов этой последовательности. (Например, в списке пять элементов, а пытаются обратиться к шестому).")

def ask_translation(chat_id, user_words, words_left):
    if words_left > 0:
        word = random.choice(list(user_words.keys()))
        translation = user_words[word]
        bot.send_message(chat_id,f"Напиши перевод слова '{word}'.")
        bot.register_next_step_handler_by_chat_id(chat_id,check_translation,translation,words_left)
    else:
        bot.send_message(chat_id,"Урок закончен!")



def check_translation(message,expected_translation,words_left):
    user_translation = message.text.strip().lower()
    if user_translation == expected_translation.lower():
        bot.send_message(message.chat.id,"Правильно! Молодец!")

    else:
        bot.send_message(message.chat.id,f"Неправильно, правильный перевод: {expected_translation}")
    ask_translation(message.chat.id, user_data[str(message.chat.id)],words_left)




@bot.message_handler(commands=["addword"])
def handle_addword(message):
    global user_data
    chat_id  = message.chat.id
    user_dict = user_data.get(chat_id,{})

    words = message.text.split()[1:]
    if len(words) == 2:
        word, translation = words[0].lower(),words[1].lower()
        user_dict[word] = translation
        user_data[chat_id] = user_dict
        with open("user_data.json", "w", encoding="utf-8") as file:
            json.dump(user_data,file,ensure_ascii=False, indent=4)
        bot.send_message(chat_id,"Слово добавлено!")
    else:
        bot.send_message(chat_id,"Произошла ошибка! Попробуйте ещё раз!")







@bot.message_handler(commands=["help"])
def handle_start(message):
    bot.send_message(message.chat.id,"1) Данный бот предназначен для обучения английскому языку!"
                                     "2) В боте присутствуют такие команды, как: /learn(кол-во слов для изучения, но без скобок)) /help /addword."
                                     "3) Автор бота: Захаров Савелий"
                     )


@bot.message_handler(func=lambda message:True)
def handle_all(message):
    if message.text.lower() == "как тебя зовут?":
        bot.send_message(message.chat.id, "Меня зовут Digital Dave ")
    elif message.text.lower() == "расскажи о себе":
        bot.send_message(message.chat.id, "Я бот для изучения английского языка")
    elif message.text.lower() == "как дела?":
        bot.send_message(message.chat.id, "Отлично! Я рад что могу чем-то помочь тебе!")


if __name__== "__main__":
    bot.polling(non_stop=True)