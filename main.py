import asyncio

from collectors.rss import get_news
from collectors.article import load_article

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

    init_db()

    news = get_news()

    if not news:
        print("Новости не найдены.")
        return

    print(f"Получено новостей: {len(news)}")

    sent = 0

    for article in news:

        if not article.get("link"):
            continue

        if exists(article["link"]):
            print("Уже опубликована.")
            continue

        print("=" * 70)
        print("Проверяем:", article["title"])

        article["content"] = await load_article(
            article["link"],
            article["summary"],
        )

        print(
            f"Длина статьи: {len(article['content'])} символов"
        )

        analysis = analyze(article)

        print(
            f"Оценка: {analysis['score']}/10 | Категория: {analysis['category']}"
        )

        print("✍ Генерация статьи...")

        text = await rewrite(article, analysis)

        if text == "SKIP":

            print("⚠ OpenRouter недоступен.")

            text = f"""📰 {article['title']}

{article['summary']}

━━━━━━━━━━━━━━

🔗 Источник:
{article['link']}
"""

        else:

            print("📝 Редактор...")

            edited = await edit(text)

            if edited != "SKIP":
                text = edited

            # добавляем источник только если его ещё нет
            if "Источник" not in text:
                text += f"""

━━━━━━━━━━━━━━

🔗 Источник:
{article['link']}
"""

        print("📨 Отправка на модерацию...")

        message = await send_to_moderation(text)

        if message is None:

            print("❌ Новость НЕ отправлена")

            continue

        save(
            link=article["link"],
            title=article.get("title", ""),
            category=analysis.get("category", ""),
            published_at=article.get("published", ""),
        )

        sent += 1

        print("✅ Успешно отправлено")

        await asyncio.sleep(5)

    print("=" * 70)
    print(f"Готово. Отправлено: {sent}")


if __name__ == "__main__":
    asyncio.run(main())