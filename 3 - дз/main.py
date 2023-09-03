from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.storage import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import logging
import sqlite3

from config import token

bot = Bot(token=token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
logging.basicConfig(level=logging.INFO)

Connection = sqlite3.connect('kebab.db')
cursor = Connection.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY,
        username VARCHAR(200),
        first_name VARCHAR(200),
        last_name VARCHAR(200),
        date_joined TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        name VARCHAR(200),
        phone VARCHAR(20),
        address TEXT
    );
""")

direction_buttons = [
    types.KeyboardButton('Меню'),
    types.KeyboardButton('О нас'),
    types.KeyboardButton('Адрес'),
    types.KeyboardButton('Заказать еду')
]
direction_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*direction_buttons)


@dp.message_handler(commands='start')
async def start(message: types.Message):
    await message.answer(f'Здравствуйте, {message.from_user.full_name}!\nЧто вас интересует?', reply_markup=direction_keyboard)


@dp.message_handler(text='Меню')
async def Menu(message: types.Message):
    await message.reply("""Вали кебаб на 4 человек
1000 г
3200 с

Шефим кебаб
420 с

Симит кебаб
420 с

Форель на мангале целиком
700 с

Адана с йогуртом
450 г
420 с

Киремите кофте
400 с

Патлыжан кебаб
450 г
500 с

Кашарлы кебаб
480 с

Ассорти кебаб (1 персона)
700 с

Крылышки на мангале
450 г
400 с

Фыстыклы кебаб
460 с

Чоп шиш баранина
400 с

Пирзола
300 г
700 с
1
ЗАКАЗАТЬ

Сач кавурма с мясом
450 с
1
ЗАКАЗАТЬ

Сач кавурма с курицей
440 с

Форель на мангале кусочками
900 г
1100 с

Семга с ризотто
450 г
800 с

Донер кебаб 300 г
440 с

Донер сарма
380 г
450 с

Шашлык из баранины
450 г
450 с

Кашарлы кофте
420 с

Ызгара кофте
400 г
400 с

Урфа
420 с

Адана острый
420 с

Адана кебаб
450 г
420 с""")


@dp.message_handler(text='О нас')
async def aboutus(message: types.Message):
    await message.reply("""Ocak Kebap
Кафе "Ожак Кебап" на протяжении 18 лет радует своих гостей с изысканными турецкими блюдами в особенности своим кебабом.

Наше кафе отличается от многих кафе своими доступными ценами и быстрым сервисом.

В 2016 году по голосованию на сайте "Horeca" были удостоены "Лучшее кафе на каждый день" и мы стараемся оправдать доверие наших гостей.

Мы не добавляем консерванты, усилители вкуса, красители, ароматизаторы, растительные и животные жиры, вредные добавки с маркировкой «Е».
У нас строгий контроль качества: наши филиалы придерживаются
норм Кырпотребнадзор и санэпидемстанции. Мы используем только сертифицированную мясную и рыбную продукцию от крупных поставщиков.""")


@dp.message_handler(text='Адрес')
async def address(message: types.Message):
    await message.reply("""Наши адреса:
Исы Ахунбаева ,97а +996700505333

Айтматова, Бишкек, ТЦ Ала-Арча, 3 этаж фудкорт +996507880333

148 Киевская Бишкек, Бишкек Парк, 3 этаж фудкорт +996702049935

Первомайский район, 98 ул. Байтик баатыра, Вефа центр 3 этаж +996700306313

76 Б просп. Чуй, Бишкек, Киргизия, На против ювелирного магазина Алтын +996550799012

Бишкек, 1/2 ул. Горького, М.Горького 1/2, Технопарк 2 этаж. +996555799012

Первомайский район, 46 просп. Эркиндик +996709506228Первомайский район, 46 просп. Эркиндик +996709506228""")
    
class UserOrder(StatesGroup):
    waiting_for_name = State()       
    waiting_for_phone = State()     
    waiting_for_address = State() 
    
@dp.message_handler(text='Заказать еду')
async def orderfood(message: types.Message):
    await message.reply("Для оформления заказа, пожалуйста, введите ваше имя.")
    await UserOrder.waiting_for_name.set()

@dp.message_handler(state=UserOrder.waiting_for_name)
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text

    await message.reply("Отлично! Теперь введите ваш номер телефона.")
    await UserOrder.waiting_for_phone.set()

@dp.message_handler(lambda message: not message.text.isdigit(), state=UserOrder.waiting_for_phone)
async def process_phone_invalid(message: types.Message, state: FSMContext):
    await message.reply("Номер телефона должен содержать только цифры. Пожалуйста, введите ваш номер телефона еще раз (без пробелов и дополнительных символов).")

@dp.message_handler(lambda message: message.text.isdigit(), state=UserOrder.waiting_for_phone)
async def process_phone(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['phone'] = message.text

    await message.reply("Отлично! Теперь введите ваш адрес доставки.")
    await UserOrder.waiting_for_address.set()

@dp.message_handler(lambda message: len(message.text) < 10, state=UserOrder.waiting_for_address)
async def process_address_invalid(message: types.Message):
    return await message.reply("Адрес должен быть более подробным. Пожалуйста, введите ваш адрес еще раз.")

@dp.message_handler(lambda message: len(message.text) >= 10, state=UserOrder.waiting_for_address)
async def process_address(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['address'] = message.text

        # Теперь у вас есть данные о пользователе: data['name'], data['phone'], data['address']
        # Вы можете записать их в базу данных, например, в вашей таблице 'users'

        # Здесь можно добавить код для записи данных пользователя в базу данных
        cursor.execute("INSERT INTO users (username, first_name, last_name, date_joined, name, phone, address) VALUES (?, ?, ?, ?, ?, ?, ?)",
                       (message.from_user.username, message.from_user.first_name,
                        message.from_user.last_name, message.date, data['name'], data['phone'], data['address']))
        Connection.commit()

    await message.reply("Спасибо за заказ! Ваш заказ будет доставлен по указанному адресу.", reply_markup=types.ReplyKeyboardRemove())

# executor.start_polling(dp)
executor.start_polling(dp, skip_updates=True)