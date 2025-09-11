import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from config import API_TOKEN
from db import init_db
from handlers import start, favorites

async def main():
    await init_db()

    bot = Bot(
        token=API_TOKEN,
        default=DefaultBotProperties(parse_mode="HTML")
    )

    dp = Dispatcher()

    dp.include_router(start.router)
    dp.include_router(favorites.router)

    print("🤖 Crypto Bot PG FULL started")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
