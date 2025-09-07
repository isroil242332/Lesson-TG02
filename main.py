import asyncio
import random
import os
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, FSInputFile, Voice
from aiogram.filters import CommandStart, Command
from config import TOKEN
from deep_translator import GoogleTranslator  # Используем эту библиотеку для перевода

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Создаем папку для изображений, если она не существует
if not os.path.exists('img'):
    os.makedirs('img')


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Приветики, я бот!")


@dp.message(Command('help'))
async def help(message: Message):
    await message.answer("Этот бот умеет выполнять команды:\n/start\n/help\n/photo\n/video\n/audio\n/voice")


@dp.message(F.text == "что такое ИИ?")
async def aitext(message: Message):
    await message.answer(
        'Искусственный интеллект — это свойство искусственных интеллектуальных систем выполнять творческие функции,'
        ' которые традиционно считаются прерогативой человека; наука и технология создания интеллектуальных машин,'
        ' особенно интеллектуальных компьютерных программ')


@dp.message(F.photo)
async def react_photo(message: Message):
    answers = ['Ого, какая фотка!', 'Непонятно, что это такое', 'Не отправляй мне такое больше']
    rand_answ = random.choice(answers)
    await message.answer(rand_answ)

    # Сохраняем фото в папку img
    try:
        photo = message.photo[-1]  # Берем фото наивысшего качества
        file_info = await bot.get_file(photo.file_id)
        downloaded_file = await bot.download_file(file_info.file_path)

        # Создаем имя файла с timestamp
        import datetime
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"img/photo_{timestamp}_{message.from_user.id}.jpg"

        # Сохраняем файл
        with open(filename, 'wb') as new_file:
            new_file.write(downloaded_file.read())

        await message.answer(f"Фото сохранено как {filename}")
    except Exception as e:
        await message.answer(f"Ошибка при сохранении фото: {e}")


@dp.message(Command('photo'))
async def photo(message: Message):
    photos = [
        'https://i.pinimg.com/736x/b9/58/ff/b958ff7676e74253515eedaa9fc51cb3.jpg',
        'https://avatars.mds.yandex.net/i?id=3a1609c609bf0774d952011d99419dd0589ea532-16282520-images-thumbs&n=13'
    ]
    rand_photo = random.choice(photos)
    await message.answer_photo(photo=rand_photo, caption='Это супер крутая картинка')


@dp.message(Command('video'))
async def video(message: Message):
    await bot.send_chat_action(message.chat.id, 'upload_video')
    video = FSInputFile('video.mp4')
    await bot.send_video(message.chat.id, video)


@dp.message(Command('audio'))
async def audio(message: Message):
    audio = FSInputFile('cat.mp3')
    await bot.send_audio(message.chat.id, audio)


@dp.message(Command('voice'))
async def send_voice(message: Message):
    try:
        # Отправляем голосовое сообщение
        voice = FSInputFile('voice_message.ogg')  # Убедитесь, что файл существует
        await bot.send_voice(message.chat.id, voice, caption="Это голосовое сообщение от бота!")
    except FileNotFoundError:
        await message.answer("Файл голосового сообщения не найден. Создайте файл 'voice_message.ogg'")


@dp.message(F.text)
async def translate_text(message: Message):
    # Пропускаем команды и специальные тексты
    if message.text.startswith('/') or message.text == "что такое ИИ?":
        return

    try:
        # Переводим текст на английский
        translation = GoogleTranslator(source='auto', target='en').translate(message.text)
        await message.answer(f"🇬🇧 Translation: {translation}")
    except Exception as e:
        await message.answer(f"Ошибка перевода: {e}")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())