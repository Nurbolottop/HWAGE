import logging
import aiohttp
from bs4 import BeautifulSoup
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor
import config

bot = Bot(token=config.token)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)
dp.middleware.setup(LoggingMiddleware())

URL = 'https://www.nbkr.kg/index.jsp?lang=RUS'

usd_rate = None
euro_rate = None
rub_rate = None
kzt_rate = None

async def update_currency_rates():
    global usd_rate, euro_rate, rub_rate, kzt_rate
    async with aiohttp.ClientSession() as session:
        async with session.get(URL) as response:
            html = await response.text()

    soup = BeautifulSoup(html, 'html.parser')

    currency_rows = soup.find_all('tr')

    currency_rates = {}

    for row in currency_rows:
        columns = row.find_all('td')
        if len(columns) >= 4:
            currency_code = columns[0].text.strip()
            buy_rate = columns[1].text.strip()
            sell_rate = columns[2].text.strip()
            change_percent = columns[3].text.strip()

            currency_rates[currency_code] = {
                'buy_rate': buy_rate,
                'sell_rate': sell_rate,
                'change_percent': change_percent
            }

    usd_rate = currency_rates.get('USD/KGS', {}).get('buy_rate', 'Не найдено')
    euro_rate = currency_rates.get('EUR/KGS', {}).get('buy_rate', 'Не найдено')
    rub_rate = currency_rates.get('RUB/KGS', {}).get('buy_rate', 'Не найдено')
    kzt_rate = currency_rates.get('KZT/KGS', {}).get('buy_rate', 'Не найдено')

async def parse_currency():
    if usd_rate is None or euro_rate is None or rub_rate is None or kzt_rate is None:
        await update_currency_rates()

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item_usd = types.KeyboardButton("KGS → USD")
    item_euro = types.KeyboardButton("KGS → EURO")
    item_rub = types.KeyboardButton("KGS → RUB")
    item_kzt = types.KeyboardButton("KGS → KZT")
    markup.add(item_usd, item_euro, item_rub, item_kzt)
    await message.answer("Выберите валюту для обмена:", reply_markup=markup)

@dp.message_handler(lambda message: message.text.startswith("KGS → USD"))
async def handle_exchange_usd(message: types.Message):
    user_input = message.text
    user_id = message.chat.id

    await update_currency_rates()

    if usd_rate != 'Не найдено':
        await message.answer("Введите сумму в KGS для обмена на USD:")

        @dp.message_handler(lambda message: message.text.isdigit())
        async def process_usd_amount(message: types.Message):
            kgs_amount = float(message.text)
            usd_amount = kgs_amount / float(usd_rate.replace(',', '.'))
            await message.answer(f"{kgs_amount} KGS = {usd_amount:.2f} USD (по курсу {usd_rate})")
    else:
        await message.answer("Извините, данные о курсе USD временно недоступны.")

@dp.message_handler(lambda message: message.text.startswith("KGS → EURO"))
async def handle_exchange_euro(message: types.Message):
    user_input = message.text
    user_id = message.chat.id

    await update_currency_rates()

    if euro_rate != 'Не найдено':
        await message.answer("Введите сумму в KGS для обмена на EURO:")

        @dp.message_handler(lambda message: message.text.isdigit())
        async def process_euro_amount(message: types.Message):
            kgs_amount = float(message.text)
            euro_amount = kgs_amount / float(euro_rate.replace(',', '.'))
            await message.answer(f"{kgs_amount} KGS = {euro_amount:.2f} EURO (по курсу {euro_rate})")
    else:
        await message.answer("Извините, данные о курсе EURO временно недоступны.")


@dp.message_handler(lambda message: message.text.startswith("KGS → RUB"))
async def handle_exchange_rub(message: types.Message):
    user_input = message.text
    user_id = message.chat.id

    await update_currency_rates()

    if rub_rate != 'Не найдено':
        await message.answer("Введите сумму в KGS для обмена на RUB:")

        @dp.message_handler(lambda message: message.text.isdigit())
        async def process_rub_amount(message: types.Message):
            kgs_amount = float(message.text)
            rub_amount = kgs_amount / float(rub_rate.replace(',', '.'))
            await message.answer(f"{kgs_amount} KGS = {rub_amount:.2f} RUB (по курсу {rub_rate})")
    else:
        await message.answer("Извините, данные о курсе RUB временно недоступны.")


@dp.message_handler(lambda message: message.text.startswith("KGS → KZT"))
async def handle_exchange_kzt(message: types.Message):
    user_input = message.text
    user_id = message.chat.id

    await update_currency_rates()

    if kzt_rate != 'Не найдено':
        await message.answer("Введите сумму в KGS для обмена на KZT:")
        
        @dp.message_handler(lambda message: message.text.isdigit())
        async def process_kzt_amount(message: types.Message):
            kgs_amount = float(message.text)
            kzt_amount = kgs_amount / float(kzt_rate.replace(',', '.'))
            await message.answer(f"{kgs_amount} KGS = {kzt_amount:.2f} KZT (по курсу {kzt_rate})")
    else:
        await message.answer("Извините, данные о курсе KZT временно недоступны.")


executor.start_polling(dp, skip_updates=True)
