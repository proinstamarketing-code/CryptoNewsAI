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

        # -------------------------------------------------
        # Загружаем полный текст статьи
        # -------------------------------------------------

        article["content"] = await load_article(
            article["link"],
            article["summary"],
        )

        print(
            f"Длина статьи: {len(article['content'])} символов"
        )

        # -------------------------------------------------
        # Аналитик
        # -------------------------------------------------

        analysis = analyze(article)

        if not analysis["publish"]:

            print("⛔ Аналитик отклонил.")

            save(
                link=article["link"],
                title=article.get("title", ""),
                category=analysis.get("category", ""),
                published_at=article.get("published", ""),
            )

            continue

        print("✍ Генерация статьи...")

        text = await rewrite(article, analysis)

        # -------------------------------------------------
        # Если OpenRouter недоступен
        # -------------------------------------------------

        if text == "SKIP":

            print("⚠ OpenRouter недоступен.")

            text = f"""⚠️ <b>Черновик (ИИ временно недоступен)</b>

📰 <b>{article['title']}</b>

{article['summary']}

📊 <b>Оценка:</b> {analysis.get("score",0)}/10
📂 <b>Категория:</b> {analysis.get("category","Crypto")}

🔗 {article["link"]}
"""

        else:

            print("📝 Редактор...")

            edited = await edit(text)

            if edited != "SKIP":

                text = edited

            else:

                print("Редактор недоступен. Используем текст автора.")

        print("📨 Отправка на модерацию...")

        await send_to_moderation(text)

        save(
            link=article["link"],
            title=article.get("title", ""),
            category=analysis.get("category", ""),
            published_at=article.get("published", ""),
        )

        sent += 1

        print("✅ Отправлено.")

        await asyncio.sleep(5)

    print("=" * 70)
    print(f"Готово. Отправлено: {sent}")


if __name__ == "__main__":

    asyncio.run(main())