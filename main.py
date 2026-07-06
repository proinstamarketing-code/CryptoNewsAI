import asyncio

from telegram_bot.bot import bot


async def main():
    me = await bot.get_me()

    print("=" * 50)
    print("CryptoNewsAI")
    print("=" * 50)

    print(f"Бот подключился успешно!")
    print(f"Имя: {me.first_name}")
    print(f"Username: @{me.username}")
    print(f"ID: {me.id}")


if __name__ == "__main__":
    asyncio.run(main())