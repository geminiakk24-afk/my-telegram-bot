import asyncio
import os
from aiogram import Bot, Dispatcher, types, F
from yt_dlp import YoutubeDL
from aiogram.types import FSInputFile
from aiohttp import web

TOKEN = "8185111678:AAEoldj5n8ZBJl95Cd01gjYUK2aTxcQyAK8"
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Render o'chib qolmasligi uchun oddiy Web Server
async def handle(request):
    return web.Response(text="Bot is running!")

app = web.Application()
app.router.add_get("/", handle)

def download_video(url):
    ydl_opts = {
        'format': 'best', 
        'outtmpl': 'video_%(id)s.mp4', 
        'quiet': True,
        'no_warnings': True
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)

@dp.message(F.text.startswith("http"))
async def handle_link(message: types.Message):
    msg = await message.answer("⏳ Video yuklanmoqda...")
    try:
        # Videoni alohida oqimda yuklash
        loop = asyncio.get_event_loop()
        file_path = await loop.run_in_executor(None, download_video, message.text)
        
        video_file = FSInputFile(file_path)
        await message.answer_video(video_file, caption="Tayyor! ✅\n@byamirovyukla_bot")
        
        if os.path.exists(file_path):
            os.remove(file_path)
        await msg.delete()
    except Exception as e:
        await msg.edit_text(f"❌ Xatolik yuz berdi!")
        print(f"Error: {e}")

async def main():
    # Web serverni bot bilan birga ishga tushirish
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', os.getenv("PORT", 10000))
    await site.start()
    
    print("Bot Render-da muvaffaqiyatli ishga tushdi!")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
