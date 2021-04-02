import re
import vk_api
from vk_api.utils import get_random_id
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.longpoll import VkLongPoll, VkEventType
from const import TOKEN, nike_size, admin_id, load_photo
from const import get_eur_Sber, get_eur_Tinkoff, get_eur_CB
from SQLite_db import *


""" ИНИЦИЛИЗАЦИЯ """
vk_session = vk_api.VkApi(token=TOKEN)
vk = vk_session.get_api()
long_poll = VkLongPoll(vk_session)
upload = vk_api.VkUpload(vk_session)


""" КНОПКИ """
# для юзера
keyboard = VkKeyboard(one_time=False)
keyboard.add_button('Калькулятор', color='secondary')
keyboard.add_button('Услуги группы', color='secondary')
keyboard.add_line()
keyboard.add_button('Таблица размеров', color='secondary')
keyboard.add_button('Календарь релизов', color='secondary')
keyboard.add_line()
keyboard.add_button('Связь с админом', color='positive')
keyboard.add_line()
keyboard.add_button('Перезагрузить бота', color='negative')

# для админа
keyboard_admin = VkKeyboard(one_time=False)
keyboard_admin.add_button('Загрузить фото', color='positive')
keyboard_admin.add_line()
keyboard_admin.add_button('Очистить список релизов', color='secondary')
keyboard_admin.add_line()
keyboard_admin.add_button('Выход', color='negative')

# для товаров
keyboard_product = VkKeyboard(one_time=False)
keyboard_product.add_button('Legit Check', color='secondary')
keyboard_product.add_line()
keyboard_product.add_button('Гарант', color='secondary')
keyboard_product.add_line()
keyboard_product.add_button('Продажа за границу', color='secondary')
keyboard_product.add_line()
keyboard_product.add_button('Реклама', color='secondary')
keyboard_product.add_line()
keyboard_product.add_button('Назад', color='negative')

# для выбора курса
keyboard_eur = VkKeyboard(one_time=False)
keyboard_eur.add_button(f"Сбербанк [{get_eur_Sber()}]", color='secondary')
keyboard_eur.add_line()
keyboard_eur.add_button(f"Тинькофф [{get_eur_Tinkoff()}]", color='secondary')
keyboard_eur.add_line()
keyboard_eur.add_button('Назад', color='negative')

# для диалога
keyboard_dialog = VkKeyboard(one_time=False)
keyboard_dialog.add_button('Завершить диалог', color='negative')

""" ОТПРАВКА СООБЩЕНИЙ """
def send_msg(id, text):
    vk.messages.send(
        peer_id=id,
        random_id=get_random_id(),
        keyboard=keyboard.get_keyboard(),
        message=text
    )

def send_msg_admin(id, text):
    vk.messages.send(
        peer_id=id,
        random_id=get_random_id(),
        keyboard=keyboard_admin.get_keyboard(),
        message=text
    )

def send_msg_product(id, text):
    vk.messages.send(
        peer_id=id,
        random_id=get_random_id(),
        keyboard=keyboard_product.get_keyboard(),
        message=text
    )

def send_msg_eur(id, text):
    vk.messages.send(
        peer_id=id,
        random_id=get_random_id(),
        keyboard=keyboard_eur.get_keyboard(),
        message=text
    )
def send_dialog(id, text):
    vk.messages.send(
        peer_id=id,
        random_id=get_random_id(),
        keyboard=keyboard_dialog.get_keyboard(),
        message=text
    )

""" ОСНОВНОЙ ЦИКЛ СОБЫТИЙ """
for event in long_poll.listen():

    # если сообщение новое ...  &  если сообщение пришло именно моему боту ...
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:

        msg = event.text  # само сообщение
        id = event.user_id  # id пользователя

        # ЗАПИСЬ РЕЛИЗОВ
        if admin_id is not None and load_photo:
            # открыл файл на запись
            file = open('photos_id.txt', 'a')

            if msg == "Выход":
                admin_id = None  # отключил режим админа
                load_photo = False  # отключил флаг на загрузку релизов
                file.close()  # закрыл файл
                send_msg(id, "Админка отключена")

            elif msg == "Очистить список релизов":
                file = open('photos_id.txt', 'w')
                file.write("")
                file.close()
                send_msg_admin(id, "Очистка прошла успешно ✅\nЗагрузка идет, отправь данные, как в примере")

            elif msg == "Загрузить фото":
                send_msg_admin(id, "Запись уже идёт! Отправь данные, как в примере")

            else:
                file.write(msg + "\n;\n")
                send_msg_admin(id, "Отлично✅\nКогда закончишь, нажми Выход🚸")

