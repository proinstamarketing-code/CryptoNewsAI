import asyncio

from collectors.rss import get_news
from collectors.article import get_article_text

from ai.editor import review

from telegram_bot.bot import send_to_moderation

from database import init_db, exists, save


async def main():

    init_db()

    news = get_news(limit=20)

    if not news:
        print("Новостей нет")
        return

    for article in news:

        if exists(article["link"]):
            continue

        print(f"Проверяем: {article['title']}")

        full_text = get_article_text(article["link"])

        article["content"] = full_text[:5000]

        text = await review(article)

        if text is None:

            print("Редактор отклонил новость.")

            continue

        await send_to_moderation(text)

        save(article["link"])

        print("Отправлено в модерацию.")

        break

    else:

        print("Подходящих новостей нет.")


if __name__ == "__main__":
    asyncio.run(main())