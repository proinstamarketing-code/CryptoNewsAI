import asyncio

from aiogram import Dispatcher

from telegram_bot.bot import bot
from telegram_bot.moderation import router


async def main():

    dp = Dispatcher()

    dp.include_router(router)

    print("=" * 60)
    print("🚀 Moderation Bot started")
    print("=" * 60)

    await dp.start_polling(bot)


if __name__ == "__main__":

    asyncio.run(main())