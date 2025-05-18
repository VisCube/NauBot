import asyncio
import logging
from os import getenv

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from src.bot.handlers import get_routers
from src.db import init_db
from src.db.database import async_session
from src.bot.middleware.database import DatabaseMiddleware


async def main():
    load_dotenv()
    logging.basicConfig(level=logging.INFO)
    
    await init_db()
    
    dispatcher = Dispatcher()

    dispatcher.update.middleware(DatabaseMiddleware(async_session))
    
    dispatcher.include_routers(*get_routers())

    bot = Bot(token=getenv("BOT_TOKEN"))
    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
