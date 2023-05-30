import asyncio
import subprocess
from pyrogram import Client, filters

api_id = 'API_ID'
api_hash = 'API_HASH'
bot_token = "6134648347:AAG9yO_0Z-wBKrZuTIIB6tIIRLRmJrbJBO4"

menu = 0
phone_number = ""
sc = None

bot = Client("cp_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)
app = Client(f"user_auth",  api_id=api_id, api_hash=api_hash, phone_number=phone_number)


async def auth(number):
    global api_id
    global api_hash
    global phone_number
    global sc
    global menu
    global app
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    print(number)
    if menu == 1:
        await app.connect()
        sc = await app.send_code(phone_number=number)
        print("OK")
    elif menu == 2:
        code = number
        ch = sc.phone_code_hash
        print(ch)
        await app.sign_in(phone_number=phone_number, phone_code_hash=ch, phone_code=str(code))
        await app.disconnect()
        loop.close()
        restart_user_bot2()  #Перезапуск 2 - скрипта

def restart_user_bot2():
    subprocess.Popen(["python", "user_bot2.py"])

@bot.on_message(filters.command(["start"]) & filters.text)
async def command_start(client, message):
    global menu
    await message.reply_text("Чтобы подключить user_bot, необходимо сначала выключить Двухфакторную защиту, если он у вас ввключён!!! Отправьте номер телефона в международном формате (+7934567890)")
    menu = 1

@bot.on_message(filters.text)
async def command_start(client, message):
    global menu
    global phone_number
    global code
    if menu == 1:
        phone = message.text
        phone = phone.replace("+", "")
        if phone.isdigit():
            print(phone)
            phone_number = phone
            await auth(phone_number)
            menu = 2
            print("is ok")
            await message.reply_text("УСПЕШНО!\nТеперь отправь код авторизации, с цифрами через дефиз (пример: \"1-2-266\" и подобное)")
        else:
            await message.reply_text("Телефон неверный! Попробуйте еще раз")
    elif menu == 2:
        v_dig = message.text
        v_dig = v_dig.replace("-", "")
        print(v_dig)
        if v_dig.isdigit():
            code = v_dig
            print(code)
            await auth(code)
            await message.reply_text("УСПЕШНО!\nАвторизация прошла успешно!")

            await asyncio.sleep(5)  # Ожидание 5 секунд

            await message.reply_text("Бот запущен!!!")
            menu = 0
        else:
            await message.reply_text("КОД неверный! Попробуйте еще раз")
            return

print("Бот запущен!")
bot.run()