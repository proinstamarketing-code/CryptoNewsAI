import asyncio

from collectors.rss import get_news
from ai.openrouter import rewrite
from telegram_bot.bot import send_to_moderation

from database import init_db, exists, save


async def main():

    init_db()

    news = get_news(limit=5)

    if not news:
        print("Новостей нет")
        return

    for article in news:

        if exists(article["link"]):
            print("Новость уже опубликована")
            continue

        text = await rewrite(article)

        await send_to_moderation(text)

        save(article["link"])

        print("Отправлено на модерацию")


if __name__ == "__main__":
    asyncio.run(main())