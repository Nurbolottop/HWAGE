import requests
from bs4 import BeautifulSoup
import sqlite3
from datetime import datetime

# Создаем подключение к базе данных
conn = sqlite3.connect('laptops.db')
cursor = conn.cursor()

# Создаем таблицу, если она не существует
cursor.execute('''
    CREATE TABLE IF NOT EXISTS laptops (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        price REAL,
        created DATETIME
    )
''')
conn.commit()


# URL страницы для парсинга
url = 'https://www.sulpak.kg/f/noutbuki'

# Отправляем запрос на сервер и получаем HTML-код страницы
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Извлекаем данные и записываем их в базу данных
laptops = soup.find_all('div', class_='product-card')
for laptop in laptops:
    title = laptop.find('h3', class_='product-title').text.strip()
    price = float(laptop.find('span', class_='product-price').text.strip().replace(' ', '').replace('KGS', ''))
    created = datetime.now()

    # Записываем данные в базу данных
    cursor.execute('INSERT INTO laptops (title, price, created) VALUES (?, ?, ?)', (title, price, created))
    conn.commit()

# Закрываем соединение с базой данных
conn.close()
