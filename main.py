import asyncio

from collectors.rss import get_news
from collectors.article import get_article_text

from ai.openrouter import rewrite

from telegram_bot.bot import send_to_moderation

from database import init_db, exists, save


async def main():

    init_db()

    news = get_news(limit=10)

    if not news:
        print("Новостей нет")
        return

    for article in news:

        if exists(article["link"]):
            continue

        print(f"Проверяем: {article['title']}")

        full_text = get_article_text(article["link"])

        article["content"] = full_text[:5000]

        text = await rewrite(article)

        if text is None:
            print("ИИ решил пропустить новость.")
            save(article["link"])
            continue

        await send_to_moderation(text)

        save(article["link"])

        print("Новость отправлена в модерацию.")

        break

    else:
        print("Подходящих новостей не найдено.")


if __name__ == "__main__":
    asyncio.run(main())