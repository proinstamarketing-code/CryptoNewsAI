import asyncio

from ai.deepseek import rewrite
from collectors.rss import get_news
from telegram_bot.bot import bot
from config import CHANNEL_ID


async def main():

    news = get_news(limit=1)

    if not news:
        print("Новостей нет")
        return

    article = news[0]

    text = await rewrite(article["title"])

    text += f"\n\nИсточник:\n{article['link']}"

    await bot.send_message(
        CHANNEL_ID,
        text,
        disable_web_page_preview=False,
    )

    print("Пост опубликован")


if __name__ == "__main__":
    asyncio.run(main())