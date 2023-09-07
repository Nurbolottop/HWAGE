from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.storage import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from config import token  # Assuming 'token' is defined in your config module
import os, time, logging, requests, random
import re

bot = Bot(token=token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
logging.basicConfig(level=logging.INFO)

@dp.message_handler(commands='start')
async def start(message: types.Message):
    await message.answer(f"Привет {message.from_user.full_name}")

@dp.message_handler()
async def download_send_video(message: types.Message):
    await message.answer("Скачиваю видео...")
    
    # Extract video ID from the TikTok URL using regular expression
    url = message.text
    match = re.search(r'vt\.tiktok\.com/(\w+)', url)
    
    if match:
        video_id = match.group(1)
    else:
        await message.answer("Неверный формат ссылки на видео.")
        return

    video_api = requests.get(f'https://api16-normal-c-useast1a.tiktokv.com/aweme/v1/feed/?aweme_id={video_id}').json()
    
    # Получение информации о видео
    video_info = video_api.get('aweme_list')[0]
    video_url = video_info.get('video').get('play_addr').get('url_list')[0]
    video_author = video_info.get('author').get('nickname')
    video_stats = {
        "Комментарии": video_info.get('statistics').get('comment_count'),
        "Просмотры": video_info.get('statistics').get('play_count'),
        "Лайки": video_info.get('statistics').get('digg_count')
    }
    
    if video_url:
        title_video = video_api.get('aweme_list')[0].get('desc')
        if title_video.strip() == '':
            title_video = random.randint(1111, 22222)
        
        try:
            with open(f'video/{title_video}.mp4', 'wb') as video_file:
                video_file.write(requests.get(video_url).content)
            await message.answer("Видео успешно скачано, отправляю...")
        except Exception as error:
            print(f"Error: {error}")
        
        # Отправляем информацию о видео и само видео в телеграм
        try:
            with open(f'video/{title_video}.mp4', 'rb') as send_file:
                await message.answer(f"Автор видео: {video_author}\nID видео: {video_id}\nСтатистика видео:\n{', '.join([f'{key}: {value}' for key, value in video_stats.items()])}", reply_markup=None)
                await message.answer_video(send_file)
        except Exception as error:
            await message.answer(f"Ошибка: {error}")

executor.start_polling(dp, skip_updates=True)
