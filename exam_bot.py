import asyncio
import os
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from database import init_db
from handlers import router


load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')

async def main():
    init_db()
    
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    dp.include_router(router)

    print("Бот в онлайне")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
