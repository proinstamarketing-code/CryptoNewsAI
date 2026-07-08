import asyncio

from collectors.rss import get_news

from database import (
    init_db,
    exists,
    save,
)

from ai.analyzer import analyze
from ai.openrouter import rewrite
from ai.editor import edit

from telegram_bot.bot import send_to_moderation


async def main():

    # Создаем БД и таблицу при каждом запуске
    init_db()

    news = get_news()

    if not news:

        print("Новости не найдены.")

        return

    sent = 0

    for article in news:

        if exists(article["link"]):

            continue

        print("=" * 60)
        print("Проверяем:", article["title"])

        # Аналитик
        analysis = analyze(article)

        if not analysis["publish"]:

            print("⛔ Аналитик отклонил новость.")

            save(article["link"])

            continue

        # Автор
        text = await rewrite(article, analysis)

        if text == "SKIP":

            print("✍ Автор решил пропустить.")

            save(article["link"])

            continue

        # Редактор
        text = await edit(text)

        if text == "SKIP":

            print("📝 Редактор отклонил.")

            save(article["link"])

            continue

        # Модерация
        await send_to_moderation(text)

        save(article["link"])

        sent += 1

        print("✅ Отправлено на модерацию.")

        await asyncio.sleep(5)

    print("=" * 60)
    print(f"Готово. Отправлено новостей: {sent}")


if __name__ == "__main__":

    asyncio.run(main())