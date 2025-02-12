import asyncio
from logging import getLogger

from config import TG_TOKEN
from aiogram import Bot, Dispatcher
from telegram.handlers import router

bot = Bot(token=TG_TOKEN)
dp = Dispatcher()
logger = getLogger(__name__)


async def main():
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())

    except KeyboardInterrupt:
        print("Exit")
