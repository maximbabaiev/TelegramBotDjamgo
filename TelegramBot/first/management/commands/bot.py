import telebot
from telebot import types
import datetime
from first.models import *

token = "5941529305:AAGTgNW2NEM67Y8MYHYZM2Z4o_X8kcDWIMg"
max_diary = telebot.TeleBot(token)
all_categories = Categorie.objects.all()
keyboard_categories = types.ReplyKeyboardMarkup()
for key in all_categories:
    print(key)
    keyboard_categories.add(types.KeyboardButton(key.name_categories))

keyboard_start = types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_start.add(types.KeyboardButton("registration".title()),
                   types.KeyboardButton("authorization".title()))

keyboard_cancel = types.ReplyKeyboardMarkup()
keyboard_cancel.add(types.KeyboardButton("Назад"))

keyboard_pay = types.ReplyKeyboardMarkup()
keyboard_pay.add(types.KeyboardButton("Оплатить"),
                 types.KeyboardButton("Меню"))


# keyboard_inlines = types.InlineKeyboardMarkup()
# keyboard_inlines.add(types.InlineKeyboardButton(text="Добавить задачу", callback_data="add"),
#                      types.InlineKeyboardButton(text="Просмотреть задачу", callback_data="see"))


@max_diary.message_handler(commands=["start"])
def start(message):
    max_diary.send_message(message.chat.id,
                           "Какая категория вас интересует?",
                           reply_markup=keyboard_categories)


@max_diary.message_handler(content_types=["text"])
def get_text(message):
    if message.text == "Корзина":
        all_cart_user = Order.objects.filter(idUser=1)
        all_cart = [f"Ваша корзина:\n\n"]
        for i in range(len(all_cart_user)):
            all_cart.append(
                f"{i + 1}. {all_cart_user[i].nameProd} -> {all_cart_user[i].value}шт. = {all_cart_user[i].price}$\n")
        max_diary.send_message(message.chat.id, "".join(all_cart), reply_markup=keyboard_pay)
    else:
        keyboard_all_prod_categories = types.InlineKeyboardMarkup()
        all_product_of_categ = ProductModel.objects.filter(nameCategories__name_categories=message.text)
        for j in all_product_of_categ:
            if j.value >= 1:
                keyboard_all_prod_categories.add(
                    types.InlineKeyboardButton(text=f"{j.nameProd} - {j.price}$", callback_data=j.nameProd))
            max_diary.send_message(message.chat.id, f"Товары категории \"{message.text}\"",
                                   reply_markup=keyboard_all_prod_categories)


@max_diary.callback_query_handler(func=lambda call: True)
def callback_data(call):
    if call.message:
        prod = ProductModel.objects.filter(nameProd=call.data)
        date_var = str(datetime.datetime.now())[0:10].split("-")
        time_var = str(datetime.datetime.now())[11:19].split(":")
        Order.objects.get_or_create(
            nameProd=call.data,
            idUser=call.message.chat.id,
            datetime=datetime.datetime(year=int(date_var[0]), month=int(date_var[1]), day=int(date_var[2]),
                                       hour=int(time_var[0]), minute=int(time_var[1]), second=int(time_var[2])),
            value=0,
            price=0)
        max_diary.register_next_step_handler(
            max_diary.send_message(call.message.chat.id,
                                   f"Товар \"{}\" добавлен в корзину в количестве 1 шт.\n\nВведите количество товара: ", reply_markup=keyboard_cancel), add_product_cart)



def add_product_cart(message):
    if message.text == "Назад":
        Order.objects.filter(idUser=message.chat.id, value= 0, price=0).delete()
        max_diary.send_message(message.chat.id, "Какая категория вас интересует?", reply_markup=keyboard_categories)
    else:
        if message.text.isdigit():
        else:
            max_diary.register_next_step_handler(max_diary.send_message(message.chat.id))
# @max_diary.callback_query_handler(func=lambda call: call.data in ["add", "see"])
# def firs(call):
#     if call.data == "add":
#         max_diary.register_next_step_handler(max_diary.send_message(call.message.chat.id, "Hi"), file_w)
#     elif call.data == "see":
#         max_diary.register_next_step_handler(max_diary.send_message(call.message.chat.id, "See"), file_r)
#
#
# @max_diary.message_handler(content_types=["text"])
# def get_bot(message):
#     if message.text.lower() == "registration":
#         max_diary.register_next_step_handler(max_diary.send_message(message.chat.id, "Введите логин"), registration)
#     elif message.text.lower() == "authorization":
#         max_diary.register_next_step_handler(
#             max_diary.send_message(message.chat.id, "Введите логин"), authorization)
#
#
# def authorization(message):
#     global autho_user
#     autho_user = message.text
#     max_diary.register_next_step_handler(
#         max_diary.send_message(message.chat.id, "Авторизация успешна", reply_markup=keyboard_inlines),
#         authorization_text)
#
#
# def authorization_text(message):
#     with open("reg.txt", "r") as file_log:
#         login = file_log.readlines()
#     if message.text in login:
#         max_diary.send_message(message.chat.id, "Авторизация успешна")
#     if message.text not in login:
#         max_diary.send_message(message.chat.id, "Не верный логин")
#
#
# def registration(message):
#     with open("reg.txt", "a") as f:
#         f.write(message.text + "\n")
#     max_diary.send_message(message.chat.id, "Логин сохранен")
#
#
# def file_w(message):
#     with open("file.txt", "a") as file_file:
#         file_file.write("* " + message.text + '\n')
#     max_diary.send_message(message.chat.id, "Задача добавлена")
#
#
# def file_r(message):
#     with open("file.txt", "r", encoding="utf-8") as file:
#         send = file.read()
#     max_diary.send_message(message.chat.id, send)


max_diary.polling(none_stop=True, interval=0)
