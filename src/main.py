import asyncio
import logging
from os import getenv

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from src.bot.handlers import get_routers


async def main():
    load_dotenv()
    logging.basicConfig(level=logging.INFO)

    dispatcher = Dispatcher()
    dispatcher.include_routers(*get_routers())

    bot = Bot(token=getenv("BOT_TOKEN"))
    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
