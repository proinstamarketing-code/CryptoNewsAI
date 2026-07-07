from aiogram import Dispatcher

from bot import bot
from telegram_bot.moderation import router


dp = Dispatcher()

dp.include_router(router)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())