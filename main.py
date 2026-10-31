import asyncio
import os
from aiohttp import web
from aiogram import Bot, Dispatcher

TOKEN = "9287007550:AAE_08mQHSBMJcTSC1OnCEl2wodjjeeEDM4"
CHANNEL_ID = "@kanaliniz_usernami"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Render uchun kichik veb-server (port xatosini oldini oladi)
async def handle(request):
    return web.Response(text="Bot is running!")

async def web_server():
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 10000))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

async def main():
    # Veb-server va botni bir vaqtda ishga tushirish
    await web_server()
    print("Bot ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

