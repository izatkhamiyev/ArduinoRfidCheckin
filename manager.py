import telebot
import time
from firebase import firebase
bot = telebot.TeleBot("1022367256:AAHIWDzFQIXc6VlEf_jbwrkoRb85rDIqbkU")
firebase = firebase.FirebaseApplication("https://smart-sockets.firebaseio.com/")

managers = []

def get():
    result = firebase.get("/users", None)
    inTheHouse = []
    for key, value in result.items():
        if value['in'] == 1:
            inTheHouse.append(value["email"])
    return inTheHouse

@bot.message_handler(commands=['start'])
def start(message):
    print("I am in start")
    counter = 0
    while counter < 1800:
        req = firebase.get("/globalstate", None)
        print(req)
        for k, v in req.items():
            if v["state"] == 1:
                bot.send_message(message.from_user.id, "В комнате возможно пожар. Оповещите этих студентов")
                result = get()
                bot.send_message(message.from_user.id, "В помещении находятся:")
                for el in result:
                    bot.send_message(message.from_user.id, el)
                if len(result) == 0:
                    bot.send_message(message.from_user.id, "Никто")
                firebase.put('/globalstate/' + k, "state", 0)

        counter += 1
        time.sleep(1)


@bot.message_handler(commands=['check'])
def getUsers(message):
    print("I am in check")
    result = get()
    bot.send_message(message.from_user.id, "В помещении находятся:")
    for el in result:
        bot.send_message(message.from_user.id, el)
    if len(result) == 0:
        bot.send_message(message.from_user.id, "Никто")

    

bot.polling(none_stop=True, interval=0)