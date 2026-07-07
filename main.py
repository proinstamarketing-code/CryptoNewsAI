import asyncio

from collectors.rss import get_news
from ai.openrouter import rewrite

from telegram_bot.bot import send_to_moderation

from database import (
    init_db,
    exists,
    save,
)


async def main():

    init_db()

    news = get_news(limit=10)

    if not news:
        print("Новостей нет.")
        return

    for article in news:

        if exists(article["link"]):
            continue

        print(f"Найдена новая новость: {article['title']}")

        text = await rewrite(article)

        await send_to_moderation(text)

        save(article["link"])

        print("Отправлено на модерацию.")

        break

    else:
        print("Новых новостей нет.")


if __name__ == "__main__":
    asyncio.run(main())