# ФУНКЦИОНАЛ ОБЫЧНОГО ЮЗЕРА
        elif id != admin_id:
            if msg.lower() == "/start" or msg.lower() == "начать" or msg.lower() == "старт" or msg.lower() == "start":
                send_msg(id, "Привет 😊")
                send_msg(id, "Выберите действие\nИ нажмите на кнопку👇")
                #  запиь в бд
                if user_exists(id):
                    change_userstatus(id, "menu")
                else:
                    add_user(id, 0, "menu")

            elif msg.lower() == "завершить диалог":
                send_msg(id, "Разговор окончен")
                #  запиь в бд
                if user_exists(id):
                    change_userstatus(id, "menu")
                else:
                    add_user(id, 0, "menu")

            else:
                #  запиь в бд
                if user_exists(id):
                    pass
                else:
                    add_user(id, 0, "menu")

            if check_userinfo(id)['status'] != "dialog":

                if msg.lower() == "/start" or msg.lower() == "начать" or msg.lower() == "старт" or msg.lower() == "start":
                    pass

                elif msg.lower() == "завершить диалог":
                    pass

                elif msg == "Калькулятор":
                    send_msg(id, f"Курс евро в рублях:\n"
                                 f"📈 СберБанк: {get_eur_Sber()}₽\n"
                                 f"📉 Тинькофф: {get_eur_Tinkoff()}₽")

                    #  запиь в бд
                    if user_exists(id):
                        change_userstatus(id, "eur")
                    else:
                        add_user(id, 0, "eur")

                    send_msg_eur(id, "Выберите необходимый Вам курс евро\n" +
                                     "Если такого нет, напишите его сами\n" +
                                     "Например: 90.55")

                elif check_userinfo(id)['status'] == "eur":
                    if msg[:8] == "Сбербанк" or msg[:8] == "Тинькофф":
                        rub = float(msg[10:-1])
                        change_user_rub(id, rub)
                        change_userstatus(id, "sum")
                        send_msg(id, "Введите стоимость каждого Вашего товара через пробел в евро\n" +
                                 "Например: 50 100 56")

                    elif re.match(r'^[0-9]{1,3}[,.]{1}[0-9]{1,3}$', msg):
                        rub = float(msg.replace(",", "."))
                        change_user_rub(id, rub)
                        change_userstatus(id, "sum")
                        send_msg(id, "Введите стоимость каждого Вашего товара через пробел в евро\n" +
                                 "Например: 50 100 56")
                    elif msg == "Назад":
                        change_userstatus(id, "menu")
                        send_msg(id, "Вы вышли в главное меню")
                    else:
                        send_msg_eur(id, "Не корректный ввод круса")


                elif msg.replace(" ", "").isdigit() and check_userinfo(id)['status'] == "sum":
                    dictt = msg.split(' ')
                    subtotal = 0

                    for i in dictt:
                        subtotal = int(i) + subtotal

                    VAT = 0.8333333333  # НДС = 1 - 0.833333
                    postage = 36  # eur
                    total = 0
                    total_rub = 0
                    curs = float(check_userinfo(id)['rub'])

                    x = subtotal * VAT
                    if x >= 200:
                        postage = 0
                        customs = 1100  # руб
                        tax = 0.15 * (subtotal * VAT - 200)
                        total = x + tax  # итог в евро и еще нужно прибавить 1100
                        total_rub = float(total) * curs + 1100
                        change_userstatus(id, "menu")
                        send_msg(id, f"subtotal €{subtotal}\n" 
                                     f"VAT discount -€{round(subtotal * (1 - VAT), 2)}\n" 
                                     f"postage €{postage}\n" 
                                     f"order total €{round(x, 2)} / {round(x * curs, 2)}₽\n"
                                     f"➡ рассчитано по курсу: {curs}₽\n\n"
                                     
                                     f"налог 15%: €{round(tax, 2)} / {round(tax * get_eur_CB(), 2)}₽\n"
                                     f"(рассчитано по курсу ЦБ: {get_eur_CB()}₽)\n"
                                     f"таможенное оформление 1100₽\n"
                                     f"итог налогов и сборов {round(tax * get_eur_CB(), 2) + 1100}₽\n\n"
                                     
                                     f"итоговая сумма заказа с налогами и сборами в рублях {round(total_rub, 3)}₽"
                                 )
                    else:
                        VAT = (subtotal + postage) * (1 - VAT)
                        total = subtotal + postage - VAT
                        total_rub = float(total) * curs
                        change_userstatus(id, "menu")
                        send_msg(id, f"subtotal €{subtotal}\n"
                                     f"VAT discount -€{round(VAT, 2)}\n"
                                     f"postage €{postage}\n"
                                     f"order total €{round(total, 2)}\n\n"
                                     f"итоговая сумма заказа в рублях {round(total_rub, 3)}₽\n"
                                     f"➡ рассчитано по курсу: {curs}₽"
                                 )

                elif msg == "Услуги группы":
                    #  запиь в бд
                    if user_exists(id):
                        change_userstatus(id, "services")
                    else:
                        add_user(id, 0, "services")

                    send_msg_product(id, "Cписок услуг")
                elif msg == "Legit Check":
                    #  запиь в бд
                    if user_exists(id):
                        change_userstatus(id, "services")
                    else:
                        add_user(id, 0, "services")
                    send_msg_product(id, "vk.cc/bYZ4Zy")
                elif msg == "Гарант":
                    #  запиь в бд
                    if user_exists(id):
                        change_userstatus(id, "services")
                    else:
                        add_user(id, 0, "services")
                    send_msg_product(id, "vk.cc/anAhxW")
                elif msg == "Продажа за границу":
                    #  запиь в бд
                    if user_exists(id):
                        change_userstatus(id, "services")
                    else:
                        add_user(id, 0, "services")
                    send_msg_product(id, "vk.cc/bYZ5fd")
                elif msg == "Реклама":
                    #  запиь в бд
                    if user_exists(id):
                        change_userstatus(id, "services")
                    else:
                        add_user(id, 0, "services")
                    send_msg_product(id, """Мы открыты к сотрудничеству с интересными проектами. У нас вы можете заказать платную рекламу или договориться о взаимной.
    
    Мы не рекламируем: рефанд-кард сообщества, пальшопы и прочие группы, противоречащие нашему мировоззрению.
    
    Реклама в истории — 200р
    Репост (не удаляется) — 400р
    Нативная рекламная интеграция — цена обсуждается индивидуально
    
    Контактное лицо по вопросам рекламы: vk.com/ersheshken""")
                elif msg == "Назад":
                    #  запиь в бд
                    if user_exists(id):
                        change_userstatus(id, "menu")
                    else:
                        add_user(id, 0, "menu")
                    send_msg(id, "Вы вышли в главное Меню")

                elif msg == "Таблица размеров":
                    #  запиь в бд
                    if user_exists(id):
                        change_userstatus(id, "menu")
                    else:
                        add_user(id, 0, "menu")

                    vk.messages.send(
                        peer_id=id,
                        attachment=nike_size,
                        keyboard=keyboard.get_keyboard(),
                        random_id=get_random_id()
                    )

                elif msg == "Календарь релизов":
                    #  запиь в бд
                    if user_exists(id):
                        change_userstatus(id, "menu")
                    else:
                        add_user(id, 0, "menu")

                    with open('photos_id.txt', "r") as file_r:
                        file_r = file_r.read()
                        if file_r != "":
                            text_dict = file_r.split(";")
                            for txt in text_dict:
                                if txt != "\n":
                                    text = ""
                                    photo = ""
                                    dict_t = txt.split('\n')
                                    for i in dict_t:
                                        if i[:5] == "photo":
                                            photo = photo + i + ","
                                        else:
                                            text = text + i + "\n"
                                    vk.messages.send(
                                        peer_id=id,
                                        message=text,
                                        attachment=photo,
                                        keyboard=keyboard.get_keyboard(),
                                        random_id=get_random_id()
                                    )
                        else:
                            #  запиь в бд
                            if user_exists(id):
                                change_userstatus(id, "menu")
                            else:
                                add_user(id, 0, "menu")

                            send_msg(id, "Календарь релизов пуст! Ожидайте, когда что-нибудь появится :)")

                elif msg == "Связь с админом":
                    #  запиь в бд
                    if user_exists(id):
                        change_userstatus(id, "dialog")
                    else:
                        add_user(id, 0, "dialog")

                    # Сообщение пользователю
                    send_msg(id, "☎ Ваша заявка была успешно отправлена администратору ✅")
                    send_dialog(id, "Запущен режим дилога, команды не будут работать!")
                    send_dialog(id, "Чтобы выйти из режима нажмите на кнопку или напишите: Начать, Старт, Start или /start")
                    # Сообщение админам
                    send_msg(226847601, "👤 С Вами хочет связаться пользователь Бота ☎\n\n" +
                             "Перейдите по ссылке:\n" +
                             f"https://vk.com/gim166728235?sel={id}")
                    send_msg(80019309, "👤 С Вами хочет связаться пользователь Бота ☎\n\n" +
                             "Перейдите по ссылке:\n" +
                             f"https://vk.com/gim166728235?sel={id}")

                elif msg == "Перезагрузить бота":
                    #  запиь в бд
                    if user_exists(id):
                        change_userstatus(id, "menu")
                    else:
                        add_user(id, 0, "menu")

                    send_msg(id, "Перезагрузка ...")
                    send_msg(id, "Привет 😊")
                    send_msg(id, "Выберите действие\nИ нажмите на кнопку👇")

                elif msg == "/admin_983254":
                    admin_id = id
                    send_msg_admin(id, "Админка активирована")

                else:
                    #  запиь в бд
                    if user_exists(id):
                        change_userstatus(id, "menu")
                    else:
                        add_user(id, 0, "menu")
                    send_msg(id, "Я не знаю такой команды!\nНапишите: Начать, Старт или Start")

            elif check_userinfo(id)['status'] == "dialog":
                if msg.lower() == "/start" or msg.lower() == "начать" or msg.lower() == "старт" or msg.lower() == "start":
                    send_msg(id, "Привет 😊")
                    send_msg(id, "Выберите действие\nИ нажмите на кнопку👇")
                    #  запиь в бд
                    if user_exists(id):
                        change_userstatus(id, "menu")
                    else:
                        add_user(id, 0, "menu")



# АДМИНКА
        elif id == admin_id:
            if msg == "Загрузить фото":
                load_photo = True
                send_msg_admin(id, "▶ Напиши текст сообщение и id фотографии\n" +
                               "▶ Если фотографий несколько, пиши через запятую (без пробелов)\n" +
                               "▶ Когда захочешь закончить, нажми кнопку Выход🚸\n\n" +
                               "Пример:\n" +
                               "Nike Dunk High Michigan\n" +
                                "Date: 26 сентября\n" +
                                "Price: $120\n" +
                                "photo-188345350_457345018\n(или photo-188345350_457345018,photo-112345350_457345018)\n\n" +
                                "Если ты ошибся, очисти список релизов и начни сначала :)")

            elif msg == "Очистить список релизов":
                file = open('photos_id.txt', 'w')
                file.write("")
                file.close()
                send_msg_admin(id, "Очистка прошла успешно ✅")

            elif msg == "Выход":
                admin_id = None
                send_msg(id, "Админка отключена")

            else:
                send_msg_admin(id, "Такой команды нет")
