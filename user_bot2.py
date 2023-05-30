import asyncio
from pyrogram import Client, filters
from time import sleep
import pyttsx3
from pyrogram.errors import FloodWait
from pyrogram import filters
import os


api_id = 'API-ID'
api_hash = 'API-HASH'

menu = 0
phone_number = ""
sc = None


app = Client(f"user_auth", api_id=api_id, api_hash=api_hash, phone_number=phone_number)

#путь к файлу голосового сообщения
voice_file_path = "голос2.ogg"

# Инициализация pyttsx3
engine = pyttsx3.init()

@app.on_message(filters.reply & filters.text & filters.regex(r"\.к ты кто"))
async def who_am_i(client, message):
    replied_message = message.reply_to_message

    if replied_message:
        user = replied_message.from_user

        if user:
            username = user.username or ""
            first_name = user.first_name or ""
            user_id = user.id

            text = f"Это пользователь @{username}\nИмя: {first_name}\nID: {user_id}"

            await message.edit_text(text)


@app.on_message(filters.command(["кк"], prefixes="."))
async def repeat_message(client, message):
    # Разбиваем аргументы команды
    args = message.text.split()
    if len(args) >= 4:
        try:
            count = int(args[1])  # Получаем количество сообщений
            text = " ".join(args[2:-1])  # Получаем текст сообщения
            speed = float(args[-1])  # Получаем скорость отправки

            # Удаляем исходное сообщение
            await message.delete()

            # Отправляем указанное количество сообщений с указанным текстом и заданной скоростью
            for _ in range(count):
                await client.send_message(message.chat.id, text)

                # Задержка перед отправкой следующего сообщения
                await asyncio.sleep(speed)

        except ValueError:
            await message.reply("Неверный формат команды. Пожалуйста, используйте `.кк [число] [текст] [скорость]`.")
    else:
        await message.reply("Недостаточно аргументов. Пожалуйста, используйте `.кк [число] [текст] [скорость]`.")


@app.on_message(filters.command("type", prefixes=".") & filters.me)
def type(_, msg):
    orig_text = msg.text.split(".type ", maxsplit=1)[1]
    text = orig_text
    tbp = ""
    typing_symbol = "❋"

    while(tbp != orig_text):
        try:
            msg.edit(tbp + typing_symbol)
            sleep(0.01)
            tbp = tbp + text[0]
            text = text[1:]
            msg.edit(tbp)
            sleep(0.01)
        except FloodWait as e:
            sleep(e.x)

@app.on_message(filters.command("профиль", prefixes=".к ") & filters.me)
def profile(_, msg):
    name = msg.from_user.first_name
    user_id = msg.from_user.id  # ID пользователя

    profile_text = f"Ваш профиль:\nИмя: {name}\nID: {user_id}"
    msg.edit_text(profile_text)

# Обработчик команды ".к гс"
@app.on_message(filters.command("гс", prefixes=".к ") & filters.me)
def send_voice(_, msg):
    # Проверяем, существует ли файл голосового сообщения
    if os.path.exists(voice_file_path):

        msg.delete()
        # Отправляем голосовое сообщение
        msg.reply_voice(voice_file_path)
    else:
        # Если файл не найден, отправляем сообщение об ошибке
        msg.reply_text("Файл голосового сообщения не найден.")


@app.on_message(filters.command("вгс", prefixes=".к") & filters.reply & filters.me)
def voice_reply(_, msg):
    replied_msg = msg.reply_to_message
    if replied_msg:
        text_to_speak = replied_msg.text  # Получаем текст из сообщения на которое ответили
        voice_file = "voice_message.ogg"  # Имя файла голосового сообщения

        # Конвертация текста в голосовое сообщение
        engine.save_to_file(text_to_speak, voice_file)
        engine.runAndWait()

        #удаление предыдущего сообщения
        msg.delete()

        # Отправка голосового сообщения
        msg.reply_audio(voice_file)

async def run():
    await app.start()

loop = asyncio.get_event_loop()
loop.create_task(run())
loop.run_forever()