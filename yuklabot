import asyncio
import os
import sqlite3
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import FSInputFile, InlineKeyboardMarkup, InlineKeyboardButton
from yt_dlp import YoutubeDL

# --- SOZLAMALAR ---
TOKEN = "8185111678:AAEoldj5n8ZBJl95Cd01gjYUK2aTxcQyAK8"
ADMIN_ID = 7751791288 # O'z ID-ingizni yozing
CHANNELS = ["@byamirovai"] # Kanal linkini @ bilan yozing

bot = Bot(token=TOKEN)
dp = Dispatcher()

# --- BAZA ---
db = sqlite3.connect("users.db")
cursor = db.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY)")
db.commit()

# --- OBUNANI TEKSHIRISH FUNKSIYASI ---
async def check_sub(user_id):
    for channel in CHANNELS:
        try:
            member = await bot.get_chat_member(chat_id=channel, user_id=user_id)
            if member.status == 'left':
                return False
        except Exception:
            return False
    return True

# --- VIDEO YUKLASH ---
def download_video(url):
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'video_%(id)s.mp4',
        'quiet': True,
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    cursor.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (message.from_user.id,))
    db.commit()
    await message.answer(f"Salom! Videoni yuklash uchun link yuboring.")

@dp.message(F.text.startswith("http"))
async def handle_link(message: types.Message):
    # Obunani tekshirish
    is_sub = await check_sub(message.from_user.id)
    
    if not is_sub:
        # Obuna bo'lish uchun knopka chiqarish
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Kanalga obuna bo'lish ➕", url=f"https://t.me/{CHANNELS[0][1:]}")],
            [InlineKeyboardButton(text="Tekshirish ✅", callback_data="check")]
        ])
        await message.answer("Kechirasiz, botdan foydalanish uchun kanalimizga a'zo bo'lishingiz kerak!", reply_markup=keyboard)
        return

    status_msg = await message.answer("⏳ Video yuklanmoqda...")
    try:
        loop = asyncio.get_event_loop()
        file_path = await loop.run_in_executor(None, download_video, message.text)
        video_file = FSInputFile(file_path)
        await message.answer_video(video_file, caption="Mana video! ✅\n@byamirovyukla_bot")
        os.remove(file_path)
        await status_msg.delete()
    except Exception as e:
        await status_msg.edit_text("❌ Xatolik!")

# --- TEKSHIRISH KNOPKASI BOSILGANDA ---
@dp.callback_query(F.data == "check")
async def check_callback(call: types.CallbackQuery):
    if await check_sub(call.from_user.id):
        await call.message.delete()
        await call.message.answer("Rahmat! Endi bemalol video linkini yuborishingiz mumkin.")
    else:
        await call.answer("Siz hali a'zo bo'lmadingiz! ❌", show_alert=True)

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
