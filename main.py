import telebot, json, random, os, time, datetime
from telebot import types
import os.path
from telebot import apihelper

with open("assets/data.json", "r", encoding="utf-8") as f:
    data = json.load(f)
    f.close()

with open("assets/acc.json", "r", encoding="utf-8") as f:
    acc = json.load(f)
    f.close()

api = telebot.TeleBot(data["token"])

def main_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("💻 Меню", "👤 Профиль")
    markup.row("🎰 Казино", "🛍 Магазин")
    markup.row("👥 Рефералки", "ℹ Информация")
    markup.row("📈 Статистика")
    if message.from_user.id in acc["admin"]: markup.row("🗒 Перезапуск бота", "🖥 Команды")
    else: markup.row("🗒 Перезапуск бота")
    return markup
def has_ref(id):
    if os.path.exists(f"assets/accounts/{id}.json"): return True
    else: False 

apihelper.proxy = {'http': data["proxy"], 'https': data["proxy"]}

@api.message_handler(content_types=["text"])
def message(message):
    try:
        s = message.text.split(" ")
        with open(f"assets/chats/{message.from_user.id}.txt", "a", encoding="utf-8") as f:
            f.write(f"[{datetime.datetime.now().hour}:{datetime.datetime.now().minute}] @{message.from_user.username} ({message.from_user.id}): {message.text}\n")
            f.close()
        tgk = []
        with open("assets/check.json", "r", encoding="utf-8") as f:
            ch = json.load(f)
            f.close()
        for i in range(0, len(acc["tgk"])):
            temp = api.get_chat_member(acc["tgk"][i], message.from_user.id)
            if temp.status != "left": tgk.append(1)
            else: tgk.append(0)
        if message.from_user.id in acc["banned"]:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            api.send_message(message.from_user.id, "❌ Сорян, но...\nВы были отправлены в чёрный список. Обжаловать можно в @qiwisteaml_bot", reply_markup=markup)
            pass
        elif 0 in tgk:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            api.send_message(message.from_user.id, "⚙ Проверка подписки на обязательные тгк...", reply_markup=markup)
            l = ""
            markup = types.InlineKeyboardMarkup()
            if not has_ref(id=message.from_user.id):
                if " " in message.text:
                    ref = int(message.text.split(" ")[1])
                    if message.from_user.id != ref and ref in acc["all"]:
                        with open('assets/ref.json', "r", encoding="utf-8") as f:
                            temp = json.load(f)
                            f.close()
                        with open('assets/ref.json', "w", encoding="utf-8") as f:
                            temp[f'{message.from_user.id}'] = int(ref)
                            json.dump(temp, f)
                            f.close()
            for i in range(0, tgk.count(0)):
                l += f"{acc['tgk'][tgk.index(0)]}\n"
                button1 = types.InlineKeyboardButton("Подписаться", url=f'https://{acc["tgk"][tgk.index(0)][1:len(acc["tgk"][tgk.index(0)])]}.t.me/')
                markup.add(button1)
                tgk[tgk.index(0)] = ""
            api.send_message(message.from_user.id, f"❌ Вы не подписались на все тгк!\n\nПодпишитесь на:\n{l}\nПосле чего повторите /start", reply_markup=markup)
            pass
        else:
            if os.path.exists(f"assets/accounts/{message.from_user.id}.json"):
                with open(f"assets/accounts/{message.from_user.id}.json", "r", encoding="utf-8") as f:
                    doc = json.load(f)
                    f.close()
            if message.from_user.id in acc["admin"]:
                msg = message.text.split(" ")
                if msg[0] == "/say":
                    a = 0
                    while(1):
                        try:
                            if a == len(acc["all"]): break 
                            else:
                                api.send_message(acc["all"][a], f"{message.text[4:len(message.text)]}")
                                a += 1
                        except: a += 1
                elif msg[0] == "/ban":
                    try: 
                        with open(f'assets/accounts/{msg[1]}.json', "r", encoding="utf-8") as f:
                            temp1 = json.load(f)
                            f.close()
                        acc["banned"].append(int(msg[1]))
                        with open(f'assets/acc.json', "w", encoding="utf-8") as f:
                            json.dump(acc, f)
                            f.close()
                        api.send_message(message.from_user.id, f"✅ Пользователь @{temp1['name']} был заблокирован!")
                    except: api.send_message(message.from_user.id, "❌ Пользователя, которого хотели заблокировать не существует!")
                elif msg[0] == "/bancas":
                    try: 
                        with open(f'assets/accounts/{msg[1]}.json', "r", encoding="utf-8") as f:
                            temp1 = json.load(f)
                            f.close()
                        acc["bannedcasino"].append(int(msg[1]))
                        with open(f'assets/acc.json', "w", encoding="utf-8") as f:
                            json.dump(acc, f)
                            f.close()
                        api.send_message(message.from_user.id, f"✅ Пользователь @{temp1['name']} был заблокирован в казино!")
                    except: api.send_message(message.from_user.id, "❌ Пользователя, которого хотели заблокировать не существует!")
                elif msg[0] == "/unban":
                    try: 
                        with open(f'assets/accounts/{msg[1]}.json', "r", encoding="utf-8") as f:
                            temp1 = json.load(f)
                            f.close()
                        acc["banned"].remove(int(msg[1]))
                        with open(f'assets/acc.json', "w", encoding="utf-8") as f:
                            json.dump(acc, f)
                            f.close()
                        api.send_message(message.from_user.id, f"✅ Пользователь @{temp1['name']} был разблокирован!")
                    except: api.send_message(message.from_user.id, "❌ Пользователя, которого хотели разблокировать не существует!")
                elif msg[0] == "/unbancas":
                    try: 
                        with open(f'assets/accounts/{msg[1]}.json', "r", encoding="utf-8") as f:
                            temp1 = json.load(f)
                            f.close()
                        acc["bannedcasino"].remove(int(msg[1]))
                        with open(f'assets/acc.json', "w", encoding="utf-8") as f:
                            json.dump(acc, f)
                            f.close()
                        api.send_message(message.from_user.id, f"✅ Пользователь @{temp1['name']} был разблокирован в казино!")
                    except: api.send_message(message.from_user.id, "❌ Пользователя, которого хотели разблокировать не существует!")
                elif msg[0] == "/new": 
                    with open('assets/prod.json', "r", encoding="utf-8") as f:
                        prod = json.load(f)
                        f.close()
                    r = random.randint(1, 9999999999)
                    msg = message.text.split('"')
                    if msg[1] in prod:
                        with open(f'assets/prod/{prod[msg[1]]["ID"]}.txt', "a", encoding="utf-8") as f:
                            f.write(msg[5]+"\n")
                            f.close()
                        with open('assets/prod.json', "w", encoding="utf-8") as f:
                            prod[msg[1]] = {"price": prod[msg[1]]["price"], "ID": prod[msg[1]]["ID"], "kolvo": prod[msg[1]]["kolvo"]+1}
                            json.dump(prod, f)
                            f.close()
                    else:
                        with open(f'assets/prod/{r}.txt', "w", encoding="utf-8") as f:
                            f.write(msg[5]+"\n")
                            f.close()
                        with open('assets/prod.json', "w", encoding="utf-8") as f:
                            prod[msg[1]] = {"price": int(msg[3]), "ID": r, "kolvo": 1}
                            json.dump(prod, f)
                            f.close()
                    api.send_message(message.from_user.id, f"✅ Товар '{msg[1]}' успешно разместился на полках магазина с ценой {msg[3]} QIWI монет!")
                elif msg[0] == "/grante" and int(msg[1]): # and message.from_user.id == 1959168915
                    try:
                        with open(f'assets/accounts/{msg[1]}.json', "r", encoding="utf-8") as f:
                            temp = json.load(f)
                            f.close()
                        with open(f'assets/accounts/{msg[1]}.json', "w", encoding="utf-8") as f:
                            temp["coin"] += int(msg[2])
                            json.dump(temp, f)
                            f.close()
                        api.send_message(message.from_user.id, f"✅ Пользователь @{temp['name']} пополнился на {msg[2]} QIWI монет!\nЕго счёт: {temp['coin']} монет")
                    except: api.send_message(message.from_user.id, "❌ Пользователя, у которого хотели пополнить монеты не существует!")
                elif msg[0] == "/takeoff" and int(msg[1]): # and message.from_user.id == 1959168915
                    try:
                        with open(f'assets/accounts/{msg[1]}.json', "r", encoding="utf-8") as f:
                            temp = json.load(f)
                            f.close()
                        with open(f'assets/accounts/{msg[1]}.json', "w", encoding="utf-8") as f:
                            temp["coin"] -= int(msg[2])
                            json.dump(temp, f)
                            f.close()
                        api.send_message(message.from_user.id, f"✅ Пользователь @{temp['name']} ограничился на {msg[2]} QIWI монет!\nЕго счёт: {temp['coin']} монет")
                    except: api.send_message(message.from_user.id, "❌ Пользователя, у которого хотели снять монеты не существует!")
                elif msg[0] == "/tgkon" and message.from_user.id == 1959168915:
                  try:
                      with open('assets/acc.json', "w", encoding="utf-8") as f:
                          acc["tgk"].append(msg[1])
                          json.dump(acc, f)
                          f.close()
                      api.send_message(message.from_user.id, f"✅ {msg[1]} добавлен в обязательные тгк, но попросите добавить админа этого тгк чтобы бот мог корректно работать!")
                  except: api.send_message(message.from_user.id, f"❌ Меня не добавили в {msg[1]}. Пожалуйста, добавьте в этот тгк")
                elif msg[0] == "/tgkoff" and message.from_user.id == 1959168915:
                    try:
                        with open('assets/acc.json', "w", encoding="utf-8") as f:
                            acc["tgk"].remove(msg[1])
                            json.dump(acc, f)
                            f.close()
                        api.send_message(message.from_user.id, f"✅ {msg[1]} убран из обязательных тгк!")
                    except: api.send_message(message.from_user.id, f'❌ {msg[1]} не был в обязательных подписок')
                elif msg[0] == "/send":
                    t = message.text.split('"')
                    api.send_message(int(t[1]), t[3])
                    api.send_message(message.from_user.id, "✅ Отправлено!")
                else:
                    if message.text[0:1] != "/" or msg[0] in ["/profile", "/ref", "/start"]: pass
                    else: api.send_message(message.from_user.id, "❌ Неизвестная команда!")
            if message.text == "/start" or message.text == "💻 Меню" or message.text.split(" ")[0] == "/start":
                if message.from_user.id not in acc["all"]:
                    a = 0
                    if not has_ref(id=message.from_user.id):
                        ref = None 
                        with open('assets/ref.json', "r", encoding="utf-8") as f:
                            temp1 = json.load(f)
                            f.close()
                        if " " in message.text:
                            referrer_candidate = message.text.split(" ")[1]
                            try:
                                referrer_candidate = int(referrer_candidate)
                                if message.from_user.id != referrer_candidate and referrer_candidate in acc["all"]:
                                    referer = referrer_candidate
                                    with open(f'assets/accounts/{referer}.json', 'r', encoding="utf-8") as f:
                                        temp = json.load(f)
                                        f.close()
                                    a += 5
                                    api.send_message(message.from_user.id, f"✅ Вы перешли по реферальной ссылке @{temp['name']}!\nВам бесплатно будет начислено 5 QIWI монет")
                                    api.send_message(referer, f"👤 Пользователь @{message.from_user.username} перешёл по вашей рефералке!\nВам начислено 15 QIWI монет и 1 реферал")
                                    with open(f'assets/accounts/{referer}.json', 'w', encoding="utf-8") as f:
                                        temp["coin"] += 15
                                        temp["ref"] += 1
                                        json.dump(temp, f)
                                        f.close()
                            except ValueError: pass
                        elif str(message.from_user.id) in temp1 and message.text == "/start":
                            ref = temp1[f"{message.from_user.id}"]
                            with open('assets/ref.json', "w", encoding="utf-8") as f:
                                del temp1[f'{message.from_user.id}']
                                json.dump(temp1, f)
                                f.close()
                            with open(f'assets/accounts/{ref}.json', 'r', encoding="utf-8") as f:
                                temp = json.load(f)
                                f.close()
                            a += 5
                            api.send_message(message.from_user.id, f"✅ Вы перешли по реферальной ссылке @{temp['name']}!\nВам бесплатно будет начислено 5 QIWI монет")
                            api.send_message(ref, f"👤 Пользователь @{message.from_user.username} перешёл по вашей рефералке!\nВам начислено 15 QIWI монет и 1 реферал")
                            with open(f'assets/accounts/{ref}.json', 'w', encoding="utf-8") as f:
                                temp["coin"] += 15
                                temp["ref"] += 1
                                json.dump(temp, f)
                                f.close()
                    else: message.text = "/start"
                    api.send_message(message.from_user.id, "Спасибо что выбрали наш проект!\nНадеюсь, у нас будете часто!")
                    acc["all"].append(message.from_user.id)
                    with open(f'assets/accounts/{message.from_user.id}.json', "w", encoding="utf-8") as f:
                        temp = {"name": message.from_user.username,
                            "ID": message.from_user.id,
                            "trade": None,
                            "ref": 0,
                            "coin": 0+a}
                        json.dump(temp, f)
                        f.close()
                    with open("assets/promo.json", "r", encoding="utf-8") as f:
                        temp = json.load(f)
                        f.close()
                    with open('assets/promo.json', "w", encoding="utf-8") as f:
                        temp[f"{message.from_user.id}"] = []
                        json.dump(temp, f)
                        f.close()
                    with open("assets/acc.json", "w", encoding="utf-8") as f:
                        json.dump(acc, f)
                        f.close()
                if message.from_user.id in ch["trade"]:
                    with open("assets/check.json", "w", encoding="utf-8") as f:
                        ch["trade"].remove(message.from_user.id)
                        json.dump(ch, f)
                        f.close()
                elif message.from_user.id in ch["shop"]:
                    with open("assets/check.json", "w", encoding="utf-8") as f:
                        ch["shop"].remove(message.from_user.id)
                        json.dump(ch, f)
                        f.close()
                elif message.from_user.id in ch["shop1.1"]:
                    with open("assets/check.json", "w", encoding="utf-8") as f:
                        ch["shop1.1"].remove(message.from_user.id)
                        json.dump(ch, f)
                        f.close()
                elif message.from_user.id in ch["promo"]:
                    with open("assets/check.json", "w", encoding="utf-8") as f:
                        ch["promo"].remove(message.from_user.id)
                        json.dump(ch, f)
                        f.close()
                    api.send_message(message.from_user.id, "Действие отменено.")
                elif message.from_user.id in ch["casino1"]:
                    with open("assets/check.json", "w", encoding="utf-8") as f:
                        ch["casino1"].remove(message.from_user.id)
                        json.dump(ch, f)
                        f.close()
                elif message.from_user.id in ch["casino2"]:
                    with open("assets/check.json", "w", encoding="utf-8") as f:
                        ch["casino2"].remove(message.from_user.id)
                        json.dump(ch, f)
                        f.close()
                elif message.from_user.id in ch["casino3"]:
                    with open("assets/check.json", "w", encoding="utf-8") as f:
                        ch["casino3"].remove(message.from_user.id)
                        json.dump(ch, f)
                        f.close()
                if message.from_user.username == None:
                    a = ""
                else:
                    a = f", @{message.from_user.username}"
                api.send_message(message.from_user.id, f"👋 Приветствую{a}!\n\nЭтот бот предназначен для получения ключей Steam, предметов из игр таких CS2, Dota, и других бесплатно!\n\n🤑 Получайте Qiwi монетки за приглашение друзей!\n💖 Покупайте ключи Steam за них\n🎰 Крутите казино и можете выиграть больше Qiwi монеток!", reply_markup=main_menu(message=message))
            elif message.text == "/profile" or message.text == "👤 Профиль":
                with open(f"assets/accounts/{message.from_user.id}.json", "r", encoding="utf-8") as f:
                    temp = json.load(f)
                    f.close()
                if temp["name"] == None:
                    temp["name"] = "(Ваш юзернейм был скрыт)"
                else: temp["name"] = f"@{temp['name']}"
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                markup.row("🔗 изменить трейд URL", "🎁 Активировать промо")
                markup.row("💻 Меню")
                api.send_message(message.from_user.id, f"🐧 Профиль\n\n👤 Имя: {temp['name']}\n💻 ID: {temp['ID']}\n 🔗 Трейд URL: {temp['trade']}\n👛 QIWI монеты: {temp['coin']}\n\n👥 Рефералы: {temp['ref']}", reply_markup=markup)
            elif s[0] == "/profile":
                try:
                    with open(f"assets/accounts/{s[1]}.json", "r", encoding="utf-8") as f:
                        temp = json.load(f)
                        f.close()
                    if temp["name"] == None:
                        temp["name"] = "Юзернейм был скрыт"
                    else: temp["name"] = f"@{temp['name']}"
                    api.send_message(message.from_user.id, f"🐧 Профиль\n\n👤 Имя: {temp['name']}\n💻 ID: {temp['ID']}\n 🔗 Трейд URL: {temp['trade']}\n👛 QIWI монеты: {temp['coin']}\n\n👥 Рефералы: {temp['ref']}")
                except: api.send_message(message.from_user.id,"❌ Данного профиля не существует! ")
            elif message.text == "🗒 Перезапуск бота":
                api.send_message(message.from_user.id, "⚙ Перезапуск бота...")
                time.sleep(1)
                api.send_message(message.from_user.id, "⚙ Обновление ваших данных...")
                with open(f'assets/accounts/{message.from_user.id}.json', "r", encoding="utf-8") as f:
                    temp = json.load(f)
                    f.close()
                with open(f'assets/accounts/{message.from_user.id}.json', "w", encoding="utf-8") as f:
                    temp["name"] = message.from_user.username
                    temp["ID"] = message.from_user.id
                    json.dump(temp, f)
                    f.close()
                time.sleep(1)
                api.send_message(message.from_user.id, "✅ Готово!")
            elif message.text == "🖥 Команды" and message.from_user.id in acc["admin"]:
                api.send_message(message.from_user.id, 'АДМИН КОМАНДЫ\n-----------------\n/say {текст}\n/new "{название товара}" "{цена}" "{содержимое (ключ)}"\n/ban {ID человека}\n/unban {ID человека}\n/bancas {ID человека}\n/unbancas {ID человека}\n/grante {ID человека} {сумма}\n/takeoff {ID человека} {сумма}\n/tgkon {тег тгк} (ТОЛЬКО ДЛЯ ВЛАДЕЛЬЦА)\n/tgkoff {тег тгк} (ТОЛЬКО ДЛЯ ВЛАДЕЛЬЦА)\n/send "{ID пользователя}" "{сообщение}"')
            elif message.text == "🔗 изменить трейд URL":
                with open("assets/check.json", "r", encoding="utf-8") as f:
                    temp = json.load(f)
                    f.close()
                with open("assets/check.json", "w", encoding="utf-8") as f:
                    temp["trade"].append(message.from_user.id)
                    json.dump(temp, f)
                    f.close()
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                markup.row("💻 Меню")
                api.send_message(message.from_user.id, "Жду вашу трейд URL Steam 🔗\n\nНапример: https://steamcommunity.com/tradeoffer/new/?partner=123456789&token=abcDEFG123\n(ВНИМАНИЕ: если не укажите валидный URL, то товар не поступит к вам!)", reply_markup=markup)
            elif message.text == "🎁 Активировать промо" and doc["ref"] < 1: api.send_message(message.from_user.id, "❌ Вы не можете активировать промо без 1 реферала!")
            elif message.text == "🎁 Активировать промо" and doc["ref"] > 0:
                with open("assets/check.json", "r", encoding="utf-8") as f:
                    temp = json.load(f)
                    f.close()
                with open("assets/check.json", "w", encoding="utf-8") as f:
                    temp["promo"].append(message.from_user.id)
                    json.dump(temp, f)
                    f.close()
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                markup.row("💻 Меню")
                api.send_message(message.from_user.id, "Жду активацию промокода\n\nОн бывает из рандомных цифр, но бывает и из слов", reply_markup=markup)
            elif message.text == "ℹ Информация": 
                api.send_message(message.from_user.id, """👤 Владелец/разработчик: @nn1kk00 (обратная связь: @qiwisteaml_bot), только по тех. проблемам и товарам
Модератор: @мику, только по товарам
----
Q: Что делать если бот выдал ошибку?
A: N1kk00 уже знает об проблеме, и попытается решить. С ним можно связаться через @мику
                                 
Q: Можно ли сделать возврат на товар который получил/активировал?
A: Нет, вы уже использовали. Но, если не получили, то возможно

Q: Верни монеты какашка
A: Нет, если вы потеряли QIWI монеты в казино: то не сможем вернуть, вы на свой риск испытываете свою удачу и возврату не подлежит. Также если забрал администратор бота по оправдающим причинам.

Q: Можно отписаться от спонсоров?
A: Нет, без спонсоров бот не пропустит к его функциям
                                 
Q: РАЗБАНЬ МЕНЯ АЛО 
A: Только лишь по весомым причинам
                                 
Q: ЭЭЭ, ЗА ЧТО БЛОК В КАЗИКЕ
A: Походу, вы слишком много заработали в казино. Данный бан временный, на неделю

Q: Мне не засчитался реферал, что делать
A: Если друг перешёл по рефералке и у вас не засчитался, надо ему было повторно перейти по рефералу
-----
Об других проблемах пишите в @qiwisteaml_bot""")
            elif message.text == "🛍 Магазин":  
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                markup.row("💻 Меню")
                with open('assets/prod.json', "r", encoding='utf-8') as f:
                    prod = json.load(f)
                    f.close()
                if len(prod) == 0:
                    api.send_message(message.from_user.id, "Товаров пока-что нет на полках.", reply_markup=markup)
                else:
                    with open("assets/check.json", "w", encoding="utf-8") as f:
                        ch["shop"].append(message.from_user.id)
                        json.dump(ch, f)
                        f.close()
                    for i in range(0, len(prod)):
                        markup.row(f"{list(prod.keys())[i]}")
                    api.send_message(message.from_user.id, "Все товары:", reply_markup=markup)
            elif message.text == "📈 Статистика":
                allacc = os.listdir('assets/accounts/')
                t = {"ref": 0, "coin": 0, "all": acc["all"]}
                for i in range(0, len(allacc)):
                    with open(f'assets/accounts/{allacc[i]}', 'r', encoding="utf-8") as f:
                        temp = json.load(f)
                        f.close()
                    t["coin"] += temp["coin"]
                    t["ref"] += temp["ref"]
                api.send_message(message.from_user.id, f"📈 Статистика бота\n\n👤 Всего пользователей: {len(t['all'])}\n👥 Всего пользователей, перешедших по рефералке: {t['ref']}\n👛 Всего QIWI монет у всех пользователей: {t['coin']}")
            elif message.text == "👥 Рефералки" or message.text == "/ref": api.send_message(message.from_user.id, f"Ваша реферальная ссылка:\nhttps://t.me/qiwiterminalbox_bot?start={message.from_user.id}\n\nЗа реферала 👛 15 QIWI монет!\n👥 Ваши рефералы: {doc['ref']}")
            elif message.text == "🎰 Казино" and message.from_user.id in acc["bannedcasino"]:
                api.send_message(message.from_user.id, "❌ Вы были заблокированы в казино.\n(Лудомания: плохо!)")
            elif message.text == "🎰 Казино" and message.from_user.id not in acc["bannedcasino"]:
                with open(f"assets/accounts/{message.from_user.id}.json", "r", encoding="utf-8") as f:
                    temp = json.load(f)
                    f.close()
                if temp["coin"] < 10: api.send_message(message.from_user.id, "❌ Вы не можете посетить казино, у вас меньше 10 QIWI монеток!", reply_markup=main_menu(message=message))
                else:
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    markup.row("💻 Меню")
                    markup.row("🀄 Угадай число", "🎲 Кубик")
                    markup.row("👤 ВСЁ или НИЧЕГО")
                    api.send_message(message.from_user.id, "Выберите игру:", reply_markup=markup)
            elif message.text == "🎲 Кубик" and message.from_user.id not in acc["bannedcasino"]:
                with open("assets/check.json", "r", encoding="utf-8") as f:
                    temp = json.load(f)
                    f.close()
                with open("assets/check.json", "w", encoding="utf-8") as f:
                    temp["casino2"].append(message.from_user.id)
                    json.dump(temp, f)
                    f.close()
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                markup.row("1", "2", "3", "4")
                markup.row("💻 Меню")
                api.send_message(message.from_user.id, "Выбрана игра: 🎲 Кубик\n\nВ данной игре можно испытать удачу над великим рандомом.\n Есть 4 режима:\n1. Итог 6-9 - выигрыш х2 (вклад 10 монет)\n2. Итог 3-6 - выигрыш х2 (вклад 20 монет)\n3. Итог 8-10 - выигрыш х2 (вклад 30 монет)\n4. Итог 9 - выигрыш х2.(вклад 45 монет)\n\nВыберите режим ниже:", reply_markup=markup)
            elif message.text == "👤 ВСЁ или НИЧЕГО" and message.from_user.id not in acc["bannedcasino"]:
                with open("assets/check.json", "r", encoding="utf-8") as f:
                    temp = json.load(f)
                    f.close()
                with open("assets/check.json", "w", encoding="utf-8") as f:
                    temp["casino3"].append(message.from_user.id)
                    json.dump(temp, f)
                    f.close()
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                markup.row("Продолжить", "💻 Меню")
                api.send_message(message.from_user.id, "Выбрана игра: 👤 ВСЁ или НИЧЕГО\n\nВ данной игре можно попытаться выбить х2 вашей всей суммы.\nНО, ЕСЛИ ВЫ ПРОИГРАЕТЕ: ПОТЕРЯЕТЕ ВСЕ МОНЕТЫ! Так что играйте с осторожностью.\nШанс: 25%.\nПродолжить?", reply_markup=markup)
            elif message.text == "🀄 Угадай число" and message.from_user.id not in acc["bannedcasino"]:
                with open("assets/check.json", "r", encoding="utf-8") as f:
                    temp = json.load(f)
                    f.close()
                with open("assets/check.json", "w", encoding="utf-8") as f:
                    temp["casino1"].append(message.from_user.id)
                    json.dump(temp, f)
                    f.close()
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                markup.row("Продолжить", "💻 Меню")
                api.send_message(message.from_user.id, "Выбрана игра: 🀄 Угадай число\n\nВ данной игре я загадываю число от 1 до 10, а ты должен отгадать.\nЕсли отгадаешь: умножишь свою сумму в 3 раза.\nВклад: 10 монет.\nПродолжить?", reply_markup=markup)
            else:
                with open("assets/check.json", "r", encoding="utf-8") as f:
                    temp = json.load(f)
                    f.close()
                with open(f"assets/accounts/{message.from_user.id}.json", "r", encoding="utf-8") as f:
                    temp1 = json.load(f)
                    f.close()
                if message.from_user.id in temp["trade"]:
                    with open("assets/check.json", "w", encoding="utf-8") as f:
                        temp["trade"].remove(message.from_user.id)
                        json.dump(temp, f)
                        f.close()
                    with open(f"assets/accounts/{message.from_user.id}.json", "r", encoding="utf-8") as f:
                        temp = json.load(f)
                        f.close()
                    with open(f"assets/accounts/{message.from_user.id}.json", "w", encoding="utf-8") as f:
                        temp["trade"] = message.text
                        json.dump(temp, f)
                        f.close()
                    api.send_message(message.from_user.id, "🔰 Трейд URL был изменён!", reply_markup=main_menu(message=message))
                elif message.from_user.id in temp["promo"]:
                    with open("assets/check.json", "w", encoding="utf-8") as f:
                        temp["promo"].remove(message.from_user.id)
                        json.dump(temp, f)
                        f.close()
                    with open(f"assets/accounts/{message.from_user.id}.json", "r", encoding="utf-8") as f:
                        acc1 = json.load(f)
                        f.close()
                    with open("assets/promo.json", "r", encoding="utf-8") as f:
                        pr1 = json.load(f)
                        f.close()
                    with open("assets/promo1.json", "r", encoding="utf-8") as f:
                        pr2 = json.load(f)
                        f.close()
                    if message.text in pr1[f'{message.from_user.id}']:
                        api.send_message(message.from_user.id, "❌ Данный промокод уже был у вас использован!", reply_markup=main_menu(message=message))
                    elif message.text not in pr2["promo"]:
                        api.send_message(message.from_user.id, "❌ Данного промокода не существует!", reply_markup=main_menu(message=message))
                    elif pr2["grante"][pr2["promo"].index(message.text)] == 0:
                        api.send_message(message.from_user.id, "❌ Данный промокод уже был исчерпан!", reply_markup=main_menu(message=message))
                    else:
                        temp = pr2["grante"][pr2["promo"].index(message.text)]
                        with open("assets/promo1.json", "w", encoding="utf-8") as f:
                            pr2["use"][pr2["promo"].index(message.text)] -=1
                            if pr2["use"][pr2["promo"].index(message.text)] == 0:
                                pr2["use"].pop(pr2["promo"].index(message.text))
                                pr2["grante"].pop(pr2["promo"].index(message.text))
                                pr2["promo"].remove(message.text)
                            json.dump(pr2, f)
                            f.close()
                        with open("assets/promo.json", "w", encoding="utf-8") as f:
                            pr1[f"{message.from_user.id}"].append(message.text)
                            json.dump(pr1, f)
                            f.close()
                        with open(f"assets/accounts/{message.from_user.id}.json", "w", encoding="utf-8") as f:
                            acc1["coin"] += temp
                            json.dump(acc1, f)
                            f.close()
                        api.send_message(message.from_user.id, f"Промокод был активирован и зачислено {temp} Qiwi монеток!", reply_markup=main_menu(message=message))
                elif message.from_user.id in temp["casino2"] and message.from_user.id not in acc["bannedcasino"]:
                    if message.text == "1":
                        with open(f"assets/accounts/{message.from_user.id}.json", "r", encoding="utf-8") as f:
                            acc1 = json.load(f)
                            f.close()
                        if acc1["coin"] < 10:
                            api.send_message(message.from_user.id, "НЕДОСТАТОЧНО МОНЕТ ДЛЯ ИГРЫ.")
                        else:
                            api.send_message(message.from_user.id, "🎲 Погнали...")
                            r = random.randint(1, 12)
                            with open(f"assets/accounts/{message.from_user.id}.json", "w", encoding="utf-8") as f:
                                acc1["coin"] -= 10
                                json.dump(acc1, f)
                                f.close()
                            if r > 5 and r < 10:
                                with open(f"assets/accounts/{message.from_user.id}.json", "w", encoding="utf-8") as f:
                                    acc1["coin"] += 10*2
                                    json.dump(acc1, f)
                                    f.close()
                                api.send_message(message.from_user.id, f"✅ Вам повезло, выпала цифра {r}!\nВы умножили свои 10 QIWI монет в x2 раза!\nТеперь ваша сумма составляет {acc1['coin']} монет!")
                            else:
                                api.send_message(message.from_user.id, f"❌ К несчатью, вам выпала цифра {r}.\nВы потеряли свои 10 QIWI монет.\nТеперь ваша сумма составляет {acc1['coin']} монет.")
                    if message.text == "2":
                        with open(f"assets/accounts/{message.from_user.id}.json", "r", encoding="utf-8") as f:
                            acc1 = json.load(f)
                            f.close()
                        if acc1["coin"] < 20:
                            api.send_message(message.from_user.id, "НЕДОСТАТОЧНО МОНЕТ ДЛЯ ИГРЫ.")
                        else:
                            api.send_message(message.from_user.id, "🎲 Погнали...")
                            r = random.randint(1, 12)
                            with open(f"assets/accounts/{message.from_user.id}.json", "w", encoding="utf-8") as f:
                                acc1["coin"] -= 20
                                json.dump(acc1, f)
                                f.close()
                            if r > 2 and r < 7:
                                with open(f"assets/accounts/{message.from_user.id}.json", "w", encoding="utf-8") as f:
                                    acc1["coin"] += 20*2
                                    json.dump(acc1, f)
                                    f.close()
                                api.send_message(message.from_user.id, f"✅ Вам повезло, выпала цифра {r}!\nВы умножили свои 20 QIWI монет в x2 раза!\nТеперь ваша сумма составляет {acc1['coin']} монет!")
                            else:
                                api.send_message(message.from_user.id, f"❌ К несчатью, вам выпала цифра {r}.\nВы потеряли свои 20 QIWI монет.\nТеперь ваша сумма составляет {acc1['coin']} монет.")
                    if message.text == "3":
                        with open(f"assets/accounts/{message.from_user.id}.json", "r", encoding="utf-8") as f:
                            acc1 = json.load(f)
                            f.close()
                        if acc1["coin"] < 30:
                            api.send_message(message.from_user.id, "НЕДОСТАТОЧНО МОНЕТ ДЛЯ ИГРЫ.")
                        else:
                            api.send_message(message.from_user.id, "🎲 Погнали...")
                            r = random.randint(1, 12)
                            with open(f"assets/accounts/{message.from_user.id}.json", "w", encoding="utf-8") as f:
                                acc1["coin"] -= 30
                                json.dump(acc1, f)
                                f.close()
                            if r > 7 and r < 11:
                                with open(f"assets/accounts/{message.from_user.id}.json", "w", encoding="utf-8") as f:
                                    acc1["coin"] += 30*2
                                    json.dump(acc1, f)
                                    f.close()
                                api.send_message(message.from_user.id, f"✅ Вам повезло, выпала цифра {r}!\nВы умножили свои 30 QIWI монет в x2 раза!\nТеперь ваша сумма составляет {acc1['coin']} монет!")
                            else:
                                api.send_message(message.from_user.id, f"❌ К несчатью, вам выпала цифра {r}.\nВы потеряли свои 30 QIWI монет.\nТеперь ваша сумма составляет {acc1['coin']} монет.")
                    if message.text == "4":
                        with open(f"assets/accounts/{message.from_user.id}.json", "r", encoding="utf-8") as f:
                            acc1 = json.load(f)
                            f.close()
                        if acc1["coin"] < 40:
                            api.send_message(message.from_user.id, "НЕДОСТАТОЧНО МОНЕТ ДЛЯ ИГРЫ.")
                        else:
                            api.send_message(message.from_user.id, "🎲 Погнали...")
                            r = random.randint(1, 12)
                            with open(f"assets/accounts/{message.from_user.id}.json", "w", encoding="utf-8") as f:
                                acc1["coin"] -= 40
                                json.dump(acc1, f)
                                f.close()
                            if r == 9:
                                with open(f"assets/accounts/{message.from_user.id}.json", "w", encoding="utf-8") as f:
                                    acc1["coin"] += 40*2
                                    json.dump(acc1, f)
                                    f.close()
                                api.send_message(message.from_user.id, f"✅ ДЖЕКПОТ, выпала цифра {r}!\nВы умножили свои 40 QIWI монет в x2 раза!\nТеперь ваша сумма составляет {acc1['coin']} монет!")
                            else:
                                api.send_message(message.from_user.id, f"❌ К несчатью, вам выпала цифра {r}.\nВы потеряли свои 40 QIWI монет.\nТеперь ваша сумма составляет {acc1['coin']} монет.")
                elif message.from_user.id in temp["casino3"] and message.text == "Продолжить" and message.from_user.id not in acc["bannedcasino"]:
                    with open(f"assets/accounts/{message.from_user.id}.json", "r", encoding="utf-8") as f:
                        acc1 = json.load(f)
                        f.close()
                    api.send_message(message.from_user.id, "Твой выбор...")
                    if random.randint(1, 4) == 4:
                        with open(f"assets/accounts/{message.from_user.id}.json", "w", encoding="utf-8") as f:
                            acc1["coin"] = acc1["coin"]*2
                            json.dump(acc1, f)
                            f.close()
                        api.send_message(message.from_user.id, f"✅ Ты умножил свою сумму в 2 раза!\nТеперь составляет: {acc1['coin']} монет!")
                    else:
                        with open(f"assets/accounts/{message.from_user.id}.json", "w", encoding="utf-8") as f:
                            acc1["coin"] = 0
                            json.dump(acc1, f)
                            f.close()
                        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                        markup.row("💻 Меню")
                        with open("assets/check.json", "w", encoding="utf-8") as f:
                            temp["casino3"].remove(message.from_user.id)
                            json.dump(temp, f)
                            f.close()
                        api.send_message(message.from_user.id, "❌ Плохая новость...\nТы проиграл всю свою сумму... \nТеперь составляет: 0 монет.", reply_markup=markup)
                elif message.from_user.id in temp["casino1"] and message.text == "Продолжить" and message.from_user.id not in acc["bannedcasino"]:
                    with open(f"assets/accounts/{message.from_user.id}.json", "r", encoding="utf-8") as f:
                        temp1 = json.load(f)
                        f.close()
                    if temp1["coin"] < 10: api.send_message(message.from_user.id, "НЕДОСТАТОЧНО МОНЕТ ДЛЯ ИГРЫ")
                    else:
                        with open("assets/check.json", "w", encoding="utf-8") as f:
                            temp["casino1"].remove(message.from_user.id)
                            temp["casino1.1"].append(message.from_user.id)
                            json.dump(temp, f)
                            f.close()
                        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                        markup.row("💻 Меню")
                        api.send_message(message.from_user.id, "🧝‍♂️ Число загадано.\nВведите любое предпологаемое число от 1 до 10 ниже", reply_markup=markup)
                elif message.from_user.id in temp["casino1.1"] and int(message.text) > 0 and int(message.text) < 11:
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    markup.row("💻 Меню")
                    markup.row("🀄 Угадай число", "🎲 Кубик")
                    markup.row("👤 ВСЁ или НИЧЕГО")
                    with open("assets/check.json", "w", encoding="utf-8") as f:
                        temp["casino1.1"].remove(message.from_user.id)
                        json.dump(temp, f)
                        f.close()
                    with open(f"assets/accounts/{message.from_user.id}.json", "r", encoding="utf-8") as f:
                        acc1 = json.load(f)
                        f.close()
                    with open(f"assets/accounts/{message.from_user.id}.json", "w", encoding="utf-8") as f:
                        acc1["coin"] -= 10
                        json.dump(acc1, f)
                        f.close()
                    if message.text == random.randint(1,10):
                        with open(f"assets/accounts/{message.from_user.id}.json", "w", encoding="utf-8") as f:
                            acc1["coin"] += 30
                            json.dump(acc1, f)
                            f.close()
                        api.send_message(message.from_user.id, f"✅ Ты умножил свою сумму в 3 раза!\nТеперь составляет: {acc1['coin']} монет!", reply_markup=markup)
                    else:
                        api.send_message(message.from_user.id, f"❌ К несчатью, вы не угадали.\nВы потеряли свои 10 QIWI монет.\nТеперь ваша сумма составляет {acc1['coin']} монет.", reply_markup=markup)
                elif message.from_user.id in temp["shop"]:
                    if temp1["ref"] < 5:
                        api.send_message(message.from_user.id, "❌ Вы не можете ничего купить, пока нет 5 рефералов!")
                    else:
                        with open("assets/check.json", "r", encoding="utf-8") as f:
                            temp = json.load(f)
                            f.close()
                        with open("assets/prod.json", "r", encoding="utf-8") as f:
                            prod = json.load(f)
                            f.close()
                        with open("assets/prod1.json", "r", encoding="utf-8") as f:
                            prod1 = json.load(f)
                            f.close()
                        if message.text in list(prod.keys()):
                            with open("assets/check.json", "w", encoding="utf-8") as f:
                                temp["shop"].remove(message.from_user.id)
                                temp["shop1.1"].append(message.from_user.id)
                                json.dump(temp, f)
                                f.close()
                            with open("assets/prod1.json", "w", encoding="utf-8") as f:
                                prod1[f"{message.from_user.id}"] = message.text
                                json.dump(prod1, f)
                                f.close()
                            maсkup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                            maсkup.row("Да", "Нет", "💻 Меню")
                            user_id = str(message.from_user.id)
                            key_from_prod1 = prod1[user_id]  # Получаем ключ для prod
                            price = prod[key_from_prod1]["price"]  # Берём цену по этому ключ
                            idt = prod[key_from_prod1]["ID"]  # Берём цену по этому ключу
                            name = key_from_prod1
                            api.send_message(message.from_user.id, f"⚠ Вы действительно хотите купить '{message.text}'?\n\nЦена: {price} QIWI монет\nКол-во товара: {prod[key_from_prod1]['kolvo']}", reply_markup=maсkup)
                        else:
                            api.send_message(message.from_user.id, "❌ Нет такого товара на полках!\nВыберите ниже, нажав на кнопку.")
                elif message.from_user.id in temp["shop1.1"]:
                    if temp1["ref"] < 5: api.send_message(message.from_user.id, "❌ Вы не можете ничего купить, пока нет 5 рефералов!")
                    else:
                        with open(f"assets/accounts/{message.from_user.id}.json", "r", encoding="utf-8") as f:
                            acc1 = json.load(f)
                            f.close()
                        with open("assets/prod1.json", "r", encoding="utf-8") as f:
                            prod1 = json.load(f)
                            f.close()
                        with open("assets/prod.json", "r", encoding="utf-8") as f:
                            prod = json.load(f)
                            f.close()
                        if message.text == "Да":
                            api.send_message(message.from_user.id, "⚙ Операция выполняется...")
                            user_id = str(message.from_user.id)
                            key_from_prod1 = prod1[user_id]  # Получаем ключ для prod
                            price = prod[key_from_prod1]["price"]  # Берём цену по этому ключ
                            idt = prod[key_from_prod1]["ID"]  # Берём цену по этому ключу
                            kolvo = prod[key_from_prod1]["kolvo"]  # Берём цену по этому ключу
                            name = key_from_prod1
                            if acc1["trade"] == None: api.send_message(message.from_user.id, """❌ Вы не привязали трейд ссылку!

Чтобы получить вашу трейд ссылку в Steam:
1. Наведитесь на ваш профиль и нажмите  "Инвентарь"
2. После открытия вашего инвентаря, будет синяя кнопка "Предложения обмена". Нажмите на неё
3. После открытия следующей страницы с трейдами, в правом блоке будет текст "Кто может отправлять мне предложения обмена?", туда нажмите
4. Скопируйте ссылку

Чтобы привязать к профилю бота:
Профиль » Изменить трейд ссылку » Вставьте вашу скопированную трейд ссылку""")
                            elif acc1["coin"] < price: api.send_message(message.from_user.id, "❌ К сожелению, у вас недостаточно монет для покупки данного товара.", reply_markup=main_menu(message=message))
                            else:
                                with open('assets/check.json', "w", encoding="utf-8") as f:
                                    temp["shop1.1"].remove(message.from_user.id)
                                    json.dump(temp, f)
                                    f.close()
                                with open(f"assets/accounts/{message.from_user.id}.json", "w", encoding="utf-8") as f:
                                    acc1["coin"] -= price
                                    json.dump(acc1, f)
                                    f.close()
                                with open(f"assets/prod1.json", "w", encoding="utf-8") as f:
                                    del prod1[str(message.from_user.id)]
                                    json.dump(prod1, f)
                                    f.close()
                                with open(f"assets/prod.json", "w", encoding="utf-8") as f:
                                    if prod[key_from_prod1]["kolvo"]-1 == 0:
                                        del prod[key_from_prod1]
                                    else: prod[key_from_prod1]["kolvo"] -= 1
                                    json.dump(prod, f)
                                    f.close()
                                with open(f"assets/prod/{idt}.txt", "r", encoding="utf-8") as f:
                                    text = f.readlines()
                                    text = text[kolvo-1]
                                    f.close()
                                os.remove(f"assets/prod/{idt}.txt")
                                api.send_message(message.from_user.id, f"✅ Вы успешно купили товар '{name}'!\n\n{text}\n💵 С вас списано {price} QIWI монет!\nНа счету осталось {acc1['coin']} QIWI монет.", reply_markup=main_menu(message=message))
                                api.send_message(message.from_user.id, "При получении товара, оставьте отзыв в @qiwisteaml_bot!")
                                for i in range(0, len(acc["admin"])):
                                    api.send_message(acc["admin"][i], f"✅ @{message.from_user.username}({message.from_user.id}) купил товар!\nИнформация о товаре:\nИмя: {name}\nЦена: {price}\nКол-во осталось: {kolvo-1}\nСодержимое: {text}Информация о пользователе:\nИмя: @{message.from_user.username}({message.from_user.id})\nТрейд ссылка: {acc1['trade']}\nМонет осталось: {acc1['coin']}")
                        else:
                            with open('assets/check.json', "w", encoding="utf-8") as f:
                                temp["shop1.1"].remove(message.from_user.id)
                                json.dump(temp, f)
                                f.close()
                            with open(f"assets/prod1.json", "w", encoding="utf-8") as f:
                                del prod1[str(message.from_user.id)]
                                json.dump(prod1, f)
                                f.close()
                            api.send_message(message.from_user.id, "❌ Операция отменена", reply_markup=main_menu(message=message))
                else:
                    if message.from_user.id in acc["admin"] and message.text[0:1] == "/": pass
                    else: api.send_message(message.from_user.id, "❌ Неизвестная команда!")
    except Exception as e:
        api.send_message(1959168915, f"Произошла ошибка в коде.\n\nError: {e}\nMessage: {message.text}")
        api.send_message(message.from_user.id, f"Произошла ошибка в коде.\n\nError: {e}\nMessage: {message.text}") 
        with open("ex.txt", "a", encoding="utf-8") as file:
            file.write(f"Error: {e}\nMessage: {message.text}\n") 
            file.close()

api.polling()
