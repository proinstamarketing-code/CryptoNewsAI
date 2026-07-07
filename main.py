import asyncio

from collectors.rss import get_news
from database import exists, save

from ai.analyzer import analyze
from ai.openrouter import rewrite
from ai.editor import edit

from telegram_bot.bot import send_to_moderation


async def main():

    news = get_news()

    if not news:
        print("Новости не найдены.")
        return

    sent = 0

    for article in news:

        if exists(article["link"]):
            continue

        print(f"Проверяем: {article['title']}")

        # Анализируем новость
        analysis = await analyze(article)

        if not analysis.get("publish", True):

            print("Аналитик решил пропустить новость.")

            save(article["link"])

            continue

        # Пишем статью с учетом анализа
        text = await rewrite(article, analysis)

        if text == "SKIP":

            print("Автор решил пропустить новость.")

            save(article["link"])

            continue

        # Финальная редактура
        text = await edit(text)

        if text == "SKIP":

            print("Редактор отклонил новость.")

            save(article["link"])

            continue

        # Отправка на модерацию
        await send_to_moderation(text)

        save(article["link"])

        sent += 1

        print("✅ Новость отправлена на модерацию.")

        await asyncio.sleep(5)

    print(f"\nГотово. Отправлено новостей: {sent}")


if __name__ == "__main__":

    asyncio.run(main